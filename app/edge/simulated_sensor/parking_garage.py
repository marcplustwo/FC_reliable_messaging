import random
import time
import shelve

from os import path, mkdir


class ParkingGarage:
    def __init__(self, garage_name: str):
        if not path.exists("_tmp"):
            mkdir("_tmp")

        # persist info about cars
        self.cars_inside = shelve.open(
            path.join("_tmp", f"{garage_name}_cars_inside"))

        # hacky, but also persist max_capacity
        if "max_capacity" not in self.cars_inside:
            self.cars_inside["max_capacity"] = random.randint(30, 150)

        self.max_capacity = self.cars_inside["max_capacity"]

    def start_simulation(self, eventcallback):
        print("cars inside:", [car if car != "max_capacity" else "" for car in self.cars_inside.keys()])

        while True:
            # sleep for random time
            time.sleep(random.randint(1, 4))

            # probability of car entering event - more likely when the garage is empty
            if random.random() <= 1 / (len(self.cars_inside) / self.max_capacity):
                # SENSOR 1: car entering
                if len(self.cars_inside) < self.max_capacity:
                    license_plate = self.generate_plate()
                    if license_plate in self.cars_inside:
                        continue
                    self.cars_inside[license_plate] = 0
                    print(f"SENSOR 1: car {license_plate} entered")


            if random.random() <= len(self.cars_inside) / self.max_capacity:
                if len(self.cars_inside) > 0:
                    # SENSOR 2: car leaving
                    leaving_car_key = random.choice(
                        list((self.cars_inside.keys())))
                    leaving_car_duration = self.cars_inside.pop(leaving_car_key)

                    print(f"SENSOR 2: car {leaving_car_key} left after {leaving_car_duration} mins")
                    eventcallback(leaving_car_key, leaving_car_duration)

            for car_key in self.cars_inside:
                if self.cars_inside[car_key] < 300:
                    self.cars_inside[car_key] += 1

    def get_occupancy(self) -> int:
        return len(self.cars_inside)

    def generate_plate(self) -> str:
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        nums = '0123456789'
        letters = ''
        numbers = ''
        for c in range(3):
            letters += random.choice(chars)
        for c in range(3):
            numbers += random.choice(nums)
        plate = letters + ' ' + numbers
        return plate
