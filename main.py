from pygame_functions import *
import math, random, time, pickle

screenSize(1000,1000)
setBackgroundColour("black")


class Creature:
    def __init__(self,x,y,image,  size, ranking, speed, powerUp):
        self.x = x
        self.y = y
        self.size = size   # size is a percentage of the full size image
        self.ranking = ranking
        self.speed = speed
        self.powerUp = powerUp
        
        
        self.sprite = makeSprite(image)
        moveSprite(self.sprite,self.x,self.y,centre=True)
        transformSprite(self.sprite, 0, self.size/100)
        showSprite(self.sprite)


class Player(Creature):
    def __init__(self,x,y,image,size,ranking,speed,powerUp):
        super().__init__(x,y,image,size, ranking, speed,powerUp)


setAutoUpdate(False)
c1 = Creature(random.randint(0,1000),random.randint(0,1000), "enemy1.png", random.randint(10,100),0,0,0)
p1 = Player(random.randint(0,1000), random.randint(0,1000), "player1.png", random.randint(10,100),0,0,0)

updateDisplay()
        
endWait()

