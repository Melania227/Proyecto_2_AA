from Point import *
import math
from Line import *
from bresenham import bresenham
import numpy as np 

def drawRayOfLight(screen, pixeles, imgRef, intensidad, puntoActual, fuenteLuz):
    trazoPixelesPorPintar = list(bresenham(int(puntoActual.x),int(puntoActual.y),int(fuenteLuz.x),int(fuenteLuz.y)))
    light = np.array([1, 1, 0.75])

    for pxInTrazo in trazoPixelesPorPintar:
        pixeles[int(pxInTrazo[0])][int(pxInTrazo[1])] = pixeles[int(pxInTrazo[0])][int(pxInTrazo[1])] + imgRef[int(pxInTrazo[1])][int(pxInTrazo[0])][:3]*intensidad*light
    # pixeles[int(pxInTrazo[0])][int(pxInTrazo[1])] = imgRef[int(pxInTrazo[1])][int(pxInTrazo[0])][:3]*intensidad*light