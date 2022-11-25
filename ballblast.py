#####BALL BLAST DIMENSIONS MENU.py
from pygame import *
from datetime import datetime
from math import *
from random import *
init()
font.init()
mixer.init()

fontSize = 22
storyFont=font.SysFont("Comic Sans MS",fontSize)  #font for scrolling story
dialogueFont=font.Font("A Goblin Appears!.otf",10)#dialogue font
lvlFont=font.Font("CRACKERS BRUSHER.otf", 100)#lvlfont
lolfont=font.SysFont("Comic Sans MS",30)#font for each lvl

myClock=time.Clock()
size=width,height=1280,900
screen=display.set_mode(size)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)
ORANGE=(242,76,0)
YELLOW=(255,248,50)
#####
donelevels=set() #set with levels that are completed
################################################
MAXRAPID=2 #fire a bullet when rapid reaches MAXRAPID
rapid=MAXRAPID

#loading images
circle=image.load("circle2.png")
bigcircle=transform.scale(circle,(140,140))
midcircle=transform.scale(circle,(100,100))
smcircle=transform.scale(circle,(60,60))
guypic=image.load("guy.png")
guypic=transform.scale(guypic,(60,80))
ghostguypic=image.load("ghostguy.png")
ghostguypic=transform.scale(ghostguypic,(60,80))
fastpic=image.load("fast.png")
fastpic=transform.scale(fastpic,(60,60))
slowpic=image.load("slowpic.png")
slowpic=transform.scale(slowpic,(60,60))
xpic=image.load("2x.png")
xpic=transform.scale(xpic,(60,60))
ghostpic=image.load("ghost.png")
ghostpic=transform.scale(ghostpic,(60,60))
bulletpic=image.load("9mm.png")
bulletpic=transform.scale(bulletpic,(20,20))


#initializing variables
score=0
tmin=20 #min & max health for full-sized targets
tmax=40
mtmin=10 #min & max for medium targets
mtmax=20
stmin=5 #min & max small targets
stmax=10
yspeed=0.015 #angle added to sin function get next y-value of balls
slowyspeed=0.0075 #when slow powerup is on
xspeed=6 #pixels to move left or right every frame
slowxspeed=3 #when slow is on
targets=[] #list of full-sized targets
midtargets=[] #medium targets
smtargets=[] #small
maxtarg=12 #maximum "number" of targets on screen at a time
death=False
slow=False #slow balls powerup
ghost=False #ghost player powerup
powerupchance=2400 #1/2400 chance of a powerup appearing every frame

#duration left of each powerup
fastduration=0 #faster bullets powerup
slowduration=0
xduration=0 #2x bullets powerup
ghostduration=0

#list of powerup balls on screen
slowballs=[]
gunfastballs=[]
xballs=[]
ghostballs=[]

bullets=[]

def moveBalls(targets,lvl,midtargets,smtargets,gfastballs,slowballs,xballs,ghostballs,slow):
    for target in targets: #full-sized targets
        if slow: #slow down speeds if show powerup is on
            if target[2]>0:
                target[2]=slowxspeed
            else:
                target[2]=-slowxspeed
        else: #speed up otherwise
            if target[2]>0:
                target[2]=xspeed
            else:
                target[2]=-xspeed

        if target[5]: #if target is in frame
            if target[0]>1210 or target[0]<70: #if target hits edges
                target[2]*=-1 #switch horizontal direction
        else: #if outside frame
            if target[0]<1100 and target[0]>180: #if enters frame
                target[5]=True
        target[0]+=target[2] #move ball horizontally
        target[1]=int(-(sin(target[3])*600)+730) #using sin function to determine path of ball
        if slow:
            target[3]+=slowyspeed #change to next angle
        else:
            target[3]+=yspeed
        if target[3]>pi: #reset to 0 when angle reaches 180 degrees
            target[3]-=pi

    for target in midtargets: #medium targets
        if slow:
            if target[2]>0:
                target[2]=slowxspeed
            else:
                target[2]=-slowxspeed
        else:
            if target[2]>0:
                target[2]=xspeed
            else:
                target[2]=-xspeed
        if target[0]>1250 or target[0]<30:
            target[2]*=-1
        target[0]+=target[2]
        if target[5]: #if ball has hit the bottom at leaast once
            target[1]=int(-(sin(target[3])*500)+750) #follow medium-sized ball path
            if slow:
                target[3]+=slowyspeed
            else:
                target[3]+=yspeed
        else: #if ball just spawned from parent full-sized ball
            target[1]=int(-(sin(target[3])*600)+750) #keep following full-sized ball path for smoothness
            if slow:
                target[3]+=slowyspeed
            else:
                target[3]+=yspeed
            if target[3]>pi: #when hits bottom
                target[5]=True #start following medium ball path
        if target[3]>pi:
            target[3]-=pi

    for target in smtargets: #small targets
        if slow:
            if target[2]>0:
                target[2]=slowxspeed
            else:
                target[2]=-slowxspeed
        else:
            if target[2]>0:
                target[2]=xspeed
            else:
                target[2]=-xspeed
        if target[0]>1250 or target[0]<30:
            target[2]*=-1
        target[0]+=target[2]
        if target[5]:
            target[1]=int(-(sin(target[3])*400)+770)
            if slow:
                target[3]+=slowyspeed
            else:
                target[3]+=yspeed
        else:
            target[1]=int(-(sin(target[3])*500)+770)
            if slow:
                target[3]+=slowyspeed
            else:
                target[3]+=yspeed
            if target[3]>pi:
                target[5]=True
        if target[3]>pi:
            target[3]-=pi

    #powerup balls, follow same rules as small balls except they don't spawn from a parent ball and don't need smoothness fix
    for target in gfastballs:
        if slow:
            if target[2]>0:
                target[2]=slowxspeed
            else:
                target[2]=-slowxspeed
        else:
            if target[2]>0:
                target[2]=xspeed
            else:
                target[2]=-xspeed
        if target[4]:
            if target[0]>1250 or target[0]<30:
                target[2]*=-1
        else:
            if target[0]<1100 and target[0]>180: 
                target[4]=True
        target[0]+=target[2]

        target[1]=int(-(sin(target[3])*400)+770)
        if slow:
            target[3]+=slowyspeed
        else:
            target[3]+=yspeed
        if target[3]>pi:
            target[3]-=pi

    for target in slowballs:
        if slow:
            if target[2]>0:
                target[2]=slowxspeed
            else:
                target[2]=-slowxspeed
        else:
            if target[2]>0:
                target[2]=xspeed
            else:
                target[2]=-xspeed
        if target[4]:
            if target[0]>1250 or target[0]<30:
                target[2]*=-1
        else:
            if target[0]<1100 and target[0]>180: 
                target[4]=True
        target[0]+=target[2]

        target[1]=int(-(sin(target[3])*400)+770)
        if slow:
            target[3]+=slowyspeed
        else:
            target[3]+=yspeed
        if target[3]>pi:
            target[3]-=pi

    for target in xballs:
        if slow:
            if target[2]>0:
                target[2]=slowxspeed
            else:
                target[2]=-slowxspeed
        else:
            if target[2]>0:
                target[2]=xspeed
            else:
                target[2]=-xspeed
        if target[4]:
            if target[0]>1250 or target[0]<30:
                target[2]*=-1
        else:
            if target[0]<1100 and target[0]>180: 
                target[4]=True
        target[0]+=target[2]

        target[1]=int(-(sin(target[3])*400)+770)
        if slow:
            target[3]+=slowyspeed
        else:
            target[3]+=yspeed
        if target[3]>pi:
            target[3]-=pi

    for target in ghostballs:
        if slow:
            if target[2]>0:
                target[2]=slowxspeed
            else:
                target[2]=-slowxspeed
        else:
            if target[2]>0:
                target[2]=xspeed
            else:
                target[2]=-xspeed
        if target[4]:
            if target[0]>1250 or target[0]<30:
                target[2]*=-1
        else:
            if target[0]<1100 and target[0]>180: 
                target[4]=True
        target[0]+=target[2]
        target[1]=int(-(sin(target[3])*400)+770)
        if slow:
            target[3]+=slowyspeed
        else:
            target[3]+=yspeed
        if target[3]>pi:
            target[3]-=pi
    #change max targets depending on level and current score
    if lvl<3:
        maxtarg=12+int(score/500)
    elif lvl<6:
        maxtarg=13+int(score/500)
    elif lvl<9:
        maxtarg=14+int(score/500)
    else:
        maxtarg=15+int(score/500)
    return maxtarg #return updated max targets

                           #player/guy  bullets  all 3 target lists             powerup balls           ghost powerup duration  ghost boolean           pic to blit for boss levels    location to blit
