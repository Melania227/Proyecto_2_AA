from Point import *
import math
from Line import *
from bresenham import bresenham
import numpy as np 
import random

def drawRayOfLight(screen, pixeles, imgRef, intensidad, puntoActual, fuenteLuz, pintados):
    trazoPixelesPorPintar = list(bresenham(int(fuenteLuz.x),int(fuenteLuz.y),int(puntoActual.x),int(puntoActual.y)))
    totalAPintar = 250
    rango = totalAPintar//12
    contador=0

    for i in range (len(trazoPixelesPorPintar)):
        if (contador==rango):
            contador=0
            if (intensidad >= 0.2):
                intensidad = intensidad - 0.1
        contador += 1

        if (intensidad>0.9):
            intensidad = 0.9
        if (intensidad<0.1):
            intensidad = 0.1

        if (int(trazoPixelesPorPintar[i][0]) >= 0 and int(trazoPixelesPorPintar[i][0]) <=499 and int(trazoPixelesPorPintar[i][1]) >= 0 and int(trazoPixelesPorPintar[i][1]) <=499):
            if(pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][0] == 0 and pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][1] == 0 and pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][2] == 0):
                pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])] = imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][:3]*intensidad
                pintados[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])]+=[fuenteLuz]

            else:
                if (imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][0] != 0):
                    intensidadPasada =  pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][0] / imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][0]
                else:
                    intensidadPasada = 0.2
                intensidadNueva = intensidad + intensidadPasada

                if not (intensidad < intensidadPasada):
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
def espejos(lineaLuzPunto, interseccion):    
    #hay que redireccionar el rayo
    lineaLuzPunto.inicio.y = (interseccion.y-lineaLuzPunto.inicio.y)+interseccion.y
    lineaLuzPunto.final = interseccion
    #En este punto no interseca con un espejo
    return lineaLuzPunto

def paredesRecursivo(rayoOriginal, puntoInterseccion, wall):
    largoRayo = puntoInterseccion.distanciaEntreDosPuntos(rayoOriginal.final)

    #HORIZONTAL
    if (wall.pos=="H1"):
        #RAYO VIENE DE ABAJO
        angulo = random.uniform (181,359)
    elif (wall.pos=="H2"):
        #RAYO VIENE DE ARRIBA
        angulo = random.uniform (1,179)
    #VERTICAL
    elif (wall.pos=="V1"):
        angulo = random.uniform (91,269)
    elif (wall.pos=="V2"):
        #RAYO VIENE DE LA IZQUIERDA
        angulo = random.uniform (271,449)
    else:
        if (rayoOriginal.inicio.x > puntoInterseccion.x):
            angulo = random.uniform (91,269)
        else:
            #RAYO VIENE DE LA IZQUIERDA
            angulo = random.uniform (271,449)

    puntoDestino = Point(puntoInterseccion.x + math.cos(math.radians(angulo))*largoRayo, puntoInterseccion.y + math.sin(math.radians(angulo))*largoRayo)
    return puntoDestino
