from Point import *
import math
from Line import *
from bresenham import bresenham
import numpy as np
import random

#LARGO DEL RAYO!!!!
def drawRayOfLight(pixeles, imgRef, puntoActual, puntoFuente, pintados, intensidadesDePixeles, colores, colorDeLaLuz, esReflejo, largoTotal, esMirror, paredCercana):
    trazoPixelesPorPintar = list(bresenham(int(puntoFuente.x),int(puntoFuente.y),int(puntoActual.x),int(puntoActual.y)))

    if not(esReflejo):
        drawRayOfLightLuzPrincipal(trazoPixelesPorPintar, pixeles, imgRef, puntoActual, puntoFuente, pintados, intensidadesDePixeles, colores, colorDeLaLuz, largoTotal, paredCercana)
    else:
        drawRayOfLightLuzReflejos(trazoPixelesPorPintar, pixeles, imgRef, puntoActual, puntoFuente, pintados, intensidadesDePixeles, colores, colorDeLaLuz, largoTotal, esMirror, paredCercana)

def drawRayOfLightLuzPrincipal(trazoPixelesPorPintar, pixeles, imgRef, puntoActual, puntoFuente, pintados, intensidadesDePixeles, colores, colorDeLaLuz, largoTotal, paredCercana):
    for pixelAct in (trazoPixelesPorPintar):
        x=pixelAct[0]
        y=pixelAct[1]
        puntoDestinoAct = Point(x, y)

        if (int(x) >= 0 and int(x) <=499 and int(y) >= 0 and int(y) <=499):
            intensidadPasada = (intensidadesDePixeles[int(x)][int(y)])
            largoDelRayo = puntoFuente.distanciaEntreDosPuntos(puntoDestinoAct)

            #INTENSIDAD:
            intensidad= (1-(largoDelRayo/500))**2
            intensidadTemp= intensidadPasada + intensidad

            if (intensidadTemp>0.8):
                intensidadTemp = 0.8

            #COLOREAMOS SI SE PUEDE:
            if (pintados[int(x)][int(y)][0]):
                continue

            if (intensidadTemp >= intensidadPasada):
                #INTENSIDAD
                pixeles[int(x)][int(y)] = imgRef[int(y)][int(x)][:3]*intensidadTemp
                pintados[int(x)][int(y)][0] = True
                intensidadesDePixeles[int(x)][int(y)] = intensidadTemp

                if (colores[int(x)][int(y)] == [0,0,0]):
                    #PRIMERA VEZ QUE PINTA
                    for i in range(0,3):
                        pixeles[int(x)][int(y)][i] *= colorDeLaLuz[i]/255

                    colores[int(x)][int(y)] = [colorDeLaLuz[0],colorDeLaLuz[1], colorDeLaLuz[2]]
                else:

                    nuevoColor = get_color (colores[int(x)][int(y)], colorDeLaLuz)
                    for i in range(0,3):
                        pixeles[int(x)][int(y)][i] *= nuevoColor[i]/255

                    colores[int(x)][int(y)] = [nuevoColor[0],nuevoColor[1], nuevoColor[2]]

def drawRayOfLightLuzReflejos(trazoPixelesPorPintar, pixeles, imgRef, puntoActual, puntoFuente, pintados, intensidadesDePixeles, colores, colorDeLaLuz, largoTotal, esMirror, paredCercana):
    if (esMirror):
        drawRayOfLightLuzReflejoEspejo(trazoPixelesPorPintar, pixeles, imgRef, puntoActual, puntoFuente, pintados, intensidadesDePixeles, colores, colorDeLaLuz, largoTotal, paredCercana)
    else:
        drawRayOfLightLuzReflejoPared(trazoPixelesPorPintar, pixeles, imgRef, puntoActual, puntoFuente, pintados, intensidadesDePixeles, colores, colorDeLaLuz, largoTotal, paredCercana)


def drawRayOfLightLuzReflejoPared(trazoPixelesPorPintar, pixeles, imgRef, puntoActual, puntoFuente, pintados, intensidadesDePixeles, colores, colorDeLaLuz, largoTotal, paredCercana):
    for pixelAct in (trazoPixelesPorPintar):
        x=pixelAct[0]
        y=pixelAct[1]
        puntoDestinoAct = Point(x, y)
        
        if (int(x) >= 0 and int(x) <=499 and int(y) >= 0 and int(y) <=499):
            intensidadPasada = (intensidadesDePixeles[int(x)][int(y)])
            largoDelRayo = puntoFuente.distanciaEntreDosPuntos(puntoDestinoAct)


            largoDelRayo += largoTotal
            intensidad= (1-(largoDelRayo/707))**2
            intensidadTemp = intensidadPasada + intensidad

            if (intensidadTemp>0.6):
                intensidadTemp = 0.6

            if (intensidadTemp >= intensidadPasada):

                pixeles[int(x)][int(y)] = imgRef[int(y)][int(x)][:3]*intensidadTemp
                intensidadesDePixeles[int(x)][int(y)] = intensidadTemp
                pintados[int(x)][int(y)][1] = True
                if (colores[int(x)][int(y)] == [0,0,0]):
                    nuevoColor = get_color (paredCercana.color, colorDeLaLuz)

                    #PRIMERA VEZ QUE PINTA
                    for i in range(0,3):
                        pixeles[int(x)][int(y)][i] *= nuevoColor[i]/255
                    colores[int(x)][int(y)] = [colorDeLaLuz[0],colorDeLaLuz[1], colorDeLaLuz[2]]
                else:
                    #TOCA COMBINAR COLORES E INTENSIDADES
                    nuevoColor = get_color (colores[int(x)][int(y)], colorDeLaLuz)
                    nuevoColor = get_color (nuevoColor, paredCercana.color)
                    for i in range(0,3):
                        pixeles[int(x)][int(y)][i] *= nuevoColor[i]/255
                    colores[int(x)][int(y)] = [nuevoColor[0],nuevoColor[1], nuevoColor[2]]


def drawRayOfLightLuzReflejoEspejo(trazoPixelesPorPintar, pixeles, imgRef, puntoActual, puntoFuente, pintados, intensidadesDePixeles, colores, colorDeLaLuz, largoTotal, paredCercana):
    for pixelAct in (trazoPixelesPorPintar):
        x=pixelAct[0]
        y=pixelAct[1]

        intensidadTemp = 0.9
        #INTENSIDAD
        pixeles[int(x)][int(y)] = imgRef[int(y)][int(x)][:3]*intensidadTemp

        #COLOR
        nuevoColor = get_color (colores[int(x)][int(y)], colorDeLaLuz)

        for i in range(0,3):
            pixeles[int(x)][int(y)][i] *= nuevoColor[i]/255

        #REGISTRO
        pintados[int(x)][int(y)][1] = True
        intensidadesDePixeles[int(x)][int(y)] = intensidadTemp
        colores[int(x)][int(y)] = [nuevoColor[0],nuevoColor[1], nuevoColor[2]]

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
            angulo = random.uniform (271,449)
        else:
            #RAYO VIENE DE LA IZQUIERDA
            angulo = random.uniform (91,269)

    puntoDestino = Point(puntoInterseccion.x + math.cos(math.radians(angulo))*largoRayo, puntoInterseccion.y + math.sin(math.radians(angulo))*largoRayo)
    return puntoDestino
