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
        self.x = (self.x + xSpeed) % width
        self.y = (self.y + ySpeed) % height
        moveSprite(self.sprite,self.x,self.y, centre = True)


class Player(Creature):
    def __init__(self,x,y,image,size,ranking,powerUp):
        super().__init__(x,y,image,size, ranking, powerUp)
        
    
    def move(self, creatures):
        xPos = mouseX() - self.x
        yPos = mouseY() - self.y
        distance = math.sqrt(xPos**2 + yPos**2)
        self.speed = distance / 200 * 10
        self.angle = math.degrees(math.atan2(yPos,xPos))
        transformSprite(self.sprite,self.angle,self.size/100)
        super().move()
        
        for c in creatures:
            if(touching(self.sprite,c.sprite)):
                if(self.size > c.size):
                    print("Nom")
                    creatures.remove(c)
                    hideSprite(c.sprite)
                    self.size += 5
                elif(self.size < c.size):
                    print("Dead")
    
    


setAutoUpdate(False)
creatures = []

for i in range(5):
    creatures.append(Creature(random.randint(0,1000),random.randint(0,1000), "enemy1.png", random.randint(10,100),0,0))

p1 = Player(random.randint(0,1000), random.randint(0,1000), "player1.png", random.randint(10,100),0,0)

updateDisplay()

while(True):
    for c in creatures:
        c.move()
    p1.move(creatures)
    updateDisplay()
    tick(50)
        
endWait()

