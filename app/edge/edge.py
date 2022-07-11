import threading
import zmq
import logging

from datetime import datetime
from edge.simulated_sensor.parking_garage import ParkingGarage

from edge.message_queue.message_queue import MessageQueue
from common.message import Message, MessageType, PayloadType


def simulate_parking_garage(msg_queue: MessageQueue, garage_name: str):
    parking_garage = ParkingGarage(garage_name=garage_name)

    def on_car_leaving(license_plate: str, duration_minutes: int):
        req = Message(payload={'license_plate': license_plate, 'duration_minutes': duration_minutes},
                      payload_type=PayloadType.CAR_BILLING,
                      type=MessageType.REQ,
                      sender=garage_name)
        msg_queue.enqueue(req)

    # use event based
    simulation_thread = threading.Thread(
        target=parking_garage.start_simulation, args=[on_car_leaving])

    simulation_thread.start()

    # polling
    next_occupancy_transmit_time = datetime.now().timestamp() + 5
    next_occupancy_request_time = datetime.now().timestamp() + 10
    while True:
        # at a regular interval transmit occupancy info from server
        now = datetime.now().timestamp()

        if now > next_occupancy_transmit_time:
            next_occupancy_transmit_time = now + 5

            occupancy = parking_garage.get_occupancy()
            max_occupancy = parking_garage.max_capacity

            print("sending occupancy")

            req = Message(
                payload={garage_name: {"current_occupancy": occupancy, "max_capacity": max_occupancy}},
                payload_type=PayloadType.OCCUPANCY,
                type=MessageType.REQ,
                sender=garage_name)
            msg_queue.enqueue(req)

        if now > next_occupancy_request_time:
            next_occupancy_request_time = now + 10

            print("requesting occupancy")

            req = Message(
                # payload={garage_name: occupancy},
                payload_type=PayloadType.OCCUPANCY_REQUEST,
                type=MessageType.REQ,
                sender=garage_name)
            msg_queue.enqueue(req)


def handle_resp(resp: Message):
    if resp.payload is None:
        return
    
    if resp.payload_type == PayloadType.OCCUPANCY:
        print(f"occupancy on all garages:")
        for k, v in resp.payload.items():
            print(f"\tgarage {k}: occupancy: {v['current_occupancy']}/{v['max_capacity']}")


def loop(socket, msg_queue):
    msg = msg_queue.retrieve()
    if msg is None:
        return

    logging.info(f"sending message: {msg.id}")
    socket.send(msg.construct_msg())

    try:
        raw = socket.recv()
    except zmq.Again:
        return

    resp = Message.from_bytes(raw)

    if resp is not None and resp.type == MessageType.ACK:
        logging.info(f"recvd ack: {resp.id}")
        msg_queue.dequeue(resp.id)
        # this would likely happen asynchronously
        handle_resp(resp)
    else:
        logging.warning(f"unhandled msg")


def run_edge(garage_name: str, server_ip: str, server_port: str):
    msg_queue = MessageQueue(garage_name=garage_name)

    # every 30 seconds:
    # call parking_garage.cars_recently_left() and make one message (for billing purposes)
    # add to message queue: CAR BILLING LIST (A1 Type 2)
    sensor_thread = threading.Thread(
        target=simulate_parking_garage, args=[msg_queue, garage_name])
    sensor_thread.start()

    # init socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.REQ_RELAXED, 1)
    socket.connect(f"tcp://{server_ip}:{server_port}")

    logging.info(f"Connecting to server at 'tcp://{server_ip}:{server_port}'")

    try:
        while True:
            loop(socket=socket, msg_queue=msg_queue)
    except KeyboardInterrupt:
        # we simulate crashing by stopping th process
        msg_queue.sync()
