import math
from Point import *
class Light:

    fuente = Point(0,0)
    color = (255,255,255)

    def __init__(self, x, y, color):
        self.fuente = Point (x,y)
        self.color = color