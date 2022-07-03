from datetime import datetime
from random import random
from edge.simulated_sensor.parking_garage import ParkingGarage
from edge.message_queue.message_queue import MessageQueue
from common.message import Message, MessageType, PayloadType
import zmq
import threading


def simulate_parking_garage(msg_queue: MessageQueue, garage_name: str):
    next_req = datetime.now().timestamp()
    next_car = datetime.now().timestamp() + 4
    while True:
        # at a regular interval REQUEST occupancy info from server
        # add to message queue: REQUEST msg (A1 Type 1)

        now = datetime.now().timestamp()
        if now > next_req:
            next_req = now + 3

            req = Message(
                payload={garage_name: 100},
                payload_type=PayloadType.OCCUPANCY,
                type=MessageType.REQ,
                sender=garage_name)
            msg_queue.enqueue(req)

        if now > next_car:
            next_car = now + random() * 10

            req = Message(payload={'license_plate': 'abc', 'duration_minutes': 140},
                          payload_type=PayloadType.CAR_BILLING,
                          type=MessageType.REQ,
                          sender=garage_name)
            msg_queue.enqueue(req)

    # parking_garage = ParkingGarage(id = 1)
    # parking_garage.start()


def handle_resp(resp: Message):
    if resp.payload is not None:
        print(f"{resp.payload}")


def loop(socket, msg_queue):
    msg = msg_queue.retrieve()
    if msg is None:
        return

    print(f"sending message: {msg.id}")
    socket.send(msg.construct_msg())

    try:
        raw = socket.recv()
    except zmq.Again:
        return

    resp = Message.from_bytes(raw)

    if resp is not None and resp.type == MessageType.ACK:
        print(f"recvd ack: {resp.id}")
        msg_queue.dequeue(resp.id)
        # this would likely happen asynchronously
        handle_resp(resp)
        print(f"remaining: {len(msg_queue)}")
    else:
        print(f"unhandled msg")


def run_edge(garage_name: str):
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
    socket.connect("tcp://localhost:5555")

    try:
        while True:
            loop(socket=socket, msg_queue=msg_queue)
    except KeyboardInterrupt:
        msg_queue.sync()
