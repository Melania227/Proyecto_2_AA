from Point import *
import math
from Line import *
from bresenham import bresenham
import numpy as np 

def drawRayOfLight(screen, pixeles, imgRef, intensidad, puntoActual, fuenteLuz, pintados):
    trazoPixelesPorPintar = list(bresenham(int(puntoActual.x),int(puntoActual.y),int(fuenteLuz.x),int(fuenteLuz.y)))
    totalAPintar = 350
    rango = totalAPintar//8
    contador=0
    intensidad=0.9

    for i in range (len(trazoPixelesPorPintar)-1,0, -1):
        if (contador==rango):
            contador=0
            intensidad = intensidad - 0.1
        contador += 1

        if(pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][0] == 0 and pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][1] == 0 and pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][2] == 0):
            pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])] = imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][:3]*intensidad
            pintados[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])]+=[fuenteLuz]

        else:
            if (fuenteLuz in pintados[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])]):
                continue
            
            intensidadPasada =  pixeles[int(trazoPixelesPorPintar[i][0])][int(trazoPixelesPorPintar[i][1])][0] / imgRef[int(trazoPixelesPorPintar[i][1])][int(trazoPixelesPorPintar[i][0])][0]
            intensidadNueva = intensidad + intensidadPasada

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