def drawScene(screen,score,     g       ,bull,targ,midtarg,smtarg,gunfastballs,slowballs,xballs,ghostballs,ghostduration,background,ghost,health,maxhealth,     pic,                   loc):
    y=0
    if background==startback: #blitting background (startback is special because it's tall)
        y=-1200
    screen.blit(background,(0,y))
    
    for b in bull:
        screen.blit(bulletpic,(b[0]-10,b[1]-10)) #blitting bullet pic
    for t in targ:
        screen.blit(bigcircle,(t[0]-70,t[1]-70)) #ball pic
        num=lolfont.render(str(t[4]),True,BLACK) #health text
        if t[4]>10:
            screen.blit(num,(t[0]-17,t[1]-19)) #blitting at different spots depending on width of text
        else:
            screen.blit(num,(t[0]-9,t[1]-23))
    for t in midtarg:
        screen.blit(midcircle,(t[0]-50,t[1]-50))
        num=lolfont.render(str(t[4]),True,BLACK)
        if t[4]>10:
            screen.blit(num,(t[0]-17,t[1]-19))
        else:
            screen.blit(num,(t[0]-9,t[1]-23))
    for t in smtarg:
        screen.blit(smcircle,(t[0]-30,t[1]-30))
        num=lolfont.render(str(t[4]),True,BLACK)
        screen.blit(num,(t[0]-9,t[1]-23))

    for t in gunfastballs: #blitting powerup pics
        screen.blit(fastpic,(t[0]-30,t[1]-30))
    for t in slowballs:
        screen.blit(slowpic,(t[0]-30,t[1]-30))
    for t in xballs:
        screen.blit(xpic,(t[0]-30,t[1]-30))
    for t in ghostballs:
        screen.blit(ghostpic,(t[0]-30,t[1]-30))

    if ghost: #flashing ghost effect when 1 second of ghost powerup left
        if ghostduration<20:
            screen.blit(ghostguypic,(g[0]-30,g[1]-50))
        elif ghostduration<45:
            screen.blit(guypic,(g[0]-30,g[1]-50))
        elif ghostduration<75:
            screen.blit(ghostguypic,(g[0]-30,g[1]-50))
        elif ghostduration<110:
            screen.blit(guypic,(g[0]-30,g[1]-50))
        else:
            screen.blit(ghostguypic,(g[0]-30,g[1]-50))
    else:
        screen.blit(guypic,(g[0]-30,g[1]-50)) #regular non-ghost guy
    scoretext=lolfont.render(str(score),True,WHITE)
    screen.blit(scoretext,(5,0)) #score in top-left corner

    #health bar
    maxhealthrect=Rect(760,20,500,40)
    healthrect=Rect(760,20,500*(health/maxhealth),40)
    draw.rect(screen,GREEN,healthrect)
    draw.rect(screen,BLACK,maxhealthrect,5)

    #blitting boss pic
    screen.blit(pic,(loc))
    
    display.flip()

def checkHits(bull,targets,midtargets,smtargets,score):
    for b in bull:
        for target in targets:
            if sqrt((b[0]-target[0])**2+(b[1]-target[1])**2)<75: #if bullet hits target
                score+=1 #gain 1 point
                if target[4]==1: #if ball has one hp left
                    midtargets.append([target[0],target[1],-target[2],target[3],randint(mtmin,mtmax),False]) #split into 2 medium balls
                    midtargets.append([target[0],target[1],target[2],target[3],randint(mtmin,mtmax),False])
                    targets.remove(target)
                else: #if more hp
                    target[4]-=1 #take one hp off
                try:
                    bull.remove(b)
                except:
                    pass

        for target in midtargets: #same for medium targets
            if sqrt((b[0]-target[0])**2+(b[1]-target[1])**2)<55:
                score+=1
                if target[4]==1:
                    smtargets.append([target[0],target[1],-target[2],target[3],randint(stmin,stmax),False])
                    smtargets.append([target[0],target[1],target[2],target[3],randint(stmin,stmax),False])
                    midtargets.remove(target)
                else:
                    target[4]-=1
                try:
                    bull.remove(b)
                except:
                    pass

        for target in smtargets:
            if sqrt((b[0]-target[0])**2+(b[1]-target[1])**2)<35:
                score+=1
                if target[4]==1:
                    smtargets.remove(target) #no split from small balls
                else:
                    target[4]-=1
                try:
                    bull.remove(b)
                except:
                    pass
    
    return score

def checkDeath(targets,midtargets,smtargets,guy,ghost):
    if ghost==False: #if ghost powerup isn't active
        #death=True if ball hits player
        for t in targets:
            if sqrt((t[0]-guy[0])**2+(t[1]-guy[1])**2)<100:
                return True
        for t in midtargets:
            if sqrt((t[0]-guy[0])**2+(t[1]-guy[1])**2)<80:
                return True
        for t in smtargets:
            if sqrt((t[0]-guy[0])**2+(t[1]-guy[1])**2)<60:
                return True
    return False #death=False if balls don't hit or if ghost is active

def moveBullets(bull): #move bullets up
    for b in bull:
        b[0]+=b[2]
        b[1]+=b[3]
        if b[1]<0: #delete bullet when it leaves frame
            bull.remove(b)

def gunfastcheck(gunfastballs,guy,fastduration):
    for t in gunfastballs:
        if sqrt((t[0]-guy[0])**2+(t[1]-guy[1])**2)<60:
            gunfastballs.remove(t)
            return (450) #fast gun powerup duration if powerup touches player
    if fastduration>0:
        fastduration-=1 #duration goes down by 1 every frame if powerup is active
        return (fastduration)
    else:
        return (0)

def slowcheck(slowballs,guy,slowduration):
    for t in slowballs:
        if sqrt((t[0]-guy[0])**2+(t[1]-guy[1])**2)<60:
            slowballs.remove(t)
            return (300) #same as fast powerup ^
    if slowduration>0:
        slowduration-=1
        return (slowduration)
    else:
        return (0)

def xcheck(xballs,guy,xduration):
    for t in xballs:
        if sqrt((t[0]-guy[0])**2+(t[1]-guy[1])**2)<60:
            xballs.remove(t)
            return (450)
    if xduration>0:
        xduration-=1
        return (xduration)
    else:
        return (0)

def ghostcheck(ghostballs,guy,ghostduration):
    for t in ghostballs:
        if sqrt((t[0]-guy[0])**2+(t[1]-guy[1])**2)<60:
            ghostballs.remove(t)
            return (600)
    if ghostduration>0:
        ghostduration-=1
        return (ghostduration)
    else:
        return (0)

                #health values       #pic of boss   location
def checkhealth(maxhealth,health,bullets,frame,     x,y):
    hitbox=Rect(x,y,frame.get_width(),frame.get_height()) #hitbox is the boss's picture in current frame
    for b in bullets:
        if hitbox.collidepoint(b[0],b[1]):
            health-=1 #take health off if hit
            bullets.remove(b)
    return (health) #return updated health
###############################################
#########menu picture loading
startpic=image.load("Text Pictures\start.png")
controlpic=image.load("Text Pictures\controls.png")
exitpic=image.load("Text Pictures\exit.png")
titlepic=image.load("Text Pictures\\title.png")
menuback=image.load("Text Pictures\\menuback.jpg")
menuback=transform.scale(menuback,(width,height))
startback=image.load("Text Pictures\\startback.png")
startback=transform.scale(startback,(width,2100))
dbox=image.load("txtbox.png")
endback=image.load("endstory.jpg")
endback=transform.scale(endback,(width,2100))
startpic.get_width()
endpic=image.load("Text Pictures\\end.png")
hubpic=image.load("Hub.jpg")
hubpic=transform.scale(hubpic,(800,height))
guy=image.load("maincharacter.png")

###dialogue box values
dboxX=240
dboxY=700


###oVALS for hub

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

###background for each world
lvl2back=image.load("lvl2back.jpg")
lvl2back=transform.scale(lvl2back,(1280,900))
lvl3back=image.load("lvl3back.png")
lvl3back=transform.scale(lvl3back,(1280,900))
lvl4back=image.load("lvl4back.png")
lvl4back=transform.scale(lvl4back,(1280,900))
lvl5back=image.load("lvl5back.jpg")
lvl5back=transform.scale(lvl5back,(1280,900))

####knight/skeleton
dialoguetxt_skeleton=open("dialogue.txt","r")  #opening txt file
dialoguetxt_skeleton=dialoguetxt_skeleton.readlines()
dlist_skeleton=[]

for i in dialoguetxt_skeleton:
    d=i.strip().split(" ")
    dlist_skeleton.append(d)
final_skeleton=" ".join(dlist_skeleton[0])
final2_skeleton=" ".join(dlist_skeleton[1])
final3_skeleton=" ".join(dlist_skeleton[2]) #creating a different variable for each line

dbox=image.load("txtbox.png")####loading dialogue
dbox=transform.scale(dbox,(800,150))


###knight
xyknight=[] ###list to append after knight dies

