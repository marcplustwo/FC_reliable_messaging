from typing import List
from random import random


class Sensor:
    def __init__(self, range: List[int]):
        # initialize data range
        self.range = range

    def read(self) -> int:
        # random data in range
        return random() * (self.range[1] - self.range[0]) + self.range[0]
