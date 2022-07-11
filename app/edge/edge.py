import threading
import zmq
import logging

from random import random
from datetime import datetime

from edge.message_queue.message_queue import MessageQueue
from common.message import Message, MessageType, PayloadType


def simulate_parking_garage(msg_queue: MessageQueue, garage_name: str):
    next_req = datetime.now().timestamp()
    next_car = datetime.now().timestamp() + 4
    next_data = datetime.now().timestamp() + 4

    # parking_garage = ParkingGarage(id = 1)
    # parking_garage.start_simulation()

    def event_callback(license_plate: str, duration_minutes: int):
        req = Message(payload={'license_plate': license_plate, 'duration_minutes': duration_minutes},
                        payload_type=PayloadType.CAR_BILLING,
                        type=MessageType.REQ,
                        sender=garage_name)
        msg_queue.enqueue(req)

    # parking_garage.on_car_leave = event_callback
    
    while True:
        # at a regular interval REQUEST occupancy info from server
        # add to message queue: REQUEST msg (A1 Type 1)
        now = datetime.now().timestamp()

        if now > next_data:
            # B1 msg -> request all other garage occupancies
            next_data = now + 10

            req = Message(
                payload_type=PayloadType.OCCUPANCY_REQUEST,
                type=MessageType.REQ,
                sender=garage_name)
            msg_queue.enqueue(req)

        if now > next_req:
            #A1 type1 msg -> send current occupancy of this garage
            next_req = now + 3

            # occupancy = parking_garage.get_occupancy()

            req = Message(
                payload={garage_name: int(random() * 500)},
                payload_type=PayloadType.OCCUPANCY,
                type=MessageType.REQ,
                sender=garage_name)
            msg_queue.enqueue(req)

        if now > next_car:
            #A2 type2 msg -> car leave, to get  the bill
            next_car = now + random() * 10


            req = Message(payload={'license_plate': 'abc', 'duration_minutes': 140},
                          payload_type=PayloadType.CAR_BILLING,
                          type=MessageType.REQ,
                          sender=garage_name)
            msg_queue.enqueue(req)



def handle_resp(resp: Message):
    if resp.payload is not None:
        print(f"{resp.payload}")


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