def knight(): #knight boss
    
    pics=[] ##sprites
    frame=0
    frameDelay=6
    y=177 #starting y val
    j=1  #changing val for y
    
    x=(-1/5*(1/2*((y-100)**2))+600)*j  ####horizontal parabola
    active=False  ###to run function 1 time
    for i in range(7,10,1):
        pics.append(image.load("knight"+str(i)+".png")) ##sprite
    ######
    #resetting all variables that can be changed in other levels
    MAXRAPID=2
    rapid=MAXRAPID

    maxhealth=50 #knight's health
    health=50

    score=0
        
    targets=[]
    midtargets=[]
    smtargets=[]

    maxtarg=12

    death=False
    slow=False
    ghost=False
    powerupchance=1200

    fastduration=0
    slowduration=0
    xduration=0
    ghostduration=0

    slowballs=[]
    gunfastballs=[]
    xballs=[]
    ghostballs=[]

    bullets=[]

    lvl=0 #level number
    powerupchance=1200
    maxtarg=12

    #start with 3 targets
    targets.append([randint(100,1180),0,xspeed,pi/2,randint(tmin,tmax),True])
    targets.append([-70,xspeed,6,pi/2,randint(tmin,tmax),False])
    targets.append([1350,0,-xspeed,pi/2,randint(tmin,tmax),False])
    ###
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
                quit()
        
        mb=mouse.get_pressed()
        
        if not active: #knight dialogue
            dialogue_knight()
            active=True
            mixer.music.load("Sounds\\knight.mp3")
            mixer.music.set_volume(0.1)
            mixer.music.play(-1)
        y+=j
        x=(-1/5*(1/2*((y-100)**2))+600)*j #path
        
        frameDelay-=1
        if frameDelay==0:
            frameDelay=5
            
            frame+=1
        if frame==3:
            frame=0
        if x<-600 or x>600: #reversing direction and flipping pic
            j*=-1
            for i in range(len(pics)):
                pics[i]=transform.flip(pics[i],1,0)
        if not active: #running dialogue 1 time
            dialogue_knight()
            mixer.music.set_volume(0.8)
            active=True
            
        mx,my=mouse.get_pos()
        guy=[mx,770]  #pos of main character

        #add ball if less on screen than max target points
            #big balls worth 4 points   mid-2    small-1
        if len(targets)*4+len(midtargets)*2+len(smtargets)<maxtarg:
            lr=randint(1,2) #coming from left or right
            if lr==1:
                        #        x   y  xspeed  yspeed      health      inside frame=False
                targets.append([-30,100,6,      pi/2,  randint(tmin,tmax),  False])
            else:
                targets.append([1310,100,-6,pi/2,randint(tmin,tmax),False])

        powerup=randint(0,powerupchance) #powerups awarded if randint lands on 1-4
        lr=randint(1,2)

        #add ball to corresponding powerup list if the powerup isn't already on screen
        if powerup==1 and len(gunfastballs)==0:
            if lr==1:
                gunfastballs.append([-30,100,6,pi/2,False])
            else:
                gunfastballs.append([1310,100,-6,pi/2,False])

        if powerup==2 and len(slowballs)==0:
            if lr==1:
                slowballs.append([-30,100,6,pi/2,False])
            else:
                slowballs.append([1310,100,-6,pi/2,False])

        if powerup==3 and len(xballs)==0:
            if lr==1:
                xballs.append([-30,100,6,pi/2,False])
            else:
                xballs.append([1310,100,-6,pi/2,False])

        if powerup==4 and len(ghostballs)==0:
            if lr==1:
                ghostballs.append([-30,100,6,pi/2,False])
            else:
                ghostballs.append([1310,100,-6,pi/2,False])

        if fastduration>0:
            MAXRAPID=1 #fires twice as fast with fast powerup active
        else:
            MAXRAPID=2

        if slowduration>0:
            slow=True
        else:
            slow=False

        if rapid>=MAXRAPID: #when rapid hits MAXRAPID
            if xduration>0: #add 2 bullets if 2x bullets powerup active
                bullets.append([guy[0]-10,guy[1]-20,0,-25])
                bullets.append([guy[0]+10,guy[1]-20,0,-25])
            else:
                bullets.append([guy[0],guy[1]-20,0,-25])
            rapid=0 #reset rapid
        else:
            rapid+=1

        if ghostduration>0:
            ghost=True
        else:
            ghost=False

        if death==False:
            maxtarg=moveBalls(targets,lvl,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,slow)               #         bg                              boss pic          location
            drawScene(screen,score,guy,bullets,targets,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,ghostduration,startback,ghost,health,maxhealth,pics[int(frame)],(width/2+x,y))
            health=checkhealth(maxhealth,health,bullets,pics[int(frame)],(width/2+x),y)
            moveBullets(bullets)
            score=checkHits(bullets,targets,midtargets,smtargets,score)
            fastduration=gunfastcheck(gunfastballs,guy,fastduration)
            slowduration=slowcheck(slowballs,guy,slowduration)
            xduration=xcheck(xballs,guy,xduration)
            ghostduration=ghostcheck(ghostballs,guy,ghostduration)
            death=checkDeath(targets,midtargets,smtargets,guy,ghost)
            if health<=0: #when knight dies
                donelevels.add(0) #add knight's level to set of completed levels
                #####blitting end text if win
                xyknight.append(x)
                xyknight.append(y)
                death_knight() ###animation for win
                endtext=lolfont.render("CONGRATULATIONS",True,BLACK)
                screen.blit(endtext,(550,400))
                endscore=lolfont.render("Score: "+str(score),True,BLACK)
                screen.blit(endscore,(570,450))
                nexttxt=lolfont.render("Back to hub (Left Click)",True,BLACK)
                screen.blit(nexttxt,(520,500))
                if mb[0]==1: #returning to hub
                    hub()
        else:
            
            
        
            ##########blitting end text if lose
            endtext=lolfont.render("GAME OVER",True,BLACK)
            screen.blit(endtext,(550,400))
            endscore=lolfont.render("Score: "+str(score),True,BLACK)
            screen.blit(endscore,(570,450))
            nexttxt=lolfont.render("Back to hub (Left Click)",True,BLACK)
            screen.blit(nexttxt,(520,500))
            if mb[0]==1: #return to  hub
                hub()
            
            

        myClock.tick(60)
        display.flip()
        
def death_knight(): ###################################################################################################################################################################################
    active=False
    pics=[]
    x=0
    for i in range(4,6,1):
        pics.append(image.load("knight"+str(i)+".png"))
    
    frame=0
    frameDelay=6
    
    running=True
    mixer.music.load("Sounds\\victory.mp3")
    mixer.music.play()
    
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                quit()  
        
            
        screen.blit(startback,(0,-1200))
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
        if mpos==-1:
            hub()
                        
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
        myClock.tick(30)
    for i in range(len(final2_skeleton)):
        finaldialogue2+=final2_skeleton[i]
        d1=dialogueFont.render(finaldialogue2,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50+20))
        display.flip()
        myClock.tick(30)
    time.wait(10000)
def deathdialogue_knight():
    pics=[]
    
    finaldialogue=""
    screen.blit(dbox,(dboxX,dboxY))
    for i in range(len(final3_skeleton)):
        finaldialogue+=final3_skeleton[i]
        d1=dialogueFont.render(finaldialogue,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50))
        display.flip()
        myClock.tick(30)
###########################################################################################################################################################################################

    #number of level
def level(lvl):
    screen=display.set_mode(size)
    mixer.music.load("Sounds\\dragon.mp3") ###################################################################################################################################################################################
    mixer.music.play(-1)
    
    ############## mostly same as knight
    MAXRAPID=2
    rapid=MAXRAPID

    health=lvl*50+300 #different health (score needed to win) based on number of level
    maxhealth=health

    targets=[]
    midtargets=[]
    smtargets=[]

    death=False
    slow=False
    ghost=False
    #different settings for each group of levels
    if lvl<3:
        powerupchance=1200
        maxtarg=12
        background=lvl2back
    elif lvl<6:
        powerupchance=1800
        maxtarg=13
        background=lvl3back
    elif lvl<9:
        powerupchance=2400
        maxtarg=14
        background=lvl4back
    else:
        powerupchance=3000
        maxtarg=15
        background=lvl5back

    score=0
    fastduration=0
    slowduration=0
    xduration=0
    ghostduration=0

    slowballs=[]
    gunfastballs=[]
    xballs=[]
    ghostballs=[]

    bullets=[]

    targets.append([randint(100,1180),0,xspeed,pi/2,randint(tmin,tmax),True])
    if lvl>3: #add a 4th ball after the first 4 levels
        targets.append([randint(100,1180),0,xspeed,pi*2/3,randint(tmin,tmax),True])
        
    targets.append([-70,xspeed,6,pi/2,randint(tmin,tmax),False])
    targets.append([1350,0,-xspeed,pi/2,randint(tmin,tmax),False])
    ###############

    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
                quit()
        
        mb=mouse.get_pressed()
        keys=key.get_pressed()
        mx,my=mouse.get_pos()
        guy=[mx,770]

        if len(targets)*4+len(midtargets)*2+len(smtargets)<maxtarg:
            lr=randint(1,2)
            if lr==1:
                targets.append([-30,100,6,pi/2,randint(tmin,tmax),False])
            else:
                targets.append([1310,100,-6,pi/2,randint(tmin,tmax),False])

        powerup=randint(0,powerupchance)
        lr=randint(1,2)
        
        if powerup==1 and len(gunfastballs)==0:
            if lr==1:
                gunfastballs.append([-30,100,6,pi/2,False])
            else:
                gunfastballs.append([1310,100,-6,pi/2,False])
        if powerup==2 and len(slowballs)==0:
            if lr==1:
                slowballs.append([-30,100,6,pi/2,False])
            else:
                slowballs.append([1310,100,-6,pi/2,False])
        if powerup==3 and len(xballs)==0:
            if lr==1:
                xballs.append([-30,100,6,pi/2,False])
            else:
                xballs.append([1310,100,-6,pi/2,False])
        if powerup==4 and len(ghostballs)==0:
            if lr==1:
                ghostballs.append([-30,100,6,pi/2,False])
            else:
                ghostballs.append([1310,100,-6,pi/2,False])

        if fastduration>0:
            MAXRAPID=1
        else:
            MAXRAPID=2

        if slowduration>0:
            slow=True
        else:
            slow=False

        if rapid>=MAXRAPID:
            if xduration>0:
                bullets.append([guy[0]-10,guy[1]-20,0,-25])
                bullets.append([guy[0]+10,guy[1]-20,0,-25])
            else:
                bullets.append([guy[0],guy[1]-20,0,-25])
            rapid=0
        else:
            rapid+=1

        if ghostduration>0:
            ghost=True
        else:
            ghost=False

        if death==False:
            maxtarg=moveBalls(targets,lvl,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,slow)                                               #boss pic not needed for regular levels
            drawScene(screen,score,guy,bullets,targets,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,ghostduration,background,ghost,health,maxhealth,ghostpic,(-100,-100))
            health=maxhealth-score #health=score left
            moveBullets(bullets)
            score=checkHits(bullets,targets,midtargets,smtargets,score)
            fastduration=gunfastcheck(gunfastballs,guy,fastduration)
            slowduration=slowcheck(slowballs,guy,slowduration)
            xduration=xcheck(xballs,guy,xduration)
            ghostduration=ghostcheck(ghostballs,guy,ghostduration)
            death=checkDeath(targets,midtargets,smtargets,guy,ghost)
            if health<=0: #when score requirement reached
                donelevels.add(lvl) #add current level to completed list
                running=False
                endtext=lolfont.render("WINNER!!!",True,BLACK)
                screen.blit(endtext,(550,400))
                endscore=lolfont.render("Score: "+str(score),True,BLACK)
                screen.blit(endscore,(570,450))
                display.flip()                            
                time.wait(1000)
                hub()
        else:

            endtext=lolfont.render("GAME OVER",True,BLACK)
            screen.blit(endtext,(550,400))
            endscore=lolfont.render("Score: "+str(score),True,BLACK)
            screen.blit(endscore,(570,450))
            nexttxt=lolfont.render("Back to hub (Left Click)",True,BLACK)
            screen.blit(nexttxt,(520,500))
            if mb[0]==1:
                hub()
            
            

        myClock.tick(60)
        display.flip()

