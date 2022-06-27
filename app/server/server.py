import json
from random import random
import zmq


def run_server():
    # init message receiver
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    # socket.setsockopt(zmq.REQ_RELAXED, 1)
    socket.bind("tcp://*:5555")

    # loop:
    #   recv data
    #   store data
    #
    #   (not every iteration but regularly e.g. timer):
    #     aggregate data and send out via message queue
    recvd = dict()

    while True:
        msg = socket.recv()

        if random() < 0.2:
            socket.send_string("")
            print(f"didn't ack {msg}")
            continue

        # if random() < 0.1:
        #     print(recvd)

        print(f"ack: {msg}")
        msg = json.loads(msg)
        socket.send_string(f"{msg['id']}", zmq.NOBLOCK)

        # just check that we don't get duplicates
        if not msg['id'] in recvd:
            recvd[msg['id']] = 1
        else:
            recvd[msg['id']] += 1
