from typing import List
from random import random


class ParkingGarage:
    def __init__(self, max_capacity: int):
        # initialize data range
        self.range = range

    def start_simulation(self):
        # start simulating cars coming in and out (keep track of them)
        self.cars_inside = []
        while True:
            # sleep for random time
            # probability of car event
            # car entering
            # car leaving
            # - get from list of cars_inside a random car
            pass

    def cars_recently_left(self) -> List:
        # polling based approach
        # -> empty queue
        pass

    def get_occupancy(self) -> int:
        return len(self.cars_inside)
