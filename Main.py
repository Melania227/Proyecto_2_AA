import numpy
import pygame
import random
from PIL import Image
from Point import *
import math
import threading
from Bound import *
from Line import *
from RayOperations import *
from Light import *
import time


def pointLauncher(surface, num):
    posWall(surface)

    intensidades = []
    for l in range (500):
        fila = []
        for m in range (500):
            fila+=[0]
        intensidades += [fila]

    colores = []
    for l in range (500):
        fila = []
        for m in range (500):
            fila+=[[0,0,0]]
        colores += [fila]

    #for wall in walls:
    #   wall.draw(surface,255,255,255)
    #pygame.draw.circle(surface, (255,255,255), [fuentesDeLuz[0].x,fuentesDeLuz[0].y], 5)

    n=3600
    for luz in fuentesDeLuz:

        pixelesPintados = []
        for l in range (500):
            fila = []
            for m in range (500):
                fila+=[[False, False]]
            pixelesPintados += [fila]

        for i in range (n):
            destino = Point(luz.fuente.x + math.cos(math.radians(i/10))*300, luz.fuente.y + math.sin(math.radians(i/10))*300)

            '''if(destino.x<0):
                destino.x = 0
            if(destino.x>499):
                destino.x = 499
            if(destino.y<0):
                destino.y = 0
            if(destino.y>499):
                destino.y =499'''

            lineaLuzAPunto = Line (luz.fuente.x,luz.fuente.y,destino.x,destino.y)
            pathTracer (lineaLuzAPunto, luz.fuente, destino,surface, 1, pixelesPintados, intensidades, colores, luz.color, False, 0, False, walls[0])

def posWall(surface):
    n=45
    for light in fuentesDeLuz:
        for i in range (n):
            vaHacia = Point(light.fuente.x + math.cos(math.radians(i*85))*1000, light.fuente.y + math.sin(math.radians(i*85))*1000)
            rayo = Line (light.fuente.x,light.fuente.y,vaHacia.x,vaHacia.y)

            for wall in walls:
                if wall.esWall:
                    if  (rayo.lineIntersectOrNot(wall.linea)):
                        puntoInterseccion = rayo.linesIntersection(wall.linea)
                        if (light.fuente.distanciaEntreDosPuntos(puntoInterseccion)<light.fuente.distanciaEntreDosPuntos(vaHacia)):
                            vaHacia = puntoInterseccion
                            wallD=wall
                elif(wall.pos=="none"):
                    wallD=wall
                    if(wall.linea.inicio.x==wall.linea.final.x):
                        wall.pos="V"
                    else:
                        wall.pos="H"

            if wallD.esWall:
                if(wallD.linea.inicio.y == wallD.linea.final.y):
                    if (rayo.inicio.y < wallD.linea.inicio.y):
                        wallD.pos="H1"
                    else:
                        wallD.pos="H2"
                else:
                    if (rayo.inicio.x < wallD.linea.inicio.x):
                        if(wallD.pos!="V2" and wallD.pos!="M"):
                            wallD.pos="V1"
                        else:
                            wallD.pos="M"
                    else:
                        if(wallD.pos!="V1" and wallD.pos!="M"):
                            wallD.pos="V2"
                        else:
                            wallD.pos="M"


def pathTracer (rayo, puntoFuente, puntoDestino, surface, intensidad, pixelesPintados, intensidadesDePixeles, colores, colorDeLaLuz, esReflejo, distanciaTotal, esMirror, paredCercana):
    interseca = False
    mirror = False
    for wall in walls:
        if  (rayo.lineIntersectOrNot(wall.linea)):
            if wall.esWall:
                puntoInterseccion = rayo.linesIntersection(wall.linea)
                #Prueba si el punto de interseccion actual es el más cercano a la fuente de luz.
                if (puntoFuente.distanciaEntreDosPuntos(puntoInterseccion)<puntoFuente.distanciaEntreDosPuntos(puntoDestino)):
                    puntoDestino = puntoInterseccion
                    interseca = True
                    boundCercano = wall
            else:
               if  (rayo.lineIntersectOrNot(wall.linea)):
                    if puntoFuente.distanciaEntreDosPuntos(puntoDestino)>puntoFuente.distanciaEntreDosPuntos(rayo.linesIntersection(wall.linea)):
                        mirror = True
                        iT = rayo.linesIntersection(wall.linea)
                        espejo=wall.pos
                        boundEspejo = wall

    if (interseca):
        distanciaTotal += rayo.inicio.distanciaEntreDosPuntos(rayo.final)
        nuevoPuntoDestino = paredesRecursivo(rayo, puntoDestino, boundCercano)
        nuevoRayo = Line (puntoDestino.x, puntoDestino.y, nuevoPuntoDestino.x, nuevoPuntoDestino.y)
        pathTracer (nuevoRayo, puntoDestino, nuevoPuntoDestino, surface, 1, pixelesPintados, intensidadesDePixeles, colores, colorDeLaLuz, True, distanciaTotal, False, boundCercano)

    if (mirror):
        res = mirrorFuncion(rayo, iT, espejo)
        pathTracer (res[0], res[0].inicio, res[0].final, surface, 1, pixelesPintados, intensidadesDePixeles, colores, colorDeLaLuz, True, res[1], True, boundEspejo)

    drawRayOfLight(px, ref, puntoDestino, puntoFuente, pixelesPintados, intensidadesDePixeles, colores, colorDeLaLuz, esReflejo, distanciaTotal, esMirror, paredCercana)

