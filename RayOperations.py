from Point import *
import math
from Line import *
from bresenham import bresenham
import numpy as np
import random

def drawRayOfLight(screen, pixeles, imgRef, intensidad, puntoActual, puntoFuente, pintados, intensidadesDePixeles, colores, colorDeLaLuz, esReflejo, largoTotal):
    trazoPixelesPorPintar = list(bresenham(int(puntoFuente.x),int(puntoFuente.y),int(puntoActual.x),int(puntoActual.y)))

    for pixelAct in (trazoPixelesPorPintar):
        puntoDestinoAct = Point(pixelAct[0], pixelAct[1])

        if (int(pixelAct[0]) >= 0 and int(pixelAct[0]) <=499 and int(pixelAct[1]) >= 0 and int(pixelAct[1]) <=499):
            intensidadPasada = (intensidadesDePixeles[int(pixelAct[0])][int(pixelAct[1])])
            largoDelRayo = puntoFuente.distanciaEntreDosPuntos(puntoDestinoAct)

            #ES UN REFLEJO O NO?
            if not (esReflejo): #NO ES REFLEJO
                #INTENSIDAD:
                intensidad= (1-(largoDelRayo/500))**2
                intensidadTemp = intensidadPasada + intensidad
                if (intensidadTemp>1):
                    intensidadTemp = 1

                #COLOREAMOS SI SE PUEDE:
                if (puntoFuente == pintados[int(pixelAct[0])][int(pixelAct[1])][0]):
                    continue

                else:
                    if (colores[int(pixelAct[0])][int(pixelAct[1])] == [0,0,0]):
                        #PRIMERA VEZ QUE PINTA
                        if (intensidadTemp > intensidadPasada):
                            #INTENSIDAD
                            pixeles[int(pixelAct[0])][int(pixelAct[1])] = imgRef[int(pixelAct[1])][int(pixelAct[0])][:3]*intensidadTemp
                            #COLOR
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][0] *= colorDeLaLuz[0]/255
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][1] *= colorDeLaLuz[1]/255
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][2] *= colorDeLaLuz[2]/255
                            #REGISTRO
                            pintados[int(pixelAct[0])][int(pixelAct[1])][0] = puntoFuente
                            intensidadesDePixeles[int(pixelAct[0])][int(pixelAct[1])] = intensidadTemp
                            colores[int(pixelAct[0])][int(pixelAct[1])] = [colorDeLaLuz[0],colorDeLaLuz[1], colorDeLaLuz[2]]
                    else:
                        #TOCA COMBINAR COLORES E INTENSIDADES
                        if (intensidadTemp > intensidadPasada):
                            #INTENSIDAD
                            pixeles[int(pixelAct[0])][int(pixelAct[1])] = imgRef[int(pixelAct[1])][int(pixelAct[0])][:3]*intensidadTemp
                            #COLOR
                            nuevoColor = get_color (colores[int(pixelAct[0])][int(pixelAct[1])], colorDeLaLuz)
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][0] *= nuevoColor[0]/255
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][1] *= nuevoColor[1]/255
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][2] *= nuevoColor[2]/255
                            #REGISTRO
                            pintados[int(pixelAct[0])][int(pixelAct[1])][0] = puntoFuente
                            intensidadesDePixeles[int(pixelAct[0])][int(pixelAct[1])] = intensidadTemp
                            colores[int(pixelAct[0])][int(pixelAct[1])] = [nuevoColor[0],nuevoColor[1], nuevoColor[2]]


            else: #ES REFLEJO
                #INTENSIDAD:
                largoDelRayo += largoTotal
                intensidad= (1-(largoDelRayo/707))**2
                intensidadTemp = intensidadPasada + intensidad
                if (intensidadTemp>1):
                    intensidadTemp = 1
                
               #COLOREAMOS SI SE PUEDE:
                if (pintados[int(pixelAct[0])][int(pixelAct[1])][1]):
                    continue

                else:
                    if (colores[int(pixelAct[0])][int(pixelAct[1])] == [0,0,0]):
                        #PRIMERA VEZ QUE PINTA
                        if (intensidadTemp > intensidadPasada):
                            #INTENSIDAD
                            pixeles[int(pixelAct[0])][int(pixelAct[1])] = imgRef[int(pixelAct[1])][int(pixelAct[0])][:3]*intensidadTemp
                            #COLOR
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][0] *= colorDeLaLuz[0]/255
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][1] *= colorDeLaLuz[1]/255
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][2] *= colorDeLaLuz[2]/255
                            #REGISTRO
                            pintados[int(pixelAct[0])][int(pixelAct[1])][1] = True
                            intensidadesDePixeles[int(pixelAct[0])][int(pixelAct[1])] = intensidadTemp
                            colores[int(pixelAct[0])][int(pixelAct[1])] = [colorDeLaLuz[0],colorDeLaLuz[1], colorDeLaLuz[2]]
                    else:
                        #TOCA COMBINAR COLORES E INTENSIDADES
                        if (intensidadTemp > intensidadPasada):
                            #INTENSIDAD
                            pixeles[int(pixelAct[0])][int(pixelAct[1])] = imgRef[int(pixelAct[1])][int(pixelAct[0])][:3]*intensidadTemp
                            #COLOR
                            nuevoColor = get_color (colores[int(pixelAct[0])][int(pixelAct[1])], colorDeLaLuz)
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][0] *= nuevoColor[0]/255
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][1] *= nuevoColor[1]/255
                            pixeles[int(pixelAct[0])][int(pixelAct[1])][2] *= nuevoColor[2]/255
                            #REGISTRO
                            pintados[int(pixelAct[0])][int(pixelAct[1])][1] = True
                            intensidadesDePixeles[int(pixelAct[0])][int(pixelAct[1])] = intensidadTemp
                            colores[int(pixelAct[0])][int(pixelAct[1])] = [nuevoColor[0],nuevoColor[1], nuevoColor[2]]


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
            angulo = random.uniform (271,449)
        else:
            #RAYO VIENE DE LA IZQUIERDA
            angulo = random.uniform (91,269)

    puntoDestino = Point(puntoInterseccion.x + math.cos(math.radians(angulo))*largoRayo, puntoInterseccion.y + math.sin(math.radians(angulo))*largoRayo)
    return puntoDestino
