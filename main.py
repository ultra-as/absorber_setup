from pygame_functions import *
import math, random, time, pickle

height = 1000
width = 1000

screenSize(height,width)
setBackgroundColour("black")


class Creature:
    def __init__(self,x,y,image,  size, ranking, powerUp):
        self.x = x
        self.y = y
        self.size = size   # size is a percentage of the full size image
        self.ranking = ranking
        self.speed = 0
        self.angle = random.randint(1,360)
        self.powerUp = powerUp
        
        
        self.sprite = makeSprite(image)
        moveSprite(self.sprite,self.x,self.y,centre=True)
        transformSprite(self.sprite, self.angle, self.size/100)
        showSprite(self.sprite)
    
    def move(self, player):
        if(not player.end):
            xSpeed = self.speed * math.cos(self.angle/180*math.pi)
            ySpeed = self.speed * math.sin(self.angle/180*math.pi)
            self.x = (self.x + xSpeed) % (width*10)
            self.y = (self.y + ySpeed) % (height*10)
            #self.x = (self.x - player.xPos) % (width*10)
            #self.y = (self.x - player.yPos) % (height*10)
            
            moveSprite(self.sprite,(500+(self.x - player.x)),(500+(self.y - player.y)), centre = True)
        
        
class trailC(Creature):
    def __init__(self,x,y,image,size,ranking,powerup):
        super().__init__(x,y,image,size,ranking,powerup)
        self.speed = 0
    
    


class Player(Creature):
    def __init__(self,x,y,image,size,ranking,powerUp):
        super().__init__(x,y,image,size, ranking, powerUp)
        self.lastTrail = clock()
        self.now = clock()
        moveSprite(self.sprite,500,500,centre=True)
        self.end = False

        
    
    def move(self, creatures):
        if(not self.end):
            self.now = clock()
                
            
            xPos = mouseX() - 500
            yPos = mouseY() - 500
            distance = math.sqrt(xPos**2 + yPos**2)
            self.speed = distance / 200 * 10
            self.angle = math.degrees(math.atan2(yPos,xPos))
            
            transformSprite(self.sprite,self.angle,self.size/100)
            
            xSpeed = self.speed * math.cos(self.angle/180*math.pi)
            ySpeed = self.speed * math.sin(self.angle/180*math.pi)
            self.x = (self.x + xSpeed) % (width*10)
            self.y = (self.y + ySpeed) % (height*10)
            
         

            
            for c in creatures:
                if(touching(self.sprite,c.sprite)):
                    if(self.size > c.size):
                        print("Nom")
                        creatures.remove(c)
                        hideSprite(c.sprite)
                        self.size += c.speed*0.2
                    elif(self.size < c.size):
                        self.end = True
    
    def trail(self,trailList):
        diff = self.lastTrail - self.now
        if(diff >= 1000):
            self.lastTrail = clock()
            t = trailC(self.x,self.y,"enemy1.png",10,0,0)
            if(len(trailList) >= 20):
                gone = trailList.pop(0)
                hideSprite(gone.sprite)
            
            trailList.append(t)
        
    
    

def drawBorder(player):
    clearShapes()
    drawRect(500-player.x, 500-player.y, 10000,10000, (20,20,20),0)
    drawRect(500-player.x, 500-player.y, 10000,10000, (255,255,255),5)


setAutoUpdate(False)
creatures = []
trails = []

for i in range(1):
    creatures.append(Creature(random.randint(0,10000),random.randint(0,10000), "enemy1.png", random.randint(15,150),0,0))

p1 = Player(5000, 5000, "player1.png", random.randint(30,40),0,0)


count = 0
while(not p1.end):
    for c in creatures:
        if(count%100 == 0):
            print("Creature: " + str(c.x) + "," + str(c.y))
        c.move(p1)
    p1.move(creatures)
    p1.trail(trails)
    for t in trails:
        t.move(p1)
    if(count%100 == 0):
        print("Player: " + str(p1.x) + "," + str(p1.y))
    count += 1
    drawBorder(p1)
    updateDisplay()
    tick(50)
        
endWait()

