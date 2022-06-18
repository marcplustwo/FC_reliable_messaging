from time import sleep
from sensor.sensor import Sensor
import zmq

# init sensors
sensor = Sensor([18, 24])

# init cloud server
context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.PUSH)
socket.connect("tcp://localhost:5555")


# loop:
#   read sensors
#   send data (put into message queue)
while True:
    val = sensor.read()
    socket.send_string(str(val))
    print(val)

    sleep(10)




# queue:
#   message event:
#   try to send
#   (try to resend)