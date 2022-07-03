from datetime import datetime
from common.message import Message


def ts():
    return datetime.now().timestamp()


class MessageQueue:
    def __init__(self):
        self.queue = dict()

    def enqueue(self, msg: Message):
        self.queue[msg.id] = {"ts": ts(),
                              "msg": msg}

    def dequeue(self, id: str):
        msg = self.queue[id]
        del self.queue[id]
        return msg

    def retrieve(self) -> Message | None:
        keys = list(self.queue.keys())
        for key in keys:
            entry = self.queue[key]
            # only give me something that hasn't been sent in 2 seconds
            if ts() - entry["ts"] > 2:
                entry["ts"] = ts()
                return entry["msg"]

    def __len__(self):
        return len(self.queue)
