import json
from random import random
import zmq

from common.message import Message, MessageType, PayloadType

# dictionary of parking garages
# with latest information on occupancy


def bill_customer(license_plate: str, duration_minutes: int, garage: str):
    print(
        f"Sending bill to '{license_plate}' for parking {duration_minutes} min in garage {garage}.")


def handle_msg(msg: Message) -> dict | None:
    resp_payload = None
    resp_payload_type = None
    if msg.payload_type == PayloadType.CAR_BILLING:
        license_plate = msg.payload["license_plate"]
        duration_minutes = msg.payload["duration_minutes"]
        garage = msg.sender
        bill_customer(license_plate=license_plate,
                      duration_minutes=duration_minutes,
                      garage=garage)
    elif msg.payload_type == PayloadType.OCCUPANCY:
        # update_occupancy()
        pass
    elif msg.payload_type == PayloadType.OCCUPANCY_REQUEST:
        resp_payload_type = PayloadType.OCCUPANCY
        payload = {
            "1": 100,
            "2": 300,
            "3": 400
        }

    return resp_payload, resp_payload_type


def run_server():
    # init message receiver
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    # socket.setsockopt(zmq.REQ_RELAXED, 1)
    socket.bind("tcp://*:5555")

    while True:
        # listen for msg
        raw_msg = socket.recv()

        # handle msg
        msg = Message.from_bytes(raw_msg)

        if random() < 0.1:
            # simulate msg being dropped
            socket.send_string("")
            print(f"didn't receive {msg.id}")
            continue

        # this would likely happen asynchronously
        resp_payload, resp_payload_type = handle_msg(msg)

        # acknowledge msg
        if random() < 0.1:
            # simulate ACK being dropped
            socket.send_string("")
            print(f"didn't ack {msg.id}")
            continue

        print(f"ack: {msg.id}")
        resp = Message(type=MessageType.ACK, _id=msg.id, sender="server",
                       payload=resp_payload, payload_type=resp_payload_type)

        # build response
        socket.send(resp.construct_msg(), zmq.NOBLOCK)
