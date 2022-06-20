import zmq

# init message receiver
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")

# loop:
#   recv data
#   store data
#
#   (not every iteration but regularly e.g. timer):
#     aggregate data and send out via message queue

while True:
  msg = socket.recv()
  print(f"receeived: {msg}")
