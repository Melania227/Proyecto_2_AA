import numpy as np 
import pygame
import random
from PIL import Image
from Point import *
#import rt
import math
import threading
from Line import *


def raytrace(surface,num):
    #Raytraces the scene progessively
    for i in range (5):
        #random point in the image
        point = Point(random.uniform(0, 500), random.uniform(0, 500))
        #pixel color
        pixel = 0

        for luz in fuentesDeLuz:
            #calculates direction to light source
            
            #dir = luz-point
            lineaLuzAPunto = Line(luz.x,luz.y,point.x,point.y)
            distanciaLuzAPunto = point.distanciaEntreDosPuntos(luz)
            lineaLuzAPunto.draw (surface)

            #distance between point and light source
            #normalized distance to source
            #length2 = rt.length(rt.normalize(dir))
            
            interseca = True
            for wall in walls:           
                #if intersection, or if intersection is closer than light source
                if  (lineaLuzAPunto.lineIntersectOrNot(wall)):
                    #check if ray intersects with segment
                    dist = lineaLuzAPunto.linesIntersection(wall)
                    print ("Interseca.")
                    break

            if interseca:        
                intensity = (1-(distanciaLuzAPunto/500))**2
                intensity = max(0, min(intensity, 255))
                values = (ref[int(point.y)][int(point.x)])[:3]
                #combine color, light source and light color
                values = values * intensity * light
                
                #add all light sources 
                pixel += values
            
            #average pixel value and assign
            px[int(point.x)][int(point.y)] = pixel // len(fuentesDeLuz)


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
fuentesDeLuz = [ Point(373,224) ]
#Point(128,133), Point(220,360), 

#light color
light = np.array([1, 1, 0.75])
#light = np.array([1, 1, 1])

#warning, point order affects intersection test!!
walls = [Line(267, 23, 267, 369)]
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
            wall.draw(surface)
        screen.fill((255, 255, 255))

        # Get a numpy array to display from the simulation
        

        # Convert to a surface and splat onto screen offset by border width and height
        
        screen.blit(surface, (border, border))

        pygame.display.flip()
        clock.tick(60)
