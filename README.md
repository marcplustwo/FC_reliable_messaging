# Reliable Messaging for Fog Use Cases

## (Constructed) Use Case

## Reliable Messaging
We operate on a client-server model. There can be multiple clients that we calle edge nodes. They sent data to a server (in the cloud). Data is processed and aggregated. At regular intervals clients receive this aggregated data back.

Clients can fail or become unresponsive. The network does not guarantee order, timely delivery, or delivery at all.

We implement a reliable delivery mechanism.

### Algorithm
- put data in queue (at regular intervals)
  - mark as "NEW"
- send data that is not acknowledged (take form queue)
  - every x interval we take the y first messages from the queue and send it
  - mark as "AWAITING_ACK"

- server
  - receive
  - wait for some time and collect messages
  - send ACK with a list of IDs

- client
  - wait for ACK messages
  - delete ACK's messages from queue


(draw this type of diagram)
https://taotetek.wordpress.com/2011/02/02/python-multiprocessing-with-zeromq/

### MSG Types
READING
ACK
REQ


