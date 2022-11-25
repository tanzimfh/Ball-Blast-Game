from pygame import *
init()
BASE = "explosion"
pic1 = image.load(BASE+".png").convert(32,SRCALPHA)

wid,hi = pic1.get_size()
pic = Surface((wid+2,hi+2),SRCALPHA)
pic.blit(pic1,(1,1))
screen = display.set_mode(pic.get_size())
screen.fill((255,255,255))
screen.blit(pic,(0,0))

def lineHasPixel(pic,y):
    for x in range(wid):
        if pic.get_at((x,y))[3]>0:
            return True
    return False

def findPixelLine(pic,y):
    while y<hi and not lineHasPixel(pic,y):
        y+=1
    return y

def findOpenLine(pic,y):
    while y<hi and lineHasPixel(pic,y):
        y+=1
    return y

def colHasPixel(pic,top,bott,x):
    for y in range(top,bott+1):
        if pic.get_at((x,y))[3]>0:
            return True
    return False

def findPixelCol(pic,top,bott,x):
    while x<wid and not colHasPixel(pic,top,bott,x):
        x+=1
    return x

def findOpenCol(pic,top,bott,x):
    while x<wid and colHasPixel(pic,top,bott,x):
        x+=1
    return x

cnt=0
bott = 0
while bott<hi:
    top = findPixelLine(pic,bott)
    if top == hi:break
    bott = findOpenLine(pic,top)
    right = 0
    while right<wid:
        left = findPixelCol(pic,top,bott,right)
        if left == wid:break
        right = findOpenCol(pic,top,bott,left)
        cnt+=1
        image.save(pic.subsurface((left,top,right-left+1,bott-top+1)),"%s%01d.png" % (BASE, cnt))
        
        draw.rect(screen,(255,0,0),(left,top,right-left+1,bott-top+1),1)
        display.flip()
        
quit()
