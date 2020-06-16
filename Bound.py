from Line import *
import pygame


class Bound:

    linea = Line(0,0,0,0)
    wall = True

    def __init__(self, x1,y1,x2,y2, wall):
        self.linea = Line (x1,y1,x2,y2)
        self.wall = wall

    def draw(self, screen, color1, color2, color3):
        pygame.draw.line(screen,(color1, color2, color3),(self.linea.inicio.x, self.linea.inicio.y),(self.linea.final.x, self.linea.final.y),3)