###dragon, same as knight but with different pictures and harder gameplay settings
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
    j=5
    y=100*sin(1/30*(x - pi/4))+100 ###################################################################################################################################################################################
    mixer.music.load("Sounds\\dragon.mp3")
    mixer.music.play(-1)
    maxhealth=150
    health=150
    
    active=False
    active2=False
    ##############
    MAXRAPID=2
    rapid=MAXRAPID
    
    targets=[]
    midtargets=[]
    smtargets=[]


    death=False
    slow=False
    ghost=False
    powerupchance=1800

    score=0
    fastduration=0
    slowduration=0
    xduration=0
    ghostduration=0

    slowballs=[]
    gunfastballs=[]
    xballs=[]
    ghostballs=[]

    bullets=[]
    lvl=3
    powerupchance=1800
    maxtarg=14

    targets.append([randint(100,1180),0,xspeed,pi/2,randint(tmin,tmax),True])
    targets.append([randint(100,1180),0,xspeed,pi*2/3,randint(tmin,tmax),True]) #4th ball required from this point on to reach maxtarg
    targets.append([-70,xspeed,6,pi/2,randint(tmin,tmax),False])
    targets.append([1350,0,-xspeed,pi/2,randint(tmin,tmax),False])
    ###############
    for i in range(1,22,1):
        pics.append(image.load("Black Dragon"+str(i)+".png"))
        pics[i-1]=transform.flip(pics[i-1],1,0) ###################################################################################################################################################################################
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
                quit()
        
        mb=mouse.get_pressed()
        keys=key.get_pressed()
        
        if not active:
            screen.blit(lvl2back,(0,0))
            screen.blit(pics [int(frame)],(width/2-50+x,y))
            dialogue_dragon()
            active=True
        x+=j

        y = 100*sin(1/70*(x - pi/4))+100
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
    
        mx,my=mouse.get_pos()
        guy=[mx,770]

        if len(targets)*4+len(midtargets)*2+len(smtargets)<maxtarg:
            lr=randint(1,2)
            if lr==1:
                targets.append([-30,100,6,pi/2,randint(tmin,tmax),False])
            else:
                targets.append([1310,100,-6,pi/2,randint(tmin,tmax),False])

        powerup=randint(0,powerupchance)
        lr=randint(1,2)
        
        if powerup==1 and len(gunfastballs)==0:
            if lr==1:
                gunfastballs.append([-30,100,6,pi/2,False])
            else:
                gunfastballs.append([1310,100,-6,pi/2,False])
        if powerup==2 and len(slowballs)==0:
            if lr==1:
                slowballs.append([-30,100,6,pi/2,False])
            else:
                slowballs.append([1310,100,-6,pi/2,False])
        if powerup==3 and len(xballs)==0:
            if lr==1:
                xballs.append([-30,100,6,pi/2,False])
            else:
                xballs.append([1310,100,-6,pi/2,False])
        if powerup==4 and len(ghostballs)==0:
            if lr==1:
                ghostballs.append([-30,100,6,pi/2,False])
            else:
                ghostballs.append([1310,100,-6,pi/2,False])

        if fastduration>0:
            MAXRAPID=1
        else:
            MAXRAPID=2
        if slowduration>0:
            slow=True
        else:
            slow=False
        if rapid>=MAXRAPID:
            if xduration>0:
                bullets.append([guy[0]-10,guy[1]-20,0,-25])
                bullets.append([guy[0]+10,guy[1]-20,0,-25])
            else:
                bullets.append([guy[0],guy[1]-20,0,-25])
            rapid=0
        else:
            rapid+=1

        if ghostduration>0:
            ghost=True
        else:
            ghost=False

        if death==False:
            maxtarg=moveBalls(targets,lvl,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,slow)
            drawScene(screen,score,guy,bullets,targets,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,ghostduration,lvl2back,ghost,health,maxhealth,pics[int(frame)],(width/2-50+x,y))
            health=checkhealth(maxhealth,health,bullets,pics[int(frame)],(width/2-50+x),y)
            moveBullets(bullets)
            score=checkHits(bullets,targets,midtargets,smtargets,score)
            fastduration=gunfastcheck(gunfastballs,guy,fastduration)
            slowduration=slowcheck(slowballs,guy,slowduration)
            xduration=xcheck(xballs,guy,xduration)
            ghostduration=ghostcheck(ghostballs,guy,ghostduration)
            death=checkDeath(targets,midtargets,smtargets,guy,ghost)
            if health<=0:
                donelevels.add(3)
                xydragon.append(x)
                xydragon.append(y)
                death_dragon()
                running=False
                endtext=lolfont.render("WINNER!!!",True,BLACK)
                screen.blit(endtext,(550,400))
                endscore=lolfont.render("Score: "+str(score),True,BLACK)
                screen.blit(endscore,(570,450))
                display.flip()                            
                time.wait(1000)
                hub()
        else:
            
            
        
            
            endtext=lolfont.render("GAME OVER",True,BLACK)
            screen.blit(endtext,(550,400))
            endscore=lolfont.render("Score: "+str(score),True,BLACK)
            screen.blit(endscore,(570,450))
            nexttxt=lolfont.render("Back to hub (Left Click)",True,BLACK)
            screen.blit(nexttxt,(520,500))
            if mb[0]==1:
                hub()
            
            

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
    
    frame=0
    frameDelay=6
    x=width/2-50+xydragon[0]
    running=True
    mixer.music.load("Sounds\\victory.mp3")
    mixer.music.play(1)
    
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        screen.blit(lvl2back,(0,0))
        screen.blit(pics [int(frame)],(x,xydragon[1]))
        
        if not active:
            blackdragondeath_dialogue()
            
            active=True
        x-=10
        frameDelay-=1
        if frameDelay==0:
            frameDelay=4
            
            frame+=1
        if frame==4:
            frame=0
        mpos=mixer.music.get_pos() ###################################################################################################################################################################################
        
        if mpos>=5100 and x<0:                              #THIS FUNCTION DOESN'T END BY ITSELF
            
        
            
            break
            
        myClock.tick(60)
        display.flip()
        
        
def blackdragondeath_dialogue():
        finaldialogue=""
        running=True
        screen.blit(dbox,(dboxX,dboxY))
        
        for i in range(len(final3_dragon)):
            finaldialogue+=final3_dragon[i]
            d1=dialogueFont.render(finaldialogue,False,BLACK)
            screen.blit(d1,(dboxX+50,dboxY+50))
            display.flip()
            myClock.tick(60)
        
        
            mpos=mixer.music.get_pos()
            
            
                
        
            
                
        time.wait(1000)
                
                

