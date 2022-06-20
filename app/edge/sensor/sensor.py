<<<<<<< HEAD
import random

class Sensor:
  def __init__(self):
    # initialize data range
    minTemp = random.uniform(0,15)  #unit °C
    maxTemp = random.uniform(20,40)
    # how to generate data
    temp = random.uniform(minTemp,maxTemp)
    pass

  def read(self):
    # random data
    
    #pass the generated temp to which queue?
    
    return 0

#kkkk

=======
from typing import List
from random import random


class Sensor:
    def __init__(self, range: List[int]):
        # initialize data range
        self.range = range

    def read(self) -> int:
        # random data in range
        return random() * (self.range[1] - self.range[0]) + self.range[0]
>>>>>>> 538b7e818d50c96e587b9bb56fd572aa958b16c6
