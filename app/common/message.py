from curses import raw
from enum import Enum
from typing import Dict
from ulid import ULID
import json


class MessageType(str, Enum):
    REQ = "req"
    ACK = "ack"


class PayloadType(str, Enum):
    CAR_BILLING = "car_billing"
    OCCUPANCY = "occupancy"
    OCCUPANCY_REQUEST = "occupancy_request"


class Message:
    def from_bytes(bytes: bytes):
        try:
            raw_msg = json.loads(bytes)
            return Message(payload=raw_msg["payload"],
                           type=MessageType(raw_msg["type"]),
                           _id=raw_msg["id"],
                           sender=raw_msg["sender"])
        except:
            print("failed to serialize msg")

    def __init__(self, type: MessageType, sender: str, payload: Dict = None, payload_type: PayloadType = None, _id: str = None):
        self.last_tried = None
        self.id = _id or str(ULID())
        self.payload = payload
        self.payload_type = payload_type
        self.type = type
        self.sender = sender

    def construct_msg(self):
        # use json for prototype, ideally switch to protobuf for performance reasons
        # however, this is python so it doesn't really matter
        return json.dumps({
            "id": self.id,
            "type": self.type,
            "payload": self.payload,
            "payload_type": self.payload_type,
            "sender": self.sender
        }).encode("ascii")

    def __str__(self):
        return str(self.construct_msg())