###############################################



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
final4_wyvern=" ".join(dlist_wyvern[3])
xywyvern=[] 
def wyvern():
    size=width,height=1280,900
    screen=display.set_mode(size)
    mixer.music.load("Sounds\\wyvern.mp3")
    mixer.music.play(-1)
    pics=[]
    x=0
    j=4.5
    y=(1/4*(1/20*x)**2)+25
    health=300
    maxhealth=300
    for i in range(1,12,1):
        pics.append(image.load("wyvern"+str(i)+".png"))
        pics[i-1]=transform.flip(pics[i-1],1,0)
    
    active=False
    active2=False
    ##########
    MAXRAPID=2
    rapid=MAXRAPID

    targets=[]
    midtargets=[]
    smtargets=[]

    score=0


    death=False
    slow=False
    ghost=False
    powerupchance=2400

    fastduration=0
    slowduration=0
    xduration=0
    ghostduration=0

    slowballs=[]
    gunfastballs=[]
    xballs=[]
    ghostballs=[]

    bullets=[]
    
    lvl=6
    powerupchance=2400
    maxtarg=14

    targets.append([randint(100,1180),0,xspeed,pi/2,randint(tmin,tmax),True])
    targets.append([randint(100,1180),0,xspeed,pi*2/3,randint(tmin,tmax),True])
    targets.append([-70,xspeed,6,pi/2,randint(tmin,tmax),False])
    targets.append([1350,0,-xspeed,pi/2,randint(tmin,tmax),False])
    ######
    frame=0
    frameDelay=6
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                quit()
    
        mb=mouse.get_pressed()
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

        mx,my=mouse.get_pos()
        guy=[mx,770]

        if len(targets)*4+len(midtargets)*2+len(smtargets)<maxtarg:
            lr=randint(1,2)
            if lr==1:
                targets.append([-30,100,6,pi/2,randint(tmin,tmax),False])
            else:
                targets.append([1310,100,-6,pi/2,randint(tmin,tmax),False])

        powerup=randint(0,powerupchance)
        lr=randint(1,2)
        
        if powerup==1 and len(gunfastballs)==0:
            if lr==1:
                gunfastballs.append([-30,100,6,pi/2,False])
            else:
                gunfastballs.append([1310,100,-6,pi/2,False])
        if powerup==2 and len(slowballs)==0:
            if lr==1:
                slowballs.append([-30,100,6,pi/2,False])
            else:
                slowballs.append([1310,100,-6,pi/2,False])
        if powerup==3 and len(xballs)==0:
            if lr==1:
                xballs.append([-30,100,6,pi/2,False])
            else:
                xballs.append([1310,100,-6,pi/2,False])

        if powerup==4 and len(ghostballs)==0:
            if lr==1:
                ghostballs.append([-30,100,6,pi/2,False])
            else:
                ghostballs.append([1310,100,-6,pi/2,False])

        if fastduration>0:
            MAXRAPID=1
        else:
            MAXRAPID=2

        if slowduration>0:
            slow=True
        else:
            slow=False

        if rapid>=MAXRAPID:
            if xduration>0:
                bullets.append([guy[0]-10,guy[1]-20,0,-25])
                bullets.append([guy[0]+10,guy[1]-20,0,-25])
            else:
                bullets.append([guy[0],guy[1]-20,0,-25])
            rapid=0
        else:
            rapid+=1

        if ghostduration>0:
            ghost=True
        else:
            ghost=False

        if death==False:
            maxtarg=moveBalls(targets,lvl,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,slow)
            drawScene(screen,score,guy,bullets,targets,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,ghostduration,lvl3back,ghost,health,maxhealth,pics[int(frame)],(width/2-50+x,y))
            health=checkhealth(maxhealth,health,bullets,pics[int(frame)],(width/2-50+x),y)
            moveBullets(bullets)
            score=checkHits(bullets,targets,midtargets,smtargets,score)
            fastduration=gunfastcheck(gunfastballs,guy,fastduration)
            slowduration=slowcheck(slowballs,guy,slowduration)
            xduration=xcheck(xballs,guy,xduration)
            ghostduration=ghostcheck(ghostballs,guy,ghostduration)
            death=checkDeath(targets,midtargets,smtargets,guy,ghost)
            if health<=0:
                donelevels.add(6)
                xywyvern.append(x)
                xywyvern.append(y)
                death_wyvern()
                running=False
                endtext=lolfont.render("WINNER!!!",True,BLACK)
                screen.blit(endtext,(550,400))
                endscore=lolfont.render("Score: "+str(score),True,BLACK)
                screen.blit(endscore,(570,450))
                display.flip()                            
                time.wait(1000)
                hub()
        else:
            
            
        
            
            endtext=lolfont.render("GAME OVER",True,BLACK)
            screen.blit(endtext,(550,400))
            endscore=lolfont.render("Score: "+str(score),True,BLACK)
            screen.blit(endscore,(570,450))
            nexttxt=lolfont.render("Back to hub (Left Click)",True,BLACK)
            screen.blit(nexttxt,(520,500))
            if mb[0]==1:
                hub()
            
            

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
        myClock.tick(30)
    fontSize2=5
    for i in range(len(final2_wyvern)):
        finaldialogue2+=final2_wyvern[i]
        d1=dialogueFont.render(finaldialogue2,True,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50+20))
        display.flip()
        myClock.tick(30)
    time.wait(1000)
 
def death_wyvern():
    
    pics=[]
    x=0
    mixer.music.load("Sounds\\victory.mp3")
    mixer.music.play(0)
    try:
        for i in range(1,4,1):
            pics.append(image.load("wyverndeath"+str(i)+".png"))
    except:
        pass
    frame=0
    frameDelay=6
    running=True
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        
            
        screen.blit(lvl3back,(0,0))
        try:
            screen.blit(pics [int(frame)],(xywyvern[0],xywyvern[1]))
        except:
            pass
        
        frameDelay-=1
        if frameDelay==0:
            frameDelay=20
            
            frame+=1
        if frame==3:
            
            wyverndeath_dialogue()
            
            
        mpos=mixer.music.get_pos()
        if mpos>=5190:
            hub()       
                
        
        myClock.tick(60)
        display.flip()
def wyverndeath_dialogue():
        finaldialogue=""
        finaldialogue2=""
        screen.blit(dbox,(dboxX,dboxY))
        for i in range (len(final3_wyvern)):
            finaldialogue+=final3_wyvern[i]
            d1=dialogueFont.render(finaldialogue,False,BLACK)
            screen.blit(d1,(dboxX+50,dboxY+50))
            display.flip()
            myClock.tick(20)
        for i in range (len(final4_wyvern)):
            finaldialogue+=final4_wyvern[i]
            d1=dialogueFont.render(finaldialogue,False,BLACK)
            screen.blit(d1,(dboxX+50,dboxY+50))
            display.flip()
            myClock.tick(40)
        time.wait(1000)
        hub()

################################################
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
    size=width,height=1280,900
    screen=display.set_mode(size)
    mixer.music.load("Sounds\\robot.mp3")
    mixer.music.play(-1)
    pics=[]
    pics2=[]
    frame=0
    frameDelay=6
    x=5
    j=9
    y = 100*sin(1/70*(x - pi/4))+100
    health=500
    maxhealth=500
    active=False
    active2=False
    active3=False
    ############
    MAXRAPID=2
    rapid=MAXRAPID
    score=0
    targets=[]
    midtargets=[]
    smtargets=[]
    death=False
    slow=False
    ghost=False
    powerupchance=2400
    fastduration=0
    slowduration=0
    xduration=0
    ghostduration=0
    slowballs=[]
    gunfastballs=[]
    xballs=[]
    ghostballs=[]
    bullets=[]
    lvl=9
    powerupchance=3000
    maxtarg=15
    targets.append([randint(100,1180),0,xspeed,pi/2,randint(tmin,tmax),True])
    targets.append([randint(100,1180),0,xspeed,pi*2/3,randint(tmin,tmax),True])
    targets.append([randint(100,1180),0,xspeed,pi*3/4,randint(tmin,tmax),True])
    targets.append([-70,xspeed,6,pi/2,randint(tmin,tmax),False])
    targets.append([1350,0,-xspeed,pi/2,randint(tmin,tmax),False])
    ############
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

        if frame>8:  
            x+=j
        y = 100*sin(1/70*(x - pi/4))+100
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
        if not active and frame>=8:
            
            screen.blit(lvl4back,(0,0))
            screen.blit(pics2 [0],(width/2-50+x,y))
            dialogue_witch()
            active=True
        
        if health<=0 and not active2:
            xywitch.append(width/2-50+x)
            xywitch.append(y)

        mx,my=mouse.get_pos()
        guy=[mx,770]

        if len(targets)*4+len(midtargets)*2+len(smtargets)<maxtarg:
            lr=randint(1,2)
            if lr==1:
                targets.append([-30,100,6,pi/2,randint(tmin,tmax),False])
            else:
                targets.append([1310,100,-6,pi/2,randint(tmin,tmax),False])

        powerup=randint(0,powerupchance)
        lr=randint(1,2)
        
        if powerup==1 and len(gunfastballs)==0:
            if lr==1:
                gunfastballs.append([-30,100,6,pi/2,False])
            else:
                gunfastballs.append([1310,100,-6,pi/2,False])

        if powerup==2 and len(slowballs)==0:
            if lr==1:
                slowballs.append([-30,100,6,pi/2,False])
            else:
                slowballs.append([1310,100,-6,pi/2,False])

        if powerup==3 and len(xballs)==0:
            if lr==1:
                xballs.append([-30,100,6,pi/2,False])
            else:
                xballs.append([1310,100,-6,pi/2,False])

        if powerup==4 and len(ghostballs)==0:
            if lr==1:
                ghostballs.append([-30,100,6,pi/2,False])
            else:
                ghostballs.append([1310,100,-6,pi/2,False])

        if fastduration>0:
            MAXRAPID=1
        else:
            MAXRAPID=2

        if slowduration>0:
            slow=True
        else:
            slow=False

        if rapid>=MAXRAPID:
            if xduration>0:
                bullets.append([guy[0]-10,guy[1]-20,0,-25])
                bullets.append([guy[0]+10,guy[1]-20,0,-25])
            else:
                bullets.append([guy[0],guy[1]-20,0,-25])
            rapid=0
        else:
            rapid+=1

        if ghostduration>0:
            ghost=True
        else:
            ghost=False
        if frame<8:
                screen.blit(pics [int(frame)],(width/2-50+x,y)) ###start up sprite
        if death==False and frame>8:
            maxtarg=moveBalls(targets,lvl,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,slow)
            drawScene(screen,score,guy,bullets,targets,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,ghostduration,lvl4back,ghost,health,maxhealth,pics[int(frame)-9],(width/2-50+x,y))
            health=checkhealth(maxhealth,health,bullets,pics[int(frame)-9],(width/2-50+x),y)
            moveBullets(bullets)
            score=checkHits(bullets,targets,midtargets,smtargets,score)
            fastduration=gunfastcheck(gunfastballs,guy,fastduration)
            slowduration=slowcheck(slowballs,guy,slowduration)
            xduration=xcheck(xballs,guy,xduration)
            ghostduration=ghostcheck(ghostballs,guy,ghostduration)
            death=checkDeath(targets,midtargets,smtargets,guy,ghost)
            
            if health<=0:
                donelevels.add(9)
                xywitch.append(x)
                xywitch.append(y)
                
                death_witch()
                running=False
                endtext=lolfont.render("WINNER!!!",True,BLACK)
                screen.blit(endtext,(550,400))
                endscore=lolfont.render("Score: "+str(score),True,BLACK)
                screen.blit(endscore,(570,450))
                display.flip()                            
                time.wait(1000)
                hub()
        else:

            endtext=lolfont.render("GAME OVER",True,BLACK)
            screen.blit(endtext,(550,400))
            endscore=lolfont.render("Score: "+str(score),True,BLACK)
            screen.blit(endscore,(570,450))
            nexttxt=lolfont.render("Back to hub (Left Click)",True,BLACK)
            screen.blit(nexttxt,(520,500))
            if mb[0]==1:
                hub()
            
            

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
        myClock.tick(10)
    time.wait(100)
