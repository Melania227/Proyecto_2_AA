import numpy as np 
import pygame
import random
from PIL import Image
from Point import *
import math
import threading
from Line import *
from bresenham import bresenham
from RayOperations import *

def raytrace(surface,num):
    
    #pygame.draw.circle(surface, (255,255,0), [fuentesDeLuz[0].x,fuentesDeLuz[0].y], 4)
    #pygame.draw.circle(surface, (255,255,0), [fuentesDeLuz[1].x,fuentesDeLuz[1].y], 4)
    #pygame.draw.circle(surface, (255,255,0), [fuentesDeLuz[2].x,fuentesDeLuz[2].y], 4)
    pintados = []
    for l in range (500):
        fila = []
        for m in range (500):
            fila+=[[]]
        pintados += [fila]
        
    for i in range (1):
        for j in range (360*10):
            for k in range (len(fuentesDeLuz)):
                luz=fuentesDeLuz[k]

                #Toma un punto lejano dentro de los 360 radianes al rededor de la fuente de luz en la que está revisando
                point = Point(luz.x + math.cos(math.radians(j/10))*300, luz.y + math.sin(math.radians(j/10))*300)
                if(point.x<0):
                    point.x = 0
                if(point.x>499):
                    point.x = 499
                if(point.y<0):
                    point.y = 0
                if(point.y>499):
                    point.y =499
                                
                lineaLuzAPunto = Line(point.x,point.y,luz.x,luz.y)
                
                #lineaLuzAPunto.draw (surface,0,255,0) 
                
                interseca = True
                for wall in walls:           
                    if  (lineaLuzAPunto.lineIntersectOrNot(wall)):
                        puntoInterseccion = lineaLuzAPunto.linesIntersection(wall)
                        #Prueba si el punto de interseccion actual es el más cercano a la fuente de luz.
                        if (luz.distanciaEntreDosPuntos(puntoInterseccion)<luz.distanciaEntreDosPuntos(point)):
                            point = puntoInterseccion
                    else:
                        interseca = False
                        
                        #rayoDeLuz= Line(luz.x,luz.y,point.x,point.y)b
                        #rayoDeLuz.draw (surface,255,0,0)
                        #pygame.draw.circle(surface, 245, [int(puntoInterseccion.x),int(puntoInterseccion.y)], 4)

                intensidad = 0.9
                

                drawRayOfLight(surface, px, ref, intensidad, point, luz, pintados)
                #Tendría que rebotar
                if interseca:
                    n=0



def getFrame():
    # grabs the current image and returns it
    pixels = np.roll(px,(1,2),(0,1))
    return pixels


#pygame stuff
h,w=550,550
border=50
pygame.init()
screen = pygame.display.set_mode((w+(2*border), h+(2*border)))
pygame.display.set_caption("Gatito")
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
#fuentesDeLuz = [ Point(373,224)]


#light color
light = np.array([1, 1, 0.75])
#light = np.array([1, 1, 1])

#warning, point order affects intersection test!!
walls = [Line(267, 23, 267, 369), 
        Line(14, 23, 173, 23), 
        Line(14, 23, 14, 256),
        Line(14, 256, 77, 256),
        Line(77, 256, 77,483),
        Line(77,483, 362, 483), 
        Line(362, 333, 362, 483),
        Line(362, 333, 488, 333),
        Line(488, 23, 488, 333),
        Line(267, 23, 488, 23), 
        Line(173, 248, 267, 248),
        Line(173, 23, 173, 369)]

#walls = [Line(267, 23, 267, 369),Line(267, 23, 488, 23), Line(488, 23, 488, 333),Line(362, 333, 362, 483),Line(77, 256, 77,483)]

#thread setup
npimage=getFrame()
surface = pygame.surfarray.make_surface(npimage)
t = threading.Thread(target = raytrace,args=(surface,0)) # f being the function that tells how the ball should move
t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
t.start()

#main loop
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        # Clear screen to white before drawing 
        for wall in walls:
            wall.draw(surface, 255,255,255)
        screen.fill((255, 255, 255))

        # Get a numpy array to display from the simulation
        

        # Convert to a surface and splat onto screen offset by border width and height
        
        npimage=getFrame()
        surface = pygame.surfarray.make_surface(npimage)
        screen.blit(surface, (border, border))

        pygame.display.flip()
        clock.tick(60)
