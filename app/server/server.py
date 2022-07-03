import json
from random import random
import zmq

from common.message import Message, MessageType

# dictionary of parking garages
# with latest information on occupancy


def bill_customer(license_plate: str, parking_duration_minutes: int):
    # "billing service"
    # send the customer an imaginary bill
    pass


def run_server():
    # init message receiver
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    # socket.setsockopt(zmq.REQ_RELAXED, 1)
    socket.bind("tcp://*:5555")

    while True:
        raw_msg = socket.recv()

        msg = Message.from_bytes(raw_msg)

        # EASY OPTION
        # if msg type PRICE_REQUEST
        # -> send price data
        # if msg type DATA/SENSOR_READIN
        # record / send ACK

        # keep a list of msg ids to not process msg twice. do ACK though

        if random() < 0.2:
            socket.send_string("")
            print(f"didn't ack {msg}")
            continue

        # if random() < 0.1:
        #     print(recvd)


        print(f"ack: {msg.id}")

        resp = Message(type=MessageType.ACK, _id=msg.id, sender="server")

        # build response
        socket.send(resp.construct_msg(), zmq.NOBLOCK)

        # just check that we don't get duplicates
        # if not msg['id'] in recvd:
        #     recvd[msg['id']] = 1
        # else:
        #     recvd[msg['id']] += 1