def deathdialogue_witch():
    finaldialogue=""
    screen.blit(dbox,(dboxX,dboxY))
    for i in range (len(final3_witch)):
        
        finaldialogue+=final3_witch[i]
        d1=dialogueFont.render(finaldialogue,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50))
        display.flip()
        myClock.tick(10)
    time.wait(1000)
    hub()
def death_witch():
    pics=[]
    y=0
    mixer.music.load("Sounds\\victory.mp3")
    mixer.music.play()
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
            
        myClock.tick(60)
        display.flip()
#################################################################################################################################################################################################################################

###MASTER
dialogue_master=open("dialogue_master.txt","r")
dialogue_master=dialogue_master.readlines()
dlist_master=[]

for i in dialogue_master:
    d=i.strip().split(" ")
    dlist_master.append(d)
final_master=" ".join(dlist_master[0])
final2_master=" ".join(dlist_master[1])
final3_master=" ".join(dlist_master[2])
final4_master=" ".join(dlist_master[3])
final5_master=" ".join(dlist_master[4])
xymaster=[]
xymaster2=[]
xymaster3=[]
xymaster4=[]
healthmaster=[100]
def master():
    size=1280,900
    screen=display.set_mode(size)
    active=False
    pathactive1=False
    pathactive2=False
    pathactive3=False
    frame=0
    frameDelay=6
    mixer.music.pause()
    health=100
    running=True
    #####
    MAXRAPID=2
    rapid=MAXRAPID

    score=0
        
    targets=[]
    midtargets=[]
    smtargets=[]

    maxtarg=12

    death=False
    slow=False
    ghost=False
    powerupchance=2400

    fastduration=0
    slowduration=0
    xduration=0
    ghostduration=0

    slowballs=[]
    gunfastballs=[]
    xballs=[]
    ghostballs=[]

    bullets=[]

    targets.append([randint(100,1180),0,xspeed,pi/2,randint(tmin,tmax),True])
    targets.append([-70,xspeed,6,pi/2,randint(tmin,tmax),False])
    targets.append([1350,0,-xspeed,pi/2,randint(tmin,tmax),False])
    #####
    while running:
            
            for evt in event.get():
                if evt.type==QUIT:
                    running=False
            
            if not pathactive1:
                masterpath1()
                pathactive1=True
                
            if not pathactive2:
                masterpath2 (x,y)
                pathactive2=True
            if not pathactive3:
                masterpath3(x,y)
                pathactive3=True
def masterpath1():
    j=10
    xb=0
    yb=10
    yz=100
    xz=10
    x=0
    y=1
    health=750
    maxhealth=750
    bosspic=image.load("master.png")
    MAXRAPID=2
    rapid=MAXRAPID
    score=0
    targets=[]
    midtargets=[]
    smtargets=[]

    death=False
    slow=False
    ghost=False

    lvl=12
    powerupchance=3600
    maxtarg=16

    fastduration=0
    slowduration=0
    xduration=0
    ghostduration=0

    slowballs=[]
    gunfastballs=[]
    xballs=[]
    ghostballs=[]

    bullets=[]

    targets.append([randint(100,1180),0,xspeed,pi/2,randint(tmin,tmax),True])
    targets.append([randint(100,1180),0,xspeed,pi*2/3,randint(tmin,tmax),True])
    targets.append([randint(100,1180),0,xspeed,pi*3/4,randint(tmin,tmax),True])
    targets.append([-70,xspeed,6,pi/2,randint(tmin,tmax),False])
    targets.append([1350,0,-xspeed,pi/2,randint(tmin,tmax),False])
    active=False
    
    running=True
    while running:
                    
        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        
        bosspic=image.load("master.png")
        bosspic=transform.rotate(bosspic,x)
        
        if not active:
            screen.blit(lvl5back,(0,0))
            screen.blit(bosspic,(xb+width/2,yz))
            dialogue_master()
            active=True
        #horizontal mvment
        xb+=yb
        if xb>350 or xb<-700 :
            yb*=-1
        
        ##vert movememtner
        yz+=xz
        if yz>150:
            xz*=-1
        if yz<0:
            xz*=-1
        ##rotation
        x+=y
        if x>60:
            y*=-1
        if x<-60:
            y*=-1
        mx,my=mouse.get_pos()
        guy=[mx,770]

        if len(targets)*4+len(midtargets)*2+len(smtargets)<maxtarg:
            lr=randint(1,2)
            if lr==1:
                targets.append([-30,100,6,pi/2,randint(tmin,tmax),False])
            else:
                targets.append([1310,100,-6,pi/2,randint(tmin,tmax),False])

        powerup=randint(0,powerupchance)
        lr=randint(1,2)
        
        if powerup==1 and len(gunfastballs)==0:
            if lr==1:
                gunfastballs.append([-30,100,6,pi/2,False])
            else:
                gunfastballs.append([1310,100,-6,pi/2,False])

        if powerup==2 and len(slowballs)==0:
            if lr==1:
                slowballs.append([-30,100,6,pi/2,False])
            else:
                slowballs.append([1310,100,-6,pi/2,False])

        if powerup==3 and len(xballs)==0:
            if lr==1:
                xballs.append([-30,100,6,pi/2,False])
            else:
                xballs.append([1310,100,-6,pi/2,False])

        if powerup==4 and len(ghostballs)==0:
            if lr==1:
                ghostballs.append([-30,100,6,pi/2,False])
            else:
                ghostballs.append([1310,100,-6,pi/2,False])

        if fastduration>0:
            MAXRAPID=1
        else:
            MAXRAPID=2

        if slowduration>0:
            slow=True
        else:
            slow=False

        if rapid>=MAXRAPID:
            if xduration>0:
                bullets.append([guy[0]-10,guy[1]-20,0,-25])
                bullets.append([guy[0]+10,guy[1]-20,0,-25])
            else:
                bullets.append([guy[0],guy[1]-20,0,-25])
            rapid=0
        else:
            rapid+=1

        if ghostduration>0:
            ghost=True
        else:
            ghost=False
        
        if death==False:
            maxtarg=moveBalls(targets,lvl,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,slow)
            drawScene(screen,score,guy,bullets,targets,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,ghostduration,lvl5back,ghost,health,maxhealth,bosspic,(xb+width/2,yz))
            health=checkhealth(maxhealth,health,bullets,bosspic,(xb+width/2),y)
            moveBullets(bullets)
            score=checkHits(bullets,targets,midtargets,smtargets,score)
            fastduration=gunfastcheck(gunfastballs,guy,fastduration)
            slowduration=slowcheck(slowballs,guy,slowduration)
            xduration=xcheck(xballs,guy,xduration)
            ghostduration=ghostcheck(ghostballs,guy,ghostduration)
            death=checkDeath(targets,midtargets,smtargets,guy,ghost)
            
            if health<=0:
                donelevels.add(12)

                running=False
        else:
            

            endtext=lolfont.render("GAME OVER",True,BLACK)
            screen.blit(endtext,(550,400))
            endscore=lolfont.render("Score: "+str(score),True,BLACK)
            screen.blit(endscore,(570,450))
            nexttxt=lolfont.render("Back to hub (Left Click)",True,BLACK)
            screen.blit(nexttxt,(520,500))
            if mb[0]==1:
                hub()
        myClock.tick(60)
        display.flip()
        
