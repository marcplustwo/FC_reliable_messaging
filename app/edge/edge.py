from time import sleep
from edge.sensor.sensor import Sensor
from common.message import Message, MessageType
import zmq
import threading


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


def run_edge():
    sensor_thread = threading.Thread(target=read_sensor, args=[sensor, 1])
    sensor_thread.start()

    while True:
        # at a regular interval REQUEST price info from server
        # hey, it's been 5 seconds, I need a new price update


        msg_keys = list(msg_queue.keys())
        if len(msg_keys) == 0:
            continue

        # send oldest message first (ULIDs) are sortable by time
        msg_keys.sort()
        msg = msg_queue[msg_keys[0]]

        print(f"sending message: {msg.id}")
        send(msg)

        print(f"remaining: {len(msg_queue)}")