def mirrorFuncion(rayo, iT, espejo):

    distanciaTotal = rayo.inicio.distanciaEntreDosPuntos(rayo.final)
    if(espejo=="H"):
        if(rayo.final.y<iT.y):
            rayoMirror = Line ( iT.x, iT.y, rayo.final.x, (iT.y-rayo.final.y)+iT.y)
        else:
            rayoMirror = Line ( iT.x, iT.y, rayo.final.x, iT.y-(rayo.final.y-iT.y))
    else:
        if(rayo.final.x<iT.x):
            rayoMirror = Line ( iT.x, iT.y,  (iT.x-rayo.final.x)+iT.x, rayo.final.y)
        else:
            rayoMirror = Line ( iT.x, iT.y,  iT.x-(rayo.final.x-iT.x), rayo.final.y)

    return [rayoMirror,distanciaTotal]

def getFrame():
    #Ajusta los pixeles actualizados para colocar la imagen
    pixels = numpy.roll(px,(1,2),(0,1))
    return pixels

#CREACIÓN DEL CONTENEDOR DE LA IMAGEN
i = Image.new("RGB", (500, 500), (0, 0, 0) )
px = numpy.array(i)

#CARGA DE IMAGEN
#im_file = Image.open("BackWhite.png") VERSIÓN FONDO BLANCO
im_file = Image.open("Back.png")
ref = numpy.array(im_file)

#FUENTES DE LUZ
fuentesDeLuz =[Light(128,133, (153,0,102)),Light(220,448, (0,0,150)), Light(373,224, (255,255,255))]

#PAREDES, su orden afecta funcionamiento
walls = [Bound(14, 23, 173, 23, True, (96,57,34)), #H2
        Bound(14, 23, 14, 256, True, (96,57,34)), #V2
        Bound(14, 256, 77, 256, True, (96,57,34)), #H1
        Bound(77, 256, 77,483, True, (96,57,34)),  #V2
        Bound(77,483, 362, 483, True, (96,57,34)), #H1
        Bound(362, 333, 362, 483, True, (96,57,34)), #V1
        Bound(362, 333, 488, 333, True, (96,57,34)), #H1
        Bound(488, 23, 488, 333, True, (96,57,34)), #V1
        Bound(267, 23, 488, 23, True, (96,57,34)), #H2
        Bound(267, 23, 267, 248, True, (96,57,34)), #V2
        Bound(267, 248, 267, 369, True, (96,57,34)), #M
        Bound(173, 248, 173,369 , True, (96,57,34)), #M
        Bound(173, 23, 173, 249, True, (96,57,34)), #V1
        Bound(173, 248, 267, 248, True, (96,57,34)), #H2
        Bound(303, 146, 325, 146, False, (255,255,255))]  #Mirror


imagenPixelesNumpy=getFrame()
surface = pygame.surfarray.make_surface(imagenPixelesNumpy)

#DEFINCIÓN DE UN THREAD:
t = threading.Thread(target = pointLauncher, args=(surface,0)) 
t.setDaemon(True)
t.start() #Con t.join() se puede matar el thread pero no es buena idea si no se paran el resto de cosas.

def pathTracingInicializator(done, screen, border):
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((255, 255, 255))

        imagenPixelesNumpy=getFrame()
        surface = pygame.surfarray.make_surface(imagenPixelesNumpy)

        screen.blit(surface, (border, border))

        pygame.display.flip()

def main ():
    h,w=550,550
    border=50
    pygame.init()
    screen = pygame.display.set_mode((w+(2*border), h+(2*border)))
    pygame.display.set_caption("2D Path Tracing by Melania & Paola")
    done = False
    #Tomamos el tiempo de duración AHORITA TOMA DESDE QUE CORRE HASTA QUE SOY A LA X *******
    iniciarTimer=time.time()
    pathTracingInicializator(done, screen, border)
    finalizarTimer = time.time() - iniciarTimer
    print (finalizarTimer)

main()