def masterpath2(x,y):
    
    j=5
    health=500
    maxhealth=500
    bosspic=image.load("master.png")
    
    MAXRAPID=2
    rapid=MAXRAPID

    score=0
        
    targets=[]
    midtargets=[]
    smtargets=[]

    maxtarg=12

    death=False
    slow=False
    ghost=False
    powerupchance=2400

    fastduration=0
    slowduration=0
    xduration=0
    ghostduration=0

    slowballs=[]
    gunfastballs=[]
    xballs=[]
    ghostballs=[]

    bullets=[]

    targets.append([randint(100,1180),0,xspeed,pi/2,randint(tmin,tmax),True])
    targets.append([-70,xspeed,6,pi/2,randint(tmin,tmax),False])
    targets.append([1350,0,-xspeed,pi/2,randint(tmin,tmax),False])
    running=True
    while running:
        
        for evt in event.get():
            if evt.type==QUIT:
                running=False
            
        mb=mouse.get_pressed()
           
        
        
        x+=j
        y=100*sin(1/30*(x - pi/4))+100
        
        
        if x<-580 or x>550:
            j*=-1
        
        mx,my=mouse.get_pos()
        guy=[mx,770]

        if len(targets)*4+len(midtargets)*2+len(smtargets)<maxtarg:
            lr=randint(1,2)
            if lr==1:
                targets.append([-30,100,6,pi/2,randint(tmin,tmax),False])
            else:
                targets.append([1310,100,-6,pi/2,randint(tmin,tmax),False])

        powerup=randint(0,powerupchance)
        lr=randint(1,2)
        
        if powerup==1 and len(gunfastballs)==0:
            if lr==1:
                gunfastballs.append([-30,100,6,pi/2,False])
            else:
                gunfastballs.append([1310,100,-6,pi/2,False])

        if powerup==2 and len(slowballs)==0:
            if lr==1:
                slowballs.append([-30,100,6,pi/2,False])
            else:
                slowballs.append([1310,100,-6,pi/2,False])

        if powerup==3 and len(xballs)==0:
            if lr==1:
                xballs.append([-30,100,6,pi/2,False])
            else:
                xballs.append([1310,100,-6,pi/2,False])

        if powerup==4 and len(ghostballs)==0:
            if lr==1:
                ghostballs.append([-30,100,6,pi/2,False])
            else:
                ghostballs.append([1310,100,-6,pi/2,False])

        if fastduration>0:
            MAXRAPID=1
        else:
            MAXRAPID=2

        if slowduration>0:
            slow=True
        else:
            slow=False

        if rapid>=MAXRAPID:
            if xduration>0:
                bullets.append([guy[0]-10,guy[1]-20,0,-25])
                bullets.append([guy[0]+10,guy[1]-20,0,-25])
            else:
                bullets.append([guy[0],guy[1]-20,0,-25])
            rapid=0
        else:
            rapid+=1

        if ghostduration>0:
            ghost=True
        else:
            ghost=False
        
        if death==False:
            maxtarg=moveBalls(targets,lvl,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,slow)
            drawScene(screen,guy,bullets,targets,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,lvl5back,ghost)
            
            screen.blit(bosspic,(x+width/2,y))
            
            health=checkhealth(maxhealth,health,bullets,bosspic,x,y)
            moveBullets(bullets)
            score=checkHits(bullets,targets,midtargets,smtargets,score)
            fastduration=gunfastcheck(gunfastballs,guy,fastduration)
            slowduration=slowcheck(slowballs,guy,slowduration)
            xduration=xcheck(xballs,guy,xduration)
            ghostduration=ghostcheck(ghostballs,guy,ghostduration)
            death=checkDeath(targets,midtargets,smtargets,guy,ghost)
            scoretext=lolfont.render(str(score),True,WHITE)
            screen.blit(scoretext,(5,0))
            if health<=0:
                

                running=False
        else:
            
            
        
            
            endtext=lolfont.render("GAME OVER",True,BLACK)
            screen.blit(endtext,(550,400))
            endscore=lolfont.render("Score: "+str(score),True,BLACK)
            screen.blit(endscore,(570,450))
            nexttxt=lolfont.render("Back to hub (Left Click)",True,BLACK)
            screen.blit(nexttxt,(520,500))
            if mb[0]==1:
                hub()
        myClock.tick(60)
        display.flip()
def masterpath3(x,y):
    j=1
    
    
    health=500
    maxhealth=500
    x=(-1/5*(1/2*((y-100)**2))+600)*j
    bosspic=image.load("master.png")
    MAXRAPID=2
    rapid=MAXRAPID
    
    score=0

    maxtarg=12

    death=False
    slow=False
    ghost=False
    powerupchance=2400

    fastduration=0
    slowduration=0
    xduration=0
    ghostduration=0

    slowballs=[]
    gunfastballs=[]
    xballs=[]
    ghostballs=[]

    bullets=[]

    targets.append([randint(100,1180),0,xspeed,pi/2,randint(tmin,tmax),True])
    targets.append([-70,xspeed,6,pi/2,randint(tmin,tmax),False])
    targets.append([1350,0,-xspeed,pi/2,randint(tmin,tmax),False])
    running=True
    while running:
        
        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        mb=mouse.get_pressed()
        
            
        
             
            
        
        y+=j
        x=(-1/5*(1/2*((y-100)**2))+600)*j
        
        if x<-600 or x>600:
            j*=-1
        
        mx,my=mouse.get_pos()
        guy=[mx,770]

        if len(targets)*4+len(midtargets)*2+len(smtargets)<maxtarg:
            lr=randint(1,2)
            if lr==1:
                targets.append([-30,100,6,pi/2,randint(tmin,tmax),False])
            else:
                targets.append([1310,100,-6,pi/2,randint(tmin,tmax),False])

        powerup=randint(0,powerupchance)
        lr=randint(1,2)
        
        if powerup==1 and len(gunfastballs)==0:
            if lr==1:
                gunfastballs.append([-30,100,6,pi/2,False])
            else:
                gunfastballs.append([1310,100,-6,pi/2,False])

        if powerup==2 and len(slowballs)==0:
            if lr==1:
                slowballs.append([-30,100,6,pi/2,False])
            else:
                slowballs.append([1310,100,-6,pi/2,False])

        if powerup==3 and len(xballs)==0:
            if lr==1:
                xballs.append([-30,100,6,pi/2,False])
            else:
                xballs.append([1310,100,-6,pi/2,False])

        if powerup==4 and len(ghostballs)==0:
            if lr==1:
                ghostballs.append([-30,100,6,pi/2,False])
            else:
                ghostballs.append([1310,100,-6,pi/2,False])

        if fastduration>0:
            MAXRAPID=1
        else:
            MAXRAPID=2

        if slowduration>0:
            slow=True
        else:
            slow=False

        if rapid>=MAXRAPID:
            if xduration>0:
                bullets.append([guy[0]-10,guy[1]-20,0,-25])
                bullets.append([guy[0]+10,guy[1]-20,0,-25])
            else:
                bullets.append([guy[0],guy[1]-20,0,-25])
            rapid=0
        else:
            rapid+=1

        if ghostduration>0:
            ghost=True
        else:
            ghost=False
        
        if death==False:
            maxtarg=moveBalls(targets,lvl,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,slow)
            drawScene(screen,guy,bullets,targets,midtargets,smtargets,gunfastballs,slowballs,xballs,ghostballs,lvl5back,ghost)
            screen.blit(lvl5back,(0,0))
            screen.blit(bosspic,(x+width/2,yz))
            
            health=checkhealth(maxhealth,health,bullets,bosspic,x,y)
            moveBullets(bullets)
            score=checkHits(bullets,targets,midtargets,smtargets,score)
            fastduration=gunfastcheck(gunfastballs,guy,fastduration)
            slowduration=slowcheck(slowballs,guy,slowduration)
            xduration=xcheck(xballs,guy,xduration)
            ghostduration=ghostcheck(ghostballs,guy,ghostduration)
            death=checkDeath(targets,midtargets,smtargets,guy,ghost)
            scoretext=lolfont.render(str(score),True,WHITE)
            screen.blit(scoretext,(5,0))
            if health<=0:

                running=False
        else:
            
            
        
            
            endtext=lolfont.render("GAME OVER",True,BLACK)
            screen.blit(endtext,(550,400))
            endscore=lolfont.render("Score: "+str(score),True,BLACK)
            screen.blit(endscore,(570,450))
            nexttxt=lolfont.render("Back to hub (Left Click)",True,BLACK)
            screen.blit(nexttxt,(520,500))
            if mb[0]==1:
                hub()
        myClock.tick(60)
        display.flip()

def dialogue_master():
    finaldialogue=""
    finaldialogue2=""
    finaldialogue3=""
    screen.blit(dbox,(dboxX,dboxY))
    for i in range (len(final_master)):
        finaldialogue+=final_master[i]
        d1=dialogueFont.render(finaldialogue,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50))
        display.flip()
        myClock.tick(60)
    for i in range(len(final2_master)):
        finaldialogue2+=final2_master[i]
        d1=dialogueFont.render(finaldialogue2,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50+20))
        display.flip()
        myClock.tick(60)
    for i in range(len(final3_master)):
        finaldialogue3+=final3_master[i]
        d1=dialogueFont.render(finaldialogue3,False,BLACK)
        screen.blit(d1,(dboxX+50,dboxY+50+20+20))
        display.flip()
        myClock.tick(60)
    time.wait(1000)
    mixer.music.load("Sounds\\master.mp3")
    mixer.music.play(-1)
def death_master(x,y):
    pics=[]
    x=0
    active=False
    try:
        for i in range(1,5,1):
            pics.append(image.load("explosion"+str(i)+".png"))
    except:
        pass
    
    frame=0
    frameDelay=6
    
    running=True
    mixer.music.load("Sounds\\mastervictory.mp3")
    mixer.music.play(1)
    
    while running:

        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        
            
        screen.blit(lvl5back,(0,0))
        screen.blit(pics [int(frame)],(x,y))       
        if not active:
            masterdeath_dialogue()
            
            active=True
        x-=10
        frameDelay-=1
        if frameDelay==0:
            frameDelay=4
            
            frame+=1
        if frame==4:
            frame=4
        mpos=mixer.music.get_pos()
        if mpos>=5100 and x<0:
            
        
            
            endstory()
            
        myClock.tick(60)
        display.flip()
        
        
