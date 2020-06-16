from Point import *
import math
from Line import *
from bresenham import bresenham
import numpy as np 
import random

def drawRayOfLight(screen, pixeles, imgRef, intensidad, puntoActual, fuenteLuz, pintados, sonReflejo):
    trazoPixelesPorPintar = list(bresenham(int(puntoActual.x),int(puntoActual.y),int(fuenteLuz.x),int(fuenteLuz.y)))
    totalAPintar = 350
    rango = totalAPintar//12
    contador=0

    for i in range (len(trazoPixelesPorPintar)-1,0, -1):
        if (contador==rango):
            contador=0
            if (intensidad >= 0.2):
                intensidad = intensidad - 0.1
        contador += 1

        if (int(trazoPixelesPorPintar[i][0]) >= 0 and int(trazoPixelesPorPintar[i][0]) <=499 and int(trazoPixelesPorPintar[i][1]) >= 0 and int(trazoPixelesPorPintar[i][1]) <=499):
            if(pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][0] == 0 and pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][1] == 0 and pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][2] == 0):
                pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])] = imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][:3]*intensidad
                pintados[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])]+=[fuenteLuz]

            else:
                if (fuenteLuz in pintados[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])] and not(sonReflejo)):
                    continue

                if (imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][0] != 0):
                    intensidadPasada =  pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][0] / imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][0]
                else:
                    intensidadPasada = 0.2
                intensidadNueva = intensidad + intensidadPasada

                #if (intensidad < intensidadPasada):
                #   intensidadNueva = intensidadPasada + 0.05
                if (intensidadNueva >= intensidadPasada):
                    if (intensidadNueva>0.9):
                        intensidadNueva = 0.9
                    pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])] = imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][:3]*intensidadNueva
                    pintados[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])]+=[fuenteLuz]
        
#ESTO COMBINA LOS COLORES DE DOS PIXELES, EL ACTUAL Y EL DE REFERENCIA:
#        if(pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][0] == 0 and pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][1] == 0 and pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][2] == 0):
#            pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])] = imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][:3]*intensidad
#        else:
#            pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])] = get_color(pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])], imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][:3]*intensidad)
         
def get_color(colorRGBA1, colorRGBA2):
    red   = (colorRGBA1[0] + colorRGBA2[0]) / 2
    green = (colorRGBA1[1] + colorRGBA2[1]) / 2
    blue  = (colorRGBA1[2] + colorRGBA2[2]) / 2
    return [int(red), int(green), int(blue)]

#pensado en que solo hay un espejo
def espejos(lineaLuzPunto, interseccion, walls, mirrors, surface, px, ref,pintados):    
    #hay que redireccionar el rayo
    lineaLuzPunto.inicio.y = (interseccion.y-lineaLuzPunto.inicio.y)+interseccion.y
    lineaLuzPunto.final = interseccion
    #En este punto no interseca con un espejo

    interseca = False
    for wall in walls:
        if(lineaLuzPunto.lineIntersectOrNot(wall)):
            puntoInterseccion = lineaLuzPunto.linesIntersection(wall)
            interseca = True
            if (lineaLuzPunto.final.distanciaEntreDosPuntos(puntoInterseccion)<lineaLuzPunto.final.distanciaEntreDosPuntos(lineaLuzPunto.inicio)): 
                lineaLuzPunto.inicio = puntoInterseccion
    if interseca:
        paredesRecursivo(lineaLuzPunto, lineaLuzPunto.inicio, walls, mirrors, surface, px, ref,pintados) 

    drawRayOfLight(surface, px, ref, 0.9 , lineaLuzPunto.inicio, lineaLuzPunto.final,pintados,True)

def paredesRecursivo(rayoOriginal, puntoInterseccion, walls, mirrors, surface, px, ref,pintados):
    largoRayo = puntoInterseccion.distanciaEntreDosPuntos(rayoOriginal.inicio)
    if (rayoOriginal.inicio.y == puntoInterseccion.y):
        #HORIZONTAL
        if (rayoOriginal.inicio.y > puntoInterseccion.y):
            #RAYO VIENE DE ABAJO
            angulo = random.uniform (0,180)
            puntoDestino = Point(puntoInterseccion.x + math.cos(math.radians(angulo))*largoRayo, puntoInterseccion.y + math.sin(math.radians(angulo))*largoRayo)
        else:
            #RAYO VIENE DE ARRIBA
            angulo = random.uniform (180,360)
            puntoDestino = Point(puntoInterseccion.x + math.cos(math.radians(angulo))*largoRayo, puntoInterseccion.y + math.sin(math.radians(angulo))*largoRayo)
    else:
        #VERTICAL
        if (rayoOriginal.inicio.x > puntoInterseccion.x):
            angulo = random.uniform (90,270)
            puntoDestino = Point(puntoInterseccion.x + math.cos(math.radians(angulo))*largoRayo, puntoInterseccion.y + math.sin(math.radians(angulo))*largoRayo)
        else:
            #RAYO VIENE DE LA IZQUIERDA
            angulo = random.uniform (270,450)
            puntoDestino = Point(puntoInterseccion.x + math.cos(math.radians(angulo))*largoRayo, puntoInterseccion.y + math.sin(math.radians(angulo))*largoRayo)
    
    repeticiones = rayoOriginal.inicio.distanciaEntreDosPuntos(rayoOriginal.final) // (350//15)
    intensidadDePartida= 1-(repeticiones/10)

    return puntoDestino
