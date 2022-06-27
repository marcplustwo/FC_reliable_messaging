# Reliable Messaging for Fog Use Cases

## (Constructed) Use Case

## Reliable Messaging
We operate on a client-server model. There can be multiple clients that we calle edge nodes. They sent data to a server (in the cloud). Data is processed and aggregated. At regular intervals clients receive this aggregated data back.

Clients can fail or become unresponsive. The network does not guarantee order, timely delivery, or delivery at all.

We implement a reliable delivery mechanism.

### Algorithm
- put data in queue (at regular intervals)
  - mark as "NEW"
- send data that is not acknowledged
  - every x interval we take the messages (oldest first) from the queue and send it
  - mark as "AWAITING_ACK"

- server
  - receive
  - send ACK

- client
  - wait for ACK messages
  - delete ACK's messages from queue


(draw this type of diagram)
https://taotetek.wordpress.com/2011/02/02/python-multiprocessing-with-zeromq/

### MSG Types
READING
ACK
REQ

# responsibilities / use case
## edge
- count incoming / outgoing cars
- send to cloud
  - current occupancy/availability
  - when car left: send parking length to cloud

## cloud
- billing (send the bill to the customer) (it wouldn't actually do anything in our implementation)
  - we assume/pretend every car has an account with billing information linked
- occupancy report (how many parking spots available throughout the city)


# TODO
- multiple edge instances
  - we give parking lot id (new port)
- adapt for use case
  - simulate car sensor (at parking lot entrance)
    - random: come up with algorithm that meaningfully changes occupancy -> over time there is a trend of more cars going in (so that the price would actually change)
    - a bit later the trend would be for more cars to leave again
  - direction in/out (ou including length of stay [for billing]) + license plate + id of parking lot
  - remember cars that came in, so we can simulate them leaving again
- Implement Message abstraction for server as well
  - define Message types
    - client -> server
      - A1 DATA
      - B1 DATA_REQUEST (here: price request)
    - server -> client
      - A2 ACK
      - B2 ACK (with data)
  - define msg content types
    - A1
      - license plate
      - time stamp
      - direction (in/out)
    - B1
      - 
