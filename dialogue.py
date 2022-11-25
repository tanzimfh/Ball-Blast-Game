from pygame import *
from datetime import datetime
from math import *
from random import *
from turtle import *
size=width,height=1280,700
screen=display.set_mode(size)
init()
font.init()
fontSize = 22
fontSize2=10
storyFont=font.SysFont("Comic Sans MS",fontSize)
dialogueFont=font.Font("A Goblin Appears!.otf",fontSize2)
y=550

myClock= time.Clock()

RED=(255,0,0)   
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)

dboxX=240


dboxY=500

####Music
mixer.music.load("Sounds\\victory.mp3")


####skleton
dialoguetxt_skeleton=open("dialogue.txt","r")
dialoguetxt_skeleton=dialoguetxt_skeleton.readlines()
dlist_skeleton=[]

for i in dialoguetxt_skeleton:
    d=i.strip().split(" ")
    dlist_skeleton.append(d)
final_skeleton=" ".join(dlist_skeleton[0])
final2_skeleton=" ".join(dlist_skeleton[1])
final3_skeleton=" ".join(dlist_skeleton[2])

dbox=image.load("txtbox.png")
dbox=transform.scale(dbox,(800,150))

###background
lvl2back=image.load("lvl2back.png")
lvl2back=transform.scale(lvl2back,(1280,900))
lvl3back=image.load("lvl3back.jpg")
lvl3back=transform.scale(lvl3back,(1280,900))

###knight
xyknight=[]

def knight():
    
    pics=[]
    frame=0
    frameDelay=6
    y=177
    j=1
    
    x=(-1/5*(1/2*((y-100)**2))+600)*j
    health=10
    active=False
    active2=False
    for i in range(7,10,1):
        pics.append(image.load("knight"+str(i)+".png"))
        
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
                quit()
        
        mb=mouse.get_pressed()
        screen.blit(lvl2back,(0,0))
        screen.blit(pics [int(frame)],((width/2+x,y)))
        if not active:
            dialogue_knight()
            active=True
            mixer.music.load("Sounds\\knight.mp3")
            mixer.music.set_volume(0.1)
            mixer.music.play(-1)
        y+=j
        x=(-1/5*(1/2*((y-100)**2))+600)*j
        
        print(x,y)
        
        
        
        frameDelay-=1
        if frameDelay==0:
            frameDelay=5
            
            frame+=1
        if frame==3:
            frame=0
        if x<-600 or x>600:
            j*=-1
            for i in range(len(pics)):
                pics[i]=transform.flip(pics[i],1,0)
        if not active:
            dialogue_knight()
            mixer.music.set_volume(0.8)
            active=True
            
        
        if mb[0]==1:
            health=0
        if health==0 and not active2:
            xyknight.append(x)
            xyknight.append(y)
            
            death_knight()
            
            active2=True
        
        myClock.tick(60)
        display.flip()
def death_knight():
    active=False
    pics=[]
    x=0
    for i in range(4,6,1):
        pics.append(image.load("knight"+str(i)+".png"))
    
    print(pics)
    frame=0
    frameDelay=6
    
    running=True
    mixer.music.load("Sounds\\victory.mp3")
    mixer.music.play(0)
    
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        
            
        screen.blit(lvl2back,(0,0))
        screen.blit(pics [int(frame)],(width/2+xyknight[0]+x,xyknight[1]))
        
        if not active:
            deathdialogue_knight()
            myClock.tick(5)
            active=True
        x-=10
        frameDelay-=1
        if frameDelay==0:
            frameDelay=4
            
            frame+=1
        if frame==2:
            frame=0
        mpos=mixer.music.get_pos()
        if mpos==5190:
            quit()
            
            
        
            
        myClock.tick(60)
        display.flip()
def dialogue_knight():
    finaldialogue=""
    finaldialogue2=""
    screen.blit(dbox,(dboxX,dboxY))
    for i in range (len(final_skeleton)):
        finaldialogue+=final_skeleton[i]
        d1=dialogueFont.render(finaldialogue,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50))
        display.flip()
        myClock.tick(60)
    for i in range(len(final2_skeleton)):
        finaldialogue2+=final2_skeleton[i]
        d1=dialogueFont.render(finaldialogue2,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50+20))
        display.flip()
        myClock.tick(60)