def masterdeath_dialogue():
        finaldialogue=""
        running=True
        screen.blit(dbox,(dboxX,dboxY))
        
        for i in range(len(final4_master)):
            finaldialogue+=final4_master[i]
            d1=dialogueFont.render(finaldialogue,False,BLACK)
            screen.blit(d1,(dboxX+50,dboxY+50))
            display.flip()
            myClock.tick(60)
        for i in range(len(final5_master)):
            finaldialogue+=final5_master[i]
            d1=dialogueFont.render(finaldialogue,False,BLACK)
            screen.blit(d1,(dboxX+50,dboxY+50))
            display.flip()
            myClock.tick(5)
        
            mpos=mixer.music.get_pos()
#############################################################################################################################################################################################################
                                #           BASICALLY IDK WHY THERE ARE 3 MASTER PATHS AND WHY ALL OF THEM HAVE WHILE RUNNING LOOPS BECAUSE IT CRASHES WHEN YOU DIE
                
        
            
                
        time.wait(1000)
#################
def endstory(): ###################################################################################################################################################################################
    mixer.music.load("Sounds\\story.mp3")
    mixer.music.set_volume(0.2)
    mixer.music.play()
    
    storyFont=font.SysFont("Comic Sans MS",fontSize)
    y=800
    text=open("endstory.txt","r")
    storyline=text.readlines()
    x=1
    h=0
    splist=[]
##    for i in storyline:
##        sp=i.strip().split(" ")
##        
##        splist.append(sp)
        
    fade = 0 ###################################################################################################################################################################################
    R=0 ###################################################################################################################################################################################
    startx=170
    running = True
    myClock = time.Clock()
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                
                menu()
                
        p=mixer.music.get_pos()
        if p>=46800:
            mixer.music.fadeout(1000)
        if h>-1200:
            h-=1
        screen.blit(endback,(0,h))
        
                
        if y>-400:
            y-=1.0
        
        storyFont=font.SysFont("Comic Sans MS",int(fontSize))
        line1=storyFont.render(storyline[0][0:-2],False,(R,R,R))
        
        line2=storyFont.render(storyline[1][0:-1],False,(R,R,R))
        line3=storyFont.render(storyline[2][0:-1],False,(R,R,R))
        line4=storyFont.render(storyline[3][0:-1],False,(R,R,R))
        
        screen.blit(line1,(startx,int(y)))
        screen.blit(line2,(startx,int(y+30)))
        screen.blit(line3,(startx,int(y+60)))
        screen.blit(line4,(startx,int(y+90)))
        

        display.flip()
                
############################
#master
        
def hub():
    mixer.music.load("Sounds\\hub.mp3")
    mixer.music.play(-1)
    size=800,900
    screen=display.set_mode(size)
    pos=len(donelevels) #go to last unlocked level position
    px, py = stagelist[pos].x-18, stagelist[pos].y-80 ###################################################################################################################################################################################
    pt1=1
    pt2=1

    running=True
    while running:
        pr=False
        click = False
        for evt in event.get():
            if evt.type==QUIT:
                quit()

            if evt.type==MOUSEBUTTONDOWN:
                click=True
            if evt.type==KEYDOWN:
                pr=True

                
        score=str(4561216) ###################################################################################################################################################################################
        
        keys=key.get_pressed()

        #navigating through unlocked levels
        if keys[K_UP] and pos<(len(donelevels)) and pr:
            pos += 1
            px, py = stagelist[pos].x-18, stagelist[pos].y-80
        if keys[K_DOWN] and pos>0 and pr:
            pos -= 1
            px, py = stagelist[pos].x-18, stagelist[pos].y-80
        #levels ellipses
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
        #level name
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
        
        
        lvltxt=lolfont.render((lvlval),False,BLACK)
        scoretxt=lolfont.render(score,False,BLACK)
        screen.blit(scoretxt,(400,800))
        screen.blit(lvltxt,(10,800))
        screen.blit(guy,(px,py))
        #entering each level
        if pos==0 and keys[K_RETURN]:
            story()
        if pos==1 and keys[K_RETURN]:
            level(1)
        if pos==2 and keys[K_RETURN]:
            level(2)
        if pos==3 and keys[K_RETURN]:
            dragon()
        if pos==4 and keys[K_RETURN]:
            level(4)
        if pos==5 and keys[K_RETURN]:
            level(5)
        if pos==6 and keys[K_RETURN]:
            wyvern()
        if pos==7 and keys[K_RETURN]:
            level(7)
        if pos==8 and keys[K_RETURN]:
            level(8)
        if pos==9 and keys[K_RETURN]:
            witch()
        if pos==10 and keys[K_RETURN]:
            level(10)
        if pos==1 and keys[K_RETURN]:
            level(11)
        if pos==12 and keys[K_RETURN]:
            master()
        display.flip()



def dialogue1():
    dialoguetxt=open("dialogue.txt","r")
    dialoguetxt=dialoguetxt.read()
    finaldialogue=""
    dbox=image.load("txtbox.png") ###################################################################################################################################################################################
    screen.blit(dbox,(100,600))
    for i in range (len(dialoguetxt)):
        finaldialogue+=dialoguetxt[i]
        d1=dialogueFont.render(finaldialogue,False,WHITE)
        screen.blit(d1(150,600))
        
        
    





def story(): ###################################################################################################################################################################################
    size=width,height=1280,900
    screen=display.set_mode(size)
    
    mixer.music.load("Sounds\\story.mp3")
    mixer.music.set_volume(0.2)
    mixer.music.play()
    
    storyFont=font.SysFont("Comic Sans MS",fontSize)
    y=800
    text=open("story.txt","r")
    storyline=text.readlines()
    x=1
    h=0
    hval=1
    yval=1
    splist=[]
    for i in storyline:
        sp=i.strip().split(" ")
        
        splist.append(sp)
        final=" ".join(splist[0])
    fade = 0
    R=0
    startx=170
    running = True
    myClock = time.Clock()
    while running:
        for evt in event.get():
            if evt.type == QUIT:
              
                menu()
        mb=mouse.get_pressed()
        if mb[0]==1:
            hval=10
            yval=10
        else:
            hval=1
            yval=1
        p=mixer.music.get_pos()
        if p>=46800:
            mixer.music.fadeout(1000)
        if h>-1200:
            h-=hval
        screen.blit(startback,(0,h))
        
                
        if y>-400:
            y-=yval
        
        storyFont=font.SysFont("Comic Sans MS",int(fontSize))
        line1=storyFont.render(storyline[0][0:-2],False,(R,R,R))
        
        line2=storyFont.render(storyline[1][0:-1],False,(R,R,R))
        line3=storyFont.render(storyline[2][0:-1],False,(R,R,R))
        line4=storyFont.render(storyline[3][0:-1],False,(R,R,R))
        line5=storyFont.render(storyline[4][0:-1],False,(R,R,R))
        screen.blit(line1,(startx,int(y)))
        screen.blit(line2,(startx,int(y+30)))
        screen.blit(line3,(startx,int(y+60)))
        screen.blit(line4,(startx,int(y+90)))
        screen.blit(line5,(startx,int(y+120)))

        display.flip()
        if p>=46850 or y<-401:
            knight() ###################################################################################################################################################################################

def credit():
    x=250
    y=100
    running = True

    
    line1=lvlFont.render("Game Mechanics - Tanzim",True,BLACK)
    line2=lvlFont.render("Character Design - Dylan",True,BLACK)
    line3=lvlFont.render("        Music - Dylan",True,BLACK)
    line4=lvlFont.render("        Menu - Dylan",True,BLACK)
    line5=lvlFont.render("Everything Else - Dylan",True,BLACK)
    

    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "menu"
                
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        screen.blit(menuback,(0,0))
        screen.blit(line1,(x,y))
        screen.blit(line2,(x,y+75))
        screen.blit(line3,(x,y+150))
        screen.blit(line4,(x,y+225))
        screen.blit(line5,(x,y+300))

        display.flip()

def menu():
    
    mixer.init()
    mixer.music.load("Sounds\\menu.mp3")
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)
    running = True
    myClock = time.Clock()
    
    
    buttons=[Rect(((width/2)-startpic.get_width()/2),200,(startpic.get_width()),100),
             Rect(((width/2)-controlpic.get_width()/2),305,(controlpic.get_width()),100),
             Rect(((width/2)-exitpic.get_width()/2),410,(exitpic.get_width()),100)]
    vals = ["story","credit","exitpic"]
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"
    
        mpos = mouse.get_pos()
        mb=mouse.get_pressed()
        
        screen.blit(menuback,(0,0))
        screen.blit(startpic,((width/2)-startpic.get_width()/2,195))
        screen.blit(controlpic,((width/2)-controlpic.get_width()/2,305))
        screen.blit(exitpic,((width/2)-exitpic.get_width()/2,400))
        screen.blit(titlepic,((width/2)-titlepic.get_width()/2,10))

    
        
        for i in range(len(buttons)):
            
            if buttons[i].collidepoint(mpos):
                draw.rect(screen,(0,255,0),buttons[i],2)
                if mb[0]==1:
                    return vals[i]
            else:
                draw.rect(screen,(255,255,0),buttons[i],2)
                
            
           
        display.flip()


screen = display.set_mode((width, height))
running = True
x,y = 0,0
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    elif page == "story":
        page = hub()
    elif page == "credit":
        page = credit()
    elif page == "exitpic":
        page = "exit"
    
quit()


###################################################################################################################################################################################
