from pygame_functions import *
import math, random, time, pickle

screenSize(1000,1000)
setBackgroundColour("black")


class Creature:
    def __init__(self,x,y,image,  size, ranking, powerUp):
        self.x = x
        self.y = y
        self.size = size   # size is a percentage of the full size image
        self.ranking = ranking
        self.speed = random.randint(5,15)
        self.angle = random.randint(1,360)
        self.powerUp = powerUp
        
        
        self.sprite = makeSprite(image)
        moveSprite(self.sprite,self.x,self.y,centre=True)
        transformSprite(self.sprite, self.angle, self.size/100)
        showSprite(self.sprite)
    
    def move(self):
        xSpeed = self.speed * math.cos(self.angle/180*math.pi)
        ySpeed = self.speed * math.sin(self.angle/180*math.pi)
        self.x = (self.x + xSpeed) % 1000
        self.y = (self.y + ySpeed) % 1000
        moveSprite(self.sprite,self.x,self.y, centre = True)


class Player(Creature):
    def __init__(self,x,y,image,size,ranking,powerUp):
        super().__init__(x,y,image,size, ranking, powerUp)
        
    
    def move(self):
        xPos = mouseX()
        yPos = mouseY()
        angle = math.atan2(xPos,yPos)math.pi * 180
        speed = 0


setAutoUpdate(False)
creatures = []

for i in range(15):
    creatures.append(Creature(random.randint(0,1000),random.randint(0,1000), "realenemy.png", random.randint(10,100),0,0))

p1 = Player(random.randint(0,1000), random.randint(0,1000), "player1.png", random.randint(10,100),0,0)

updateDisplay()

while(True):
    for c in creatures:
        c.move()
    updateDisplay()
    tick(50)
        
endWait()

