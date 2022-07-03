from datetime import datetime
from os import path, mkdir

import shelve
import logging

from common.message import Message

def ts():
    return datetime.now().timestamp()


class MessageQueue:
    def __init__(self, garage_name: str):
        if not path.exists("_tmp"):
            mkdir("_tmp")

        self.queue = shelve.open(path.join("_tmp", garage_name))

    def enqueue(self, msg: Message):
        self.queue[msg.id] = {"ts": ts(),
                              "msg": msg}
        logging.info(f"remaining msgs in queue: {len(self.queue)}")

    def dequeue(self, id: str):
        return self.queue.pop(id)

    def retrieve(self) -> Message | None:
        keys = list(self.queue.keys())
        for key in keys:
            entry = self.queue.get(key)
            # only give me something that hasn't been sent in 2 seconds
            if ts() - entry["ts"] > 2:
                entry["ts"] = ts()
                return entry["msg"]

    def sync(self):
        self.queue.sync()

    def __len__(self):
        return len(self.queue)
