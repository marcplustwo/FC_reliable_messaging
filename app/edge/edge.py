from concurrent.futures import thread
from enum import Enum
from time import sleep
from sensor.sensor import Sensor
import zmq
import queue
import threading
import json
from ulid import ULID


class MessageType(Enum):
    READING = 0
    ACK = 2


class Message:
    def __init__(self, payload: str, type: MessageType):
        self.id = str(ULID())

        self.payload = payload
        self.type = type

    def construct_msg(self):
        # use json for prototype, ideally switch to protobuf for performance reasons
        # however, this is python so it doesn't matter here
        return json.dumps({
            "payload": self.payload,
            "id": self.id,
        }, ensure_ascii=True).encode("ascii")


msg_queue = dict()


# init cloud server
context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.REQ_RELAXED, 1)
socket.connect("tcp://localhost:5555")


# init sensors
sensor = Sensor([18, 24])


def read_sensor(sensor: Sensor, interval_seconds: int = 5):
    # loop:
    #   read sensors
    #   send data (put into message queue)
    while True:
        reading = sensor.read()

        # make message
        msg = Message(payload=str(reading), type=MessageType.READING)

        # add to queue
        msg_queue[msg.id] = msg
        sleep(interval_seconds)


sensor_thread = threading.Thread(target=read_sensor, args=[sensor, 1])
sensor_thread.start()


def send(msg: Message):
    global socket
    socket.send(msg.construct_msg())

    # rep = socket.recv_string(zmq.NOBLOCK)
    rep = socket.recv_string()
    print(f"rep: {rep}")
    try:
        del msg_queue[rep]
    except KeyError:
        pass


while True:
    msg_keys = list(msg_queue.keys())
    if len(msg_keys) == 0:
        continue

    # send oldest message first (ULIDs) are sortable by time
    msg_keys.sort()
    msg = msg_queue[msg_keys[0]]

    print(f"sending message: {msg.id}")
    send(msg)

    print(f"remaining: {len(msg_queue)}")