def deathdialogue_knight():
    pics=[]
    
    finaldialogue=""
    screen.blit(dbox,(dboxX,dboxY))
    for i in range(len(final3_skeleton)):
        finaldialogue+=final3_skeleton[i]
        d1=dialogueFont.render(finaldialogue,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50))
        display.flip()
        myClock.tick(60)
        
###dragon
dialoguetxt_dragon=open("dialogue_dragon.txt","r")
dialoguetxt_dragon=dialoguetxt_dragon.readlines()
dlist_dragon=[]

for i in dialoguetxt_dragon:
    d=i.strip().split(" ")
    dlist_dragon.append(d)
final_dragon=" ".join(dlist_dragon[0])
final2_dragon=" ".join(dlist_dragon[1])
final3_dragon=" ".join(dlist_dragon[2])
xydragon=[]
def dragon():
    screen=display.set_mode(size)
    pics=[]
    frame=0
    frameDelay=6
    x=5
    j=10
    y=100*sin(1/30*(x - pi/4))+100
    mixer.music.load("Sounds\\dragon.mp3")
    mixer.music.play()
    health=10
    active=False
    active2=False
    for i in range(1,22,1):
        pics.append(image.load("Black Dragon"+str(i)+".png"))
        pics[i-1]=transform.flip(pics[i-1],1,0)
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
                quit()
        
        mb=mouse.get_pressed()
        screen.blit(lvl2back,(0,0))
        screen.blit(pics [int(frame)],(width/2-50+x,y))
        
        x+=j
       # y=(abs(x^2))
        y = 100*sin(1/70*(x - pi/4))+100
        print(y)
        frameDelay-=1
        if frameDelay==0:
            frameDelay=2
            
            frame+=1
        if frame==21:
            frame=0
        if x<-580 or x>600:
            j*=-1
            for i in range(len(pics)):
                pics[i]=transform.flip(pics[i],1,0)
        if not active:
            dialogue_dragon()
            active=True
        if mb[0]==1:
            health=0
        if health==0 and not active2:
            xydragon.append(x)
            xydragon.append(y)
            print(xydragon)
            death_dragon()
            
            active2=True
        
        myClock.tick(60)
        display.flip()
     
def dialogue_dragon():
    finaldialogue=""
    finaldialogue2=""
    screen.blit(dbox,(dboxX,dboxY))
    for i in range (len(final_dragon)):
        finaldialogue+=final_dragon[i]
        d1=dialogueFont.render(finaldialogue,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50))
        display.flip()
        myClock.tick(60)
    for i in range(len(final2_dragon)):
        finaldialogue2+=final2_dragon[i]
        d1=dialogueFont.render(finaldialogue2,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50+20))
        display.flip()
        myClock.tick(60)
    time.wait(1000)
def death_dragon():
    pics=[]
    x=0
    active=False
    try:
        for i in range(1,5,1):
            pics.append(image.load("blackdragondeath"+str(i)+".png"))
    except:
        pass
    print(pics)
    frame=0
    frameDelay=6
    x=width/2-50+xydragon[0]
    running=True
    mixer.music.load("Sounds\\victory.mp3")
    mixer.music.play(0)
    
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        
            
        screen.blit(lvl2back,(0,0))
        screen.blit(pics [int(frame)],(x,xydragon[1]))
        
        if not active:
            blackdragondeath_dialogue()
            myClock.tick(5)
            active=True
        x-=10
        frameDelay-=1
        if frameDelay==0:
            frameDelay=4
            
            frame+=1
        if frame==4:
            frame=0
        if x<-50:
        
            
            return "hub"
            
        myClock.tick(60)
        display.flip()
        
        
def blackdragondeath_dialogue():
        finaldialogue=""
        
        screen.blit(dbox,(dboxX,dboxY))
        
        for i in range(len(final3_dragon)):
            finaldialogue+=final3_dragon[i]
            d1=dialogueFont.render(finaldialogue,False,BLACK)
            screen.blit(d1,(dboxX+50,dboxY+50))
            display.flip()
            myClock.tick(60)
        time.wait(1000)
                

    
####witch

dialoguetxt_witch=open("dialogue_witch.txt","r")
dialoguetxt_witch=dialoguetxt_witch.readlines()
dlist_witch=[]

for i in dialoguetxt_witch:
    d=i.strip().split(" ")
    dlist_witch.append(d)
final_witch=" ".join(dlist_witch[0])
final2_witch=" ".join(dlist_witch[1])
final3_witch=" ".join(dlist_witch[2])
xywitch=[]
def witch():
    pics=[]
    pics2=[]
    frame=0
    frameDelay=6
    x=5
    j=9
