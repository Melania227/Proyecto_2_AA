import math
from Point import *
class Light:

    fuente = Point(0,0)
    color = (255,255,255)
    intensidad = 0.3

    def __init__(self, x, y, color, intensidad):
        self.fuente = Point (x,y)
        self.color = color
        self.intensidad = intensidad