from enum import Enum
from ulid import ULID
import json


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
