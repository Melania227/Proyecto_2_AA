from Line import *
import pygame


class Bound:

    linea = Line(0,0,0,0)
    pos = "none"
    esWall = True
    color = (255,255,255)

    def __init__(self, x1,y1,x2,y2, wall, color):
        self.linea = Line (x1,y1,x2,y2)
        self.esWall = wall
        self.color = color

    def draw(self, screen, color1, color2, color3):
        pygame.draw.line(screen,(color1, color2, color3),(self.linea.inicio.x, self.linea.inicio.y),(self.linea.final.x, self.linea.final.y),2)

    def __str__(self):
        return str(self.linea)
