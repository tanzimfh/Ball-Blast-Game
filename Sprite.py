###sprite
from random import *
from pygame import *
from math import *

'''Sprite is just a 2D character
A spritesheet is a sheet of all of the frames
of animation that a character uses in a game
9e.g. walking, jumping...)
To achieve this animation we need to display
the frames of the picture in order 
'''

size=width,height=800,600
screen=display.set_mode(size)
RED=(255,0,0)   
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)
myClock = time.Clock()

pics=[]#list of pictures for all frames
try:
    for i in range(1,44,1):
        pics.append(image.load("Sprites\Skeleton"+str(i)+".png"))
except:
    pass
frame=0
frameDelay=6
##screen.blit(pics[0],(100,100))
##screen.blit(pics[2],(100,100))
##screen.blit(pics[6],(100,100))
##    
running=True
while running:

    for evt in event.get():
        if evt.type==QUIT:
            running=False
    try:
        
        screen.fill((160,230,160))
        screen.blit(pics [int(frame)],(200,200))
    except:
        pass
    frameDelay-=1
    if frameDelay==0:
        frameDelay=10
        
        frame+=1
        frame=frame%42
    if frame>30:
        frame=0
    print(frameDelay)
    myClock.tick(60)
    display.flip()
    

quit()