##    mixer.music.load("Sounds\\dragon.mp3")
##    mixer.music.play()
    health=10
    active=False
    active2=False
    active3=False
    for i in range(2,10,1):
        pics.append(image.load("witch"+str(i)+".png"))
        pics[i-2]=transform.scale(pics[i-2],(120,180))
    for i in range(10,12,1):
        pics2.append(image.load("witch"+str(i)+".png"))
        pics2[i-10]=transform.scale(pics2[i-10],(120,180))
        
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
                quit()
        
        mb=mouse.get_pressed()
        
        screen.blit(lvl2back,(0,0))
        if frame<8:
            screen.blit(pics [int(frame)],(width/2-50+x,y))
            
        else:
            screen.blit(pics2[int(frame)-9],(width/2-50+x,y))
        if frame>8:  
            x+=j
       # y=(abs(x^2))
        y = 100*sin(1/70*(x - pi/4))+100
        print(y)
        frameDelay-=1
        if frameDelay==0:
            frameDelay=3
            
            frame+=1
        if frame==11:
            frame=9
        if x<-580 or x>550:
            j*=-1
            for i in range (len(pics2)):
                pics2[i]=transform.flip(pics2[i],1,0)
        if not active:
            dialogue_witch()
            active=True
        if mb[0]==1:
            health=0
        if health==0 and not active2:
            xywitch.append(width/2-50+x)
            xywitch.append(y)
            
            death_witch()
            
            active2=True
        
        myClock.tick(60)
        display.flip()    
def dialogue_witch():
    finaldialogue=""
    finaldialogue2=""
    screen.blit(dbox,(dboxX,dboxY))
    for i in range (len(final_witch)):
        finaldialogue+=final_witch[i]
        d1=dialogueFont.render(finaldialogue,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50))
        display.flip()
        myClock.tick(60)
    for i in range(len(final2_witch)):
        finaldialogue2+=final2_witch[i]
        d1=dialogueFont.render(finaldialogue2,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50+20))
        display.flip()
        myClock.tick(20)
def deathdialogue_witch():
    finaldialogue=""
    screen.blit(dbox,(dboxX,dboxY))
    for i in range (len(final3_witch)):
        
        finaldialogue+=final3_witch[i]
        d1=dialogueFont.render(finaldialogue,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50))
        display.flip()
        myClock.tick(10)
        print(finaldialogue)
    quit()
def death_witch():
    pics=[]
    y=0
    try:
        for i in range(1,4,1):
            pics.append(image.load("witchdeath"+str(i)+".png"))
            pics[i-1]=transform.scale(pics[i-1],(120,180))
    except:
        pass
    
    frame=0
    frameDelay=6
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        
            
        screen.blit(lvl2back,(0,0))
        print(xywitch)
        if frame>2:
            frame=2
        screen.blit(pics [int(frame)],(xywitch[0],xywitch[1]+y))
        
        y+=10
        frameDelay-=1
        if frameDelay==0:
            frameDelay=4
            
            frame+=1
        
        if y>800:
            deathdialogue_witch()
            break
        myClock.tick(60)
        display.flip()


######wyvern
dialoguetxt_wyvern=open("dialogue_wyvern.txt","r")
dialoguetxt_wyvern=dialoguetxt_wyvern.readlines()
dlist_wyvern=[]

for i in dialoguetxt_wyvern:
    d=i.strip().split(" ")
    dlist_wyvern.append(d)
final_wyvern=" ".join(dlist_wyvern[0])
final2_wyvern=" ".join(dlist_wyvern[1])
final3_wyvern=" ".join(dlist_wyvern[2])

def wyvern():
    pics=[]
    x=0
    j=4.5
    y=(1/4*(1/20*x)**2)+25
    health=100
    for i in range(1,12,1):
        pics.append(image.load("wyvern"+str(i)+".png"))
        pics[i-1]=transform.flip(pics[i-1],1,0)
    
    active=False
    active2=False
    print(pics)
    frame=0
    frameDelay=6
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        
        mb=mouse.get_pressed()
        screen.blit(lvl3back,(0,0))
        screen.blit(pics [int(frame)],(width/2-50+x,y))
        
        x+=j
        y=(1/4*(1/20*x)**2)+25
        frameDelay-=1
        if frameDelay==0:
            frameDelay=6
            
            frame+=1
        if frame==11:
            frame=0
        if x<-580 or x>530:
            j*=-1
            for i in range(len(pics)):
                pics[i]=transform.flip(pics[i],1,0)
        if not active:
            dialogue_wyvern()
            active=True
        if mb[0]==1:
            health=0
        if health==0 and not active2:
            death_wyvern()
            
            active2=True
        myClock.tick(60)
        display.flip()
        
