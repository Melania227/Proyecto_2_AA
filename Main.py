import numpy as np
import pygame
import random
from PIL import Image
from Point import *
import math
import threading
from Bound import *
from Line import *
from RayOperations import *


def pointLauncher(surface, num):
    posWall(surface)
    
    pixelesPintados = []
    for l in range (500):
        fila = []
        for m in range (500):
            fila+=[[]]
        pixelesPintados += [fila]

    #for wall in walls:
    #   wall.draw(surface,255,255,255)
    #pygame.draw.circle(surface, (255,255,255), [fuentesDeLuz[0].x,fuentesDeLuz[0].y], 5)
    
    n=3600    
    
    for i in range (n):
        for luz in fuentesDeLuz:
            destino = Point(luz.x + math.cos(math.radians(i/10))*300, luz.y + math.sin(math.radians(i/10))*300)
            
            if(destino.x<0):
                destino.x = 0
            if(destino.x>499):
                destino.x = 499
            if(destino.y<0):
                destino.y = 0
            if(destino.y>499):
                destino.y =499

            lineaLuzAPunto = Line (luz.x,luz.y,destino.x,destino.y)
            pathTracer (lineaLuzAPunto, luz, destino,surface, 0.9, pixelesPintados)

def posWall(surface):
    n=45
    for light in fuentesDeLuz:
        for i in range (n):
            vaHacia = Point(light.x + math.cos(math.radians(i*85))*1000, light.y + math.sin(math.radians(i*85))*1000)
            if(vaHacia.x<0):
                vaHacia.x = 0
            if(vaHacia.x>499):
                vaHacia.x = 499
            if(vaHacia.y<0):
                vaHacia.y = 0
            if(vaHacia.y>499):
                vaHacia.y =499
            rayo = Line (light.x,light.y,vaHacia.x,vaHacia.y)

            for wall in walls:
                if  (rayo.lineIntersectOrNot(wall.linea)):
                    puntoInterseccion = rayo.linesIntersection(wall.linea)
                    if (light.distanciaEntreDosPuntos(puntoInterseccion)<light.distanciaEntreDosPuntos(vaHacia)):
                        vaHacia = puntoInterseccion
                        wallD=wall

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

def pathTracer (rayo, puntoFuente, puntoDestino, surface, intensidad, pixelesPintados):
    interseca = False
    for wall in walls:
        if  (rayo.lineIntersectOrNot(wall.linea)):
            puntoInterseccion = rayo.linesIntersection(wall.linea)
            #Prueba si el punto de interseccion actual es el más cercano a la fuente de luz.
            if (puntoFuente.distanciaEntreDosPuntos(puntoInterseccion)<puntoFuente.distanciaEntreDosPuntos(puntoDestino)):
                puntoDestino = puntoInterseccion
                interseca = True
                boundCercano = wall
    
    if (interseca):
        if (boundCercano.esWall):
            nuevoPuntoDestino = paredesRecursivo(rayo, puntoDestino, boundCercano)
            nuevoRayo = Line (puntoDestino.x, puntoDestino.y, nuevoPuntoDestino.x, nuevoPuntoDestino.y)
            #sacamos la intensidad de partida
            repeticiones = rayo.inicio.distanciaEntreDosPuntos(rayo.final) // (250//12)
            intensidadDePartida= 1-(repeticiones/10)
        else:
            pass
            nuevoRayo = espejos(rayo, puntoDestino) #NO FUNCIONA ESTA PICHA :C
            nuevoPuntoDestino = nuevoRayo.inicio
            intensidadDePartida = 1 
             #ARREGLAR LA INTENSIDAD!!!!
        pathTracer (nuevoRayo, puntoDestino, nuevoPuntoDestino, surface, intensidadDePartida, pixelesPintados)

    #pygame.draw.line(surface, (255,255,255), (int (puntoFuente.x),int (puntoFuente.y)), (int (puntoDestino.x),int (puntoDestino.y)))
    drawRayOfLight(surface, px, ref, intensidad, puntoDestino, puntoFuente, pixelesPintados)

def getFrame():
    # grabs the current image and returns it
    pixels = np.roll(px,(1,2),(0,1))
    return pixels


#pygame stuff
h,w=550,550
border=50
pygame.init()
screen = pygame.display.set_mode((w+(2*border), h+(2*border)))
pygame.display.set_caption("2D Raytracing")
done = False
clock = pygame.time.Clock()

#init random
random.seed()

#image setup
i = Image.new("RGB", (500, 500), (0, 0, 0) )
px = np.array(i)

#reference image for background color
im_file = Image.open("Back.png")
ref = np.array(im_file)

#light positions
fuentesDeLuz = [ Point(128,133), Point(373,224) , Point (220,448)]

#light color
light = np.array([1, 1, 0.75])

#warning, point order affects intersection test!!
walls = [Bound(14, 23, 173, 23, True), #H2
        Bound(14, 23, 14, 256, True ), #V2
        Bound(14, 256, 77, 256, True), #H1
        Bound(77, 256, 77,483, True),  #V2
        Bound(77,483, 362, 483, True), #H1
        Bound(362, 333, 362, 483, True), #V1
        Bound(362, 333, 488, 333, True), #H1
        Bound(488, 23, 488, 333, True), #V1
        Bound(267, 23, 488, 23, True), #H2
        Bound(267, 23, 267, 248, True), #V2
        Bound(267, 248, 267, 369, True), #M
        Bound(173, 248, 173,369 , True), #M
        Bound(173, 23, 173, 248, True), #V1
        Bound(173, 248, 267, 248, True) #H2]
        ]


npimage=getFrame()
surface = pygame.surfarray.make_surface(npimage)
#thread
t = threading.Thread(target = pointLauncher, args=(surface,0)) # f being the function that tells how the ball should move
t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
t.start()

#main loop
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        screen.fill((255, 255, 255))

        npimage=getFrame()
        surface = pygame.surfarray.make_surface(npimage)

        screen.blit(surface, (border, border))

        pygame.display.flip()
        clock.tick(60)
