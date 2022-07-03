import zmq
import shelve
import logging

from os import path
from random import random
from datetime import datetime

from common.message import Message, MessageType, PayloadType

# dictionary of parking garages
# with latest information on occupancy


def bill_customer(license_plate: str, duration_minutes: int, garage: str):
    print(
        f"Sending bill to '{license_plate}' for parking {duration_minutes} min in garage {garage}.")


occupancy = shelve.open(path.join("_tmp", "_server_occupancy"))
msg_log = shelve.open(path.join("_tmp", "_server_msg_log"))


def handle_msg(msg: Message):
    if msg.id in msg_log:
        logging.info("dropping message - already processed")
        return None, None

    msg_log[msg.id] = datetime.now().timestamp()

    # seen msg before?
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
        # update occupancy
        occupancy.update(msg.payload)
    elif msg.payload_type == PayloadType.OCCUPANCY_REQUEST:
        resp_payload_type = PayloadType.OCCUPANCY
        resp_payload = {key: occupancy[key] for key in occupancy.keys()}

    return resp_payload, resp_payload_type


def loop(socket):
    # listen for msg
    raw_msg = socket.recv()

    # handle msg
    msg = Message.from_bytes(raw_msg)

    if random() < 0.1:
        # simulate msg being dropped
        socket.send_string("")
        logging.info(f"simulate having dropped req {msg.id}")
        return

    # this would likely happen asynchronously
    resp_payload, resp_payload_type = handle_msg(msg)

    # acknowledge msg
    if random() < 0.1:
        # simulate ACK being dropped
        socket.send_string("")
        logging.info(f"simulate having dropped ack {msg.id}")
        return

    logging.info(f"received and ack {msg.id}")
    resp = Message(type=MessageType.ACK, _id=msg.id, sender="server",
                   payload=resp_payload, payload_type=resp_payload_type)

    # build response
    socket.send(resp.construct_msg(), zmq.NOBLOCK)


def run_server():
    # init message receiver
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    # socket.setsockopt(zmq.REQ_RELAXED, 1)
    socket.bind("tcp://*:5555")

    try:
        while True:
            loop(socket=socket)
    except KeyboardInterrupt:
        # we simulate crashing by stopping th process
        occupancy.sync()
        msg_log.sync()