def dialogue_wyvern():
    finaldialogue=""
    finaldialogue2=""
    screen.blit(dbox,(dboxX,dboxY))
    fontSize2=15
    for i in range (len(final_wyvern)):
        finaldialogue+=final_wyvern[i]
        d1=dialogueFont.render(finaldialogue,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50))
        display.flip()
        myClock.tick(60)
    fontSize2=5
    for i in range(len(final2_wyvern)):
        finaldialogue2+=final2_wyvern[i]
        d1=dialogueFont.render(finaldialogue2,True,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50+20))
        display.flip()
        myClock.tick(60)
    
def death_wyvern():
    finaldialogue="" 
    pics=[]
    x=0
    try:
        for i in range(1,4,1):
            pics.append(image.load("wyverndeath"+str(i)+".png"))
    except:
        pass
    print(pics)
    frame=0
    frameDelay=6
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        
            
        screen.blit(lvl3back,(0,0))
        try:
            screen.blit(pics [int(frame)],(width/2-50+x,100))
        except:
            pass
        
        frameDelay-=1
        if frameDelay==0:
            frameDelay=20
            
            frame+=1
        if frame==3:
            screen.blit(dbox,(dboxX,dboxY))
            for i in range (len(final3_wyvern)):
                finaldialogue+=final3_wyvern[i]
                d1=dialogueFont.render(finaldialogue,False,BLACK)
                screen.blit(d1,(dboxX+50,dboxY+50))
                display.flip()
                
                
                
        
        myClock.tick(60)
        display.flip()


##bAll MASTER

dialoguetxt_master=open("dialogue_master.txt","r")
dialoguetxt_master=dialoguetxt_master.readlines()
dlist_master=[]

for i in dialoguetxt_master:
    d=i.strip().split(" ")
    dlist_master.append(d)
final_master=" ".join(dlist_master[0])
final2_master=" ".join(dlist_master[1])
final3_master=" ".join(dlist_master[2])

def master():
    pics=[]
    x=0
    j=3
    
    for i in range(1,12,1):
        pics.append(image.load("master"+str(i)+".png"))
        pics[i-1]=transform.flip(pics[i-1],1,0)
    
    
    print(pics)
    frame=0
    frameDelay=6
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        
            
        screen.fill(WHITE)
        screen.blit(pics [int(frame)],(width/2-50+x,100))
        
        x+=j
        frameDelay-=1
        if frameDelay==0:
            frameDelay=6
            
            frame+=1
        if frame==11:
            frame=0
        if x<-640 or x>600:
            j*=-1
            for i in range(len(pics)):
                pics[i]=transform.flip(pics[i],1,0)
        
            
        myClock.tick(60)
        display.flip()
        
def dialogue_master():
    finaldialogue=""
    finaldialogue2=""
    screen.blit(dbox,(dboxX,dboxY))
    fontSize2=15
    for i in range (len(final_wyvern)):
        finaldialogue+=final_wyvern[i]
        d1=dialogueFont.render(finaldialogue,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50))
        display.flip()
        myClock.tick(60)
    fontSize2=5
    for i in range(len(final2_wyvern)):
        finaldialogue2+=final2_wyvern[i]
        d1=dialogueFont.render(finaldialogue2,True,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50+20))
        display.flip()
        myClock.tick(60)
def death_master():
    pics=[]
    x=0
    try:
        for i in range(1,5,1):
            pics.append(image.load("masterdeath"+str(i)+".png"))
    except:
        pass
    print(pics)
    frame=0
    frameDelay=6
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        
            
        screen.fill(WHITE)
        screen.blit(pics [int(frame)],(width/2-50+x,100))
       
        x-=2
        frameDelay-=1
        if frameDelay==0:
            frameDelay=4
            
            frame+=1
        if frame==4:
            frame=0
        if x<-700:
            break
        myClock.tick(60)
        display.flip()
    
       
running = True
myClock = time.Clock()
active = False
while running:
    
    for evt in event.get():
        if evt.type == QUIT:
            running = False
   

    

    dragon()
    
    #wyvern()
    #witch()
    #master()
    #knight()
    
    display.flip()
quit()
