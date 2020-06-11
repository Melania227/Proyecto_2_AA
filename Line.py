from Point import *
import pygame


class Line:

    inicio = Point (0,0)
    final = Point (0,0)

    def __init__(self, x1,y1,x2,y2):
        self.inicio = Point (x1,y1)
        self.final = Point (x2,y2)

    def linesIntersection(self, other):
        x1 = self.inicio.x
        y1 = self.inicio.y
        x2 = self.final.x
        y2 = self.final.y
        x3 = other.inicio.x
        y3 = other.inicio.y
        x4 = other.final.x
        y4 = other.final.y
        denominador = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if (denominador != 0):
            t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / denominador
            u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / denominador

            if (0.0<t<1.0 and 0.0<u<1.0):
                xInterseccion = x1 + t*(x2-x1)
                yInterseccion = y1 + t*(y2-y1)
                return Point (xInterseccion,yInterseccion)

        return -1.0

    def lineIntersectOrNot(self, other):
        x1 = self.inicio.x
        y1 = self.inicio.y
        x2 = self.final.x
        y2 = self.final.y
        x3 = other.inicio.x
        y3 = other.inicio.y
        x4 = other.final.x
        y4 = other.final.y
        denominador = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if (denominador != 0):
            t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / denominador
            u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / denominador

            if (0.0<t<1.0 and 0.0<u<1.0):
                return True

        return False

    def draw(self, screen):
        pygame.draw.line(screen,(255,200,164),(self.inicio.x, self.inicio.y),(self.final.x, self.final.y),3)
