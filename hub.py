###hub world
from pygame import *
from datetime import datetime
from math import *
from random import *
init()
font.init()
fontSize = 15
storyFont=font.SysFont("Comic Sans MS",fontSize)
lvlFont=font.Font("CRACKERS BRUSHER.otf", 100)
y=550
px=380
py=800

##player=rect(100,100,px,py)
myClock= time.Clock()
size=width,height=800,900
screen=display.set_mode(800,900)
RED=(255,0,0)   
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)
ORANGE=(242,76,0)
YELLOW=(255,248,50)
hubpic=image.load("Hub.jpg")
hubpic=transform.scale(hubpic,(800,height))
guy=image.load("Sprites\\maincharacter.png")

###oVALS

stagelist=[Rect(375,750,50,25),
Rect(400,700,50,25),
Rect(425,650,50,25),
Rect(450,590,50,25),
Rect(410,560,50,25),
Rect(380,520,50,25),
Rect(320,470,50,25),
Rect(350,430,50,25),
Rect(370,380,50,25),
Rect(400,330,50,25),
Rect(400,280,50,25),
Rect(400,220,50,25),
Rect(385,175,50,25)]


pos=0
px, py = stagelist[pos].x-18, stagelist[pos].y-80
pt1=1
pt2=1

running=True
while running:
    pr=False
    click = False
    for evt in event.get():
        if evt.type==QUIT:
            running=False

        if evt.type==MOUSEBUTTONDOWN:
            click=True
        if evt.type==KEYDOWN:
            pr=True

            
    score=str(4561216)
    
    keys=key.get_pressed()
    
    if keys[K_UP] and pos<12 and pr:
        pos += 1
        px, py = stagelist[pos].x-18, stagelist[pos].y-80
    if keys[K_DOWN] and pos>0 and pr:
        pos -= 1
        px, py = stagelist[pos].x-18, stagelist[pos].y-80
    screen.blit(hubpic,(0,0))
    draw.ellipse(screen,BLACK,(stagelist[pos].x-2,stagelist[pos].y-2,54,29))
    draw.ellipse(screen,ORANGE,stagelist[0])
    draw.ellipse(screen,YELLOW,stagelist[1])
    draw.ellipse(screen,YELLOW,stagelist[2])
    draw.ellipse(screen,ORANGE,stagelist[3])
    draw.ellipse(screen,YELLOW,stagelist[4])
    draw.ellipse(screen,YELLOW,stagelist[5])
    draw.ellipse(screen,ORANGE,stagelist[6])
    draw.ellipse(screen,YELLOW,stagelist[7])
    draw.ellipse(screen,YELLOW,stagelist[8])
    draw.ellipse(screen,ORANGE,stagelist[9])
    draw.ellipse(screen,YELLOW,stagelist[10])
    draw.ellipse(screen,YELLOW,stagelist[11])
    draw.ellipse(screen,ORANGE,stagelist[12])
    lvlval=(str(pt1)+"-"+str(pt2))
    if 0<=pos<=2:
        pt1=1
    elif 3<=pos<=5:
        pt1=2
    elif 6<=pos<=8:
        pt1=3
    elif 9<=pos<=11:
        pt1=4
    elif pos==12:
        pt1=5
        
    if pos==0 or pos==3 or pos==6 or pos==9:
        pt2=1
    elif pos==1 or pos==4 or pos==7 or pos==10:
        pt2=2
    elif pos==2 or pos==5 or pos==8 or pos==11:
        pt2=3
    else:
        pt2=1
    
    
    print(pos)
    lvltxt=lvlFont.render((lvlval),False,BLACK)
    scoretxt=lvlFont.render(score,False,BLACK)
    screen.blit(scoretxt,(400,800))
    screen.blit(lvltxt,(10,800))
    screen.blit(guy,(px,py))
    
    
    display.flip()
quit()
