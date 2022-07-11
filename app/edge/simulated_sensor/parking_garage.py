from operator import le
from typing import List
import random
from urllib.parse import MAX_CACHE_SIZE
import time

from numpy import gradient


class ParkingGarage:
    def __init__(self, id: int):
        # initialize data range
        self.id = id
        max_capacity = random.randint(30,150)
        self.max_capacity = max_capacity
        self.init_occu = random.randint(0, max_capacity)   
        #self.recently_left = {}                            # change format??

    def start_simulation(self, eventcallback):
        #initial status of cars inside
        self.cars_inside = {}
        for n in range(self.init_occu):
            license_plate = self.generate_plate()
            duration_minutes = random.randint(0,300)

            if license_plate in self.cars_inside:
                n-=1
                continue
            self.cars_inside[license_plate] = duration_minutes
        
        current_occu = self.init_occu
        # start simulating cars coming in and out (keep track of them)

        print("initial cars inside:", self.cars_inside)
        
        while True:
            # sleep for random time
            time.sleep(1)

            # probability of car event
            if random.random() <= 0.5: 
            # car entering
                if current_occu < self.max_capacity:
                    license_plate = self.generate_plate()
                    if license_plate in self.cars_inside:
                        continue
                    #print("car entering:", license_plate)
                    self.cars_inside[license_plate] = 0
                    current_occu += 1

            elif current_occu>0: 
            # car leaving
                leaving_car_key = random.choice(list((self.cars_inside.keys())))
                leaving_car_duration = self.cars_inside.pop(leaving_car_key)
                current_occu -= 1
                #print("car leaving:", leaving_car_key, " duration:", leaving_car_duration, "min")
                #save the car left, empty it after call cars_recently_left!
                #self.recently_left[leaving_car_key] = leaving_car_duration
                eventcallback(leaving_car_key,leaving_car_duration)

        #increase duration minutes (seconds) for each car
            for car_key in self.cars_inside:
                if self.cars_inside[car_key] < 300:
                    self.cars_inside[car_key] += 1
            

            #print("rectly left:", self.cars_recently_left())
            #print("cars inside after change:", self.cars_inside)
            #print("current occupancy:", self.get_occupancy(), "/ ", self.max_capacity)            
            #print("-------------------------")

    '''def cars_recently_left(self) -> list:               #每30s 要执行一遍/ event trigger??
        # polling based approach
        return self.recently_left                  #dictionary -> list??
        
        # -> empty queue   ----> edge operate!!!？？
        self.recently_left.clear()
    '''

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
        plate = letters +' '+ numbers
        return plate


#garage1 = ParkingGarage(1)
#garage1.start_simulation()