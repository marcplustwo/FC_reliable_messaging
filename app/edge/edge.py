from time import sleep
from app.edge.simulated_sensor.parking_garage import ParkingGarage, Sensor
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


def simulate_parking_garage():
    parking_garage = ParkingGarage(id = 1)

    parking_garage.start()


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
    sensor_thread = threading.Thread(target=simulate_parking_garage, args=[sensor, 1])
    sensor_thread.start()

    while True:
        # at a regular interval REQUEST occupancy info from server
        # add to message queue: REQUEST msg (A1 Type 1)

        # every 30 seconds:
        # call parking_garage.cars_recently_left() and make one message (for billing purposes)
        # add to message queue: CAR BILLING LIST (A1 Type 2)

        msg_keys = list(msg_queue.keys())
        if len(msg_keys) == 0:
            continue

        # send oldest message first (ULIDs) are sortable by time
        msg_keys.sort()
        msg = msg_queue[msg_keys[0]]

        print(f"sending message: {msg.id}")
        send(msg)

        print(f"remaining: {len(msg_queue)}")
