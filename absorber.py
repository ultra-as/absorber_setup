from pygame_functions import *
import math, random, time, pickle

height = 1000
width = 1000

screenSize(height,width)
setBackgroundColour("black")


class Creature:
    def __init__(self,x,y,image,  size, ranking):
        self.x = x
        self.y = y
        self.size = size   # size is a percentage of the full size image
        self.ranking = ranking
        self.speed = random.randint(2,6)
        self.angle = random.randint(1,360)
        self.powerUp = random.randint(1,10)
        self.lastInArea = 0
        self.runAwayChance = 0
        self.runTowardsChance = 0
        self.stayChance = 100
        self.radius = False
        self.choice = 1000
        self.follow = False
        self.mRadius = (self.size/2)+180
        
        
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
        
    def dropPUp(self,powerUpList):
        powerUps = {1: "speed", 2: "size"}
        if(self.powerUp in powerUps):
            print(powerUps[self.powerUp])
            if(powerUps[self.powerUp] == "speed"):
                print("sp")
                p = powerUp(self.x+100,self.y,"trailBoost.png",30,0,self.powerUp)
            else:
                print("si")
                p = powerUp(self.x+100,self.y,"trail.png",30,0,self.powerUp)
            
            powerUpList.append(p)

        
class trailC(Creature):
    def __init__(self,x,y,image,size,ranking):
        super().__init__(x,y,image,size,ranking)
        self.speed = 0
     
    
    
class powerUp(Creature):
    def __init__(self,x,y,image,size,ranking,pUp):
        super().__init__(x,y,image,size,ranking)
        self.speed = 0
        self.pUp = pUp
        
        



class Player(Creature):
    def __init__(self,x,y,image,size,ranking):
        super().__init__(x,y,image,size, ranking)
        self.powerUp = 0
        self.lastTrail = clock()
        self.trailTimer = 1000
        self.trailImg = "trail.png"
        self.trailSize = 20
        self.now = clock()
        moveSprite(self.sprite,500,500,centre=True)
        self.end = False
        self.boost = 1
        self.boostTimer = 0
        self.animState = 0
        self.lastAnim = 0
        self.animFrames = []
        self.animFrames.append(pygame.image.load("player1.png"))
        self.animFrames.append(pygame.image.load("player2.png"))
        self.image = self.animFrames[self.animState]
        self.pUpBoost = 1
        self.pUpSecond = 0
        self.lastPUp = -3000
        self.invincible = False
        self.invincibility = True
        self.ending = False

        
    
    def move(self, creatures,powerUpList,movePUps,pointers):
        if(not self.end):
            if(self.now > 3000):
                self.invincibility = False
                
            if((self.now - self.boostTimer) >= 500):
                self.trailTimer = 1000
                self.trailImg = "trail.png"
                self.trailSize = 20
                self.boost = 1
            self.now = clock()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_k):
                        print(not self.invincible)
                        self.invincible = not self.invincible
                if(event.type == pygame.MOUSEBUTTONUP and event.button == 3):
                    print("yes")
                    if(self.boostTimer == 0 or self.now - self.boostTimer >= 10000):
                        self.trailTimer = 150
                        self.trailImg = "trailBoost.png"
                        self.trailSize = 15
                        self.boost = 2
                        self.boostTimer = clock()
                    
                
        
            if(self.boostTimer != 0 and (self.now - self.boostTimer) <= 10000 and (self.now - self.boostTimer)%1000 <= 15):
                print(f"{10-((self.now-self.boostTimer)//1000)} seconds left")
            xPos = mouseX() - 500
            yPos = mouseY() - 500
            distance = math.sqrt(xPos**2 + yPos**2)
            self.speed = (distance / 200 * 10)*self.boost
            self.speed += self.speed*self.pUpBoost
            self.angle = math.degrees(math.atan2(yPos,xPos))
            
            transformSprite(self.sprite,self.angle,self.size/100)
            
            xSpeed = self.speed * math.cos(self.angle/180*math.pi)
            ySpeed = self.speed * math.sin(self.angle/180*math.pi)
            self.x = (self.x + xSpeed) % (width*10)
            self.y = (self.y + ySpeed) % (height*10)
            
         

            for c in creatures:
                minCreatureVal = c.size
                if(touching(self.sprite,c.sprite)):
                    if(self.size > c.size):
                        print("Nom")
                        creatures.remove(c)
                        hideSprite(c.sprite)
                        c.dropPUp(powerUpList)
                        if(not self.ending):
                            print("yes")
                            ranX = random.randint(0,10000)
                            ranY = random.randint(0,10000)
                            ranDist = ((abs(self.x-ranX))**2+(abs(self.y-ranY))**2)**0.5
                            actualDist = (self.size/2)+(c.size/2)
                            while(ranDist <= (actualDist+200)):
                                ranX = random.randint(0,10000)
                                ranY = random.randint(0,10000)
                                ranDist = ((abs(self.x-ranX))**2+(abs(self.y-ranY))**2)**0.5
                            
                            for c2 in creatures:
                                if(c2.size < minCreatureVal):
                                    minCreatureVal = c2.size
                            
                            if(minCreatureVal >= self.size):
                                creatures.append(Creature(ranX,ranY, "enemy2.png", (self.size+random.randint(-int(self.size*0.3),-int(self.size*0.1))),0))
                            
                            creatures.append(Creature(ranX,ranY, "enemy2.png", (self.size+random.randint(-int(self.size*0.3),int(self.size*0.3))),0))
                            
                        self.size += round(c.size*0.05)
                        if(self.size >= 100):
                            if(not self.ending):
                                sizeList = []
                                for cs in creatures:
                                    sizeList.append(cs.size)
                                
                                sizeList.sort()
                                currentSize = self.size
                                
                                for i in range(len(sizeList)-1):
                                    #print(i)
                                    if(currentSize > sizeList[i]):
                                        #print("smaller")
                                        currentSize += round(sizeList[i]*0.05)
                                        #print(currentSize)
                                    else:
                                        #print("bigger")
                                        while(currentSize <= sizeList[i]):
                                            #print("new creature")
                                            currentSize += round((currentSize*0.9)*0.05)
                                            randomX = random.randint(0,10000)
                                            randomY = random.randint(0,10000)
                                            ranDist = ((abs(self.x-randomX))**2+(abs(self.y-randomY))**2)**0.5
                                            while(ranDist <= ((self.x/2)+((self.x*0.9)/2)+200)):
                                                randomX = random.randint(0,10000)
                                                randomY = random.randint(0,10000)
                                                ranDist = ((abs(self.x-randomX))**2+(abs(self.y-randomY))**2)**0.5
                                            
                                            creatures.append(Creature(randomX,randomY,"enemy2.png",self.x*0.9,0))
                                            
                                
                            self.ending = True
                            if(len(creatures) == 0):
                                self.end = True
                            print(len(creatures))
                        print(self.size)
                    
                    
                    
                    elif(self.size < c.size):

                        
                        if(self.invincible or self.invincibility):
                            pass
                        else:
                            self.end = True
            
            for p in powerUpList:
                if(touching(self.sprite,p.sprite)):
                    powerUpList.remove(p)
                    hideSprite(p.sprite)
                    if(p.pUp == 1):
                        self.pUpBoost += 0.1
                    else:
                        self.size += round(self.size*0.05)
            
            self.spawnPUp(movePUps,pointers)
            self.pUpPoint(movePUps,pointers)
            
            
            
            for p in movePUps:
                if(touching(self.sprite,p.sprite)):
                    movePUps.remove(p)
                    pointer = pointers[0]
                    hideSprite(pointer.sprite)
                    pointers.remove(pointer)
                    hideSprite(p.sprite)
                    if(p.pUp == 1):
                        self.pUpBoost += 0.2
                    else:
                        self.size += round(self.size*0.05)
            
            for pointer in pointers:
                pointer.y = self.y-((self.size/2)+20)
                pointer.x = self.x
                xSpeed = pointer.speed * math.cos(pointer.angle/180*math.pi)
                ySpeed = pointer.speed * math.sin(pointer.angle/180*math.pi)
                pointer.x = (pointer.x + xSpeed) % (width*10)
                if(-((self.size/2)+20) <= (pointer.y + ySpeed) < 0):
                    pointer.y = (pointer.y + ySpeed)
                else:
                    pointer.y = (pointer.y + ySpeed) % (height*10)
                
                moveSprite(pointer.sprite,(500+(pointer.x - self.x)),(500+(pointer.y - self.y)), centre = True)
        
            
    
    def trail(self,trailList):
        diff = self.now - self.lastTrail
        if(diff >= self.trailTimer):
            self.lastTrail = clock()
            t = trailC(self.x,self.y,self.trailImg,self.trailSize,0)
            if(len(trailList) >= 20):
                gone = trailList.pop(0)
                hideSprite(gone.sprite)
            
            trailList.append(t)
    
    def close(self,creatures,radius):
        for c in creatures:
            #print(c.radius)
            #print("attempt")
            a = 0
            radius = c.mRadius
            c.choice = 1000
            dx = abs(self.x-c.x)
            dy = abs(self.y - c.y)
            dist = ((dx**2)+(dy**2))**0.5
            if(c.x <= (self.x + radius) and c.x >= (self.x - radius) and c.y <= (self.y + radius) and c.y >= (self.y - radius)):
            #if(dist <= 300):
                #print(c.choice)
                c.choice = random.randint(0,100)
                a = 1
                pass
            else:
                c.radius = False
                
            if(c.size < self.size):
                c.runAwayChance = 33+int(77*(c.size/self.size))
                c.runTowardsChance = c.runAwayChance+((77-int(77*(c.size/self.size)))//2)
                c.stayChance = 100
            elif(c.size == self.size):
                c.runAwayChance = 33
                c.runTowardsChance = c.runAwayChance + 33
                c.stayChance = c.runTowardsChance + 34
            else:
                c.runAwayChance = int(33*(self.size/c.size))
                c.runTowardsChance = 100-c.runAwayChance
                c.stayChance = 100
            
            """if(c.radius == False):
                c.follow = False
            elif(c.follow == True):
                c.choice = 100"""
            
            self.now = clock()
            
            if(c.choice <= c.runAwayChance):
                #print("hi")
                if(c.radius == False):
                    if(a == 1 and self.now - c.lastInArea >= 1000):
                        #print(f"a {c.choice}")
                        pass
                    #print(f"a {c.choice}")
                    if(self.now - c.lastInArea >= 1000):
                        self.runAway(creatures,radius)
                    c.radius = True
                    #print(c.choice)
                    #print("yes")
            elif(c.choice <= c.runTowardsChance):
                if(c.radius == False):
                    if(a==1 and self.now - c.lastInArea >= 1000):
                        #print(f"t {c.choice}")
                        pass
                    if(self.now - c.lastInArea >= 1000):
                        self.runTowards1(creatures,radius)
                    c.radius = True
            
            elif(c.choice <= c.stayChance):
                if(c.radius == False):
                    if(a==1):
                        #print(c.choice)
                        pass
                    c.radius = True
            
            
            """elif(c.choice <= c.runTowardsChance):
                #print(f"HI {c.choice}")
                if(c.radius == False):
                    if(a==1):
                        print(c.choice)
                    self.runTowards2(creatures,radius)
                    c.follow = True
                    c.radius = True
                elif(c.follow == True):
                    self.runTowards2(creatures,radius)"""
            
            if(c.x <= (self.x + radius) and c.x >= (self.x - radius) and c.y <= (self.y + radius) and c.y >= (self.y - radius)):
                c.lastInArea = clock()
            
            
    
    
    def runAway(self,creatures,radius): # makes creatures turn away when player is in certain radius
        for c in creatures:
            self.now = clock()
            #print(self.nowArea)
            #print(self.lastInArea)
            if(c.x <= (self.x + radius) and c.x >= (self.x - radius) and c.y <= (self.y + radius) and c.y >= (self.y - radius)):
                
                timeDif = self.now - c.lastInArea
                c.lastInArea = clock()
                if(timeDif >= 1000):
                    
                    #print(c.angle)
                    dx = self.x - c.x
                    dy = self.y - c.y
                    if(dx == 0):
                        if(dy <= 0):
                            c.angle = 270
                        else:
                            c.angle = 90
                    elif(dy == 0):
                        if(dx <= 0):
                            c.angle = 180
                        else:
                            c.angle = 0
                    else:
                        if(dx < 0):
                            dx = abs(dx)
                            if(dy < 0):
                                dy = abs(dy)
                                c.angle = (180+180+math.degrees(math.atan2(dy,dx)))%360
                                #print("I")
                            else:
                                c.angle = (180+90+math.degrees(math.atan2(dx,dy)))%360
                                #print("III")
                        else:
                            if(dy < 0):
                                dy = abs(dy)
                                c.angle = (180+270+math.degrees(math.atan2(dx,dy)))%360
                                #print("II")
                            else:
                                c.angle = (180+math.degrees(math.atan2(dy,dx)))%360
                                #print("IV")
                    
                    transformSprite(c.sprite, c.angle, c.size/100)
    
    def runTowards1(self,creatures,radius):
        for c in creatures:
            self.now = clock()
            #print(self.nowArea)
            #print(self.lastInArea)
            if(c.x <= (self.x + radius) and c.x >= (self.x - radius) and c.y <= (self.y + radius) and c.y >= (self.y - radius)):
                
                timeDif = self.now - c.lastInArea
                c.lastInArea = clock()
                if(timeDif >= 1000):
                    
                    #print(c.angle)
                    dx = self.x - c.x
                    dy = self.y - c.y
                    if(dx == 0):
                        if(dy <= 0):
                            c.angle = 270
                        else:
                            c.angle = 90
                    elif(dy == 0):
                        if(dx <= 0):
                            c.angle = 180
                        else:
                            c.angle = 0
                    else:
                        if(dx < 0):
                            dx = abs(dx)
                            if(dy < 0):
                                dy = abs(dy)
                                c.angle = (180+math.degrees(math.atan2(dy,dx)))%360
                                #print("I")
                            else:
                                c.angle = (90+math.degrees(math.atan2(dx,dy)))%360
                                #print("III")
                        else:
                            if(dy < 0):
                                dy = abs(dy)
                                c.angle = (270+math.degrees(math.atan2(dx,dy)))%360
                                #print("II")
                            else:
                                c.angle = (math.degrees(math.atan2(dy,dx)))%360
                                #print("IV")
                    
                    transformSprite(c.sprite, c.angle, c.size/100)
                
    
    def runTowards2(self,creatures,radius):
        for c in creatures:
            #self.now = clock()
            #print(self.nowArea)
            #print(self.lastInArea)
            if(c.x <= (self.x + radius) and c.x >= (self.x - radius) and c.y <= (self.y + radius) and c.y >= (self.y - radius)):
                
                #timeDif = self.now - c.lastInArea
                c.lastInArea = clock()
                #if(timeDif >= 100):
                    
                print(c.angle)
                dx = self.x - c.x
                dy = self.y - c.y
                if(dx == 0):
                    if(dy <= 0):
                        c.angle = 270
                    else:
                        c.angle = 90
                elif(dy == 0):
                    if(dx <= 0):
                        c.angle = 180
                    else:
                        c.angle = 0
                else:
                    if(dx < 0):
                        dx = abs(dx)
                        if(dy < 0):
                            dy = abs(dy)
                            c.angle = (180+math.degrees(math.atan2(dy,dx)))%360
                            #print("I")
                        else:
                            c.angle = (90+math.degrees(math.atan2(dx,dy)))%360
                            #print("III")
                    else:
                        if(dy < 0):
                            dy = abs(dy)
                            c.angle = (270+math.degrees(math.atan2(dx,dy)))%360
                            #print("II")
                        else:
                            c.angle = (math.degrees(math.atan2(dy,dx)))%360
                            #print("IV")
                
                transformSprite(c.sprite, c.angle, c.size/100)
                if(c.x <= (self.x + 5) and c.x >= (self.x - 5) and c.y <= (self.y + 5) and c.y >= (self.y - 5)):
                    c.speed = 0
                else:
                    c.speed = 3
    
    def anim(self):
        self.now = clock()
        interval = 500
        timeBetween = self.now - self.lastAnim
        
        if(timeBetween >= interval):
            #print("hi")
            self.lastAnim = clock()
            self.animState = (self.animState+1)%2
            self.image = self.animFrames[self.animState]
    
    
    def spawnPUp(self,pUps,pointers):
        self.now = clock()
        if(len(pointers) > 0):
            self.lastPUp = clock()
        if(len(pUps) == 0 and (self.now - self.pUpSecond) >= 1000 and (self.now - self.lastPUp) >= 5000):
            print("hi")
            self.pUpSecond = clock()
            spawn = random.randint(1,10)
            if(spawn == 1):
                self.lastPUp = clock()
                pointer = trailC(500,500-((self.size/2)+20),"enemy2.png",30,0)
                pointers.append(pointer)
                print("hi2")
                ranX = random.randint(0,10000)
                ranY = random.randint(0,10000)
                ranDist = ((abs(self.x-ranX))**2+(abs(self.y-ranY))**2)**0.5
                
                while(ranDist < 3000):
                    ranX = random.randint(0,10000)
                    ranY = random.randint(0,10000)
                    ranDist = ((abs(self.x-ranX))**2+(abs(self.y-ranY))**2)**0.5
                
                ranPUp = random.randint(1,2)
                
                if(ranPUp == 1):
                    p = powerUp(ranX,ranY,"trailBoost.png",60,0,ranPUp)
                else:
                    p = powerUp(ranX,ranY,"trail.png",60,0,ranPUp)
                print(ranX)
                print(ranY)
                pUps.append(p)
    
    def pUpPoint(self,pUps,pointers):
        if(len(pUps) == 1):
            pointer = pointers[0]
            p = pUps[0]
            dx = self.x - p.x
            dy = self.y - p.y
            if(dx == 0):
                if(dy <= 0):
                    pointer.angle = 270
                else:
                    pointer.angle = 90
            elif(dy == 0):
                if(dx <= 0):
                    pointer.angle = 180
                else:
                    pointer.angle = 0
            else:
                if(dx < 0):
                    dx = abs(dx)
                    if(dy < 0):
                        dy = abs(dy)
                        pointer.angle = (180+180+math.degrees(math.atan2(dy,dx)))%360
                        #print("I")
                    else:
                        pointer.angle = (180+90+math.degrees(math.atan2(dx,dy)))%360
                        #print("III")
                else:
                    if(dy < 0):
                        dy = abs(dy)
                        pointer.angle = (180+270+math.degrees(math.atan2(dx,dy)))%360
                        #print("II")
                    else:
                        pointer.angle = (180+math.degrees(math.atan2(dy,dx)))%360
                        #print("IV")
            
            transformSprite(pointer.sprite, pointer.angle, pointer.size/100)
        
        

    
    

def drawBorder(player):
    clearShapes()
    drawRect(500-player.x, 500-player.y, 10000,10000, (20,20,20),0)
    drawRect(500-player.x, 500-player.y, 10000,10000, (255,255,255),5)


setAutoUpdate(False)
creatures = []
trails = []
powerUps = []
movePUps = []
pointers = []
pSize = random.randint(30,60)
spawnRadius = 100

p1 = Player(300, 300, "player1.png", pSize,0)

for _ in range(20): # 20
    randX = random.randint(0,10000)
    randY = random.randint(0,10000)
    ranDist = ((abs(p1.x-randX))**2+(abs(p1.y-randY))**2)**0.5
    while(ranDist <= ((pSize/2)+(p1.size/2))+200):
        randX = random.randint(0,10000)
        randY = random.randint(0,10000)
        ranDist = ((abs(p1.x-randX))**2+(abs(p1.y-randY))**2)**0.5
    
    creatures.append(Creature(randX,randY, "enemy2.png", (pSize-(random.randint(1,11))),0))


for _ in range(10): # 10
    randX = random.randint(0,10000)
    randY = random.randint(0,10000)
    ranDist = ((abs(p1.x-randX))**2+(abs(p1.y-randY))**2)**0.5
    while(ranDist <= ((pSize/2)+(p1.size/2))+200):
        randX = random.randint(0,10000)
        randY = random.randint(0,10000)
        ranDist = ((abs(p1.x-randX))**2+(abs(p1.y-randY))**2)**0.5

    creatures.append(Creature(randX,randY, "enemy2.png", pSize,0))

for _ in range(20): # 20
    randX = random.randint(0,10000)
    randY = random.randint(0,10000)
    ranDist = ((abs(p1.x-randX))**2+(abs(p1.y-randY))**2)**0.5
    while(ranDist <= (((pSize+20)/2)+(p1.size/2))+200):
        randX = random.randint(0,10000)
        randY = random.randint(0,10000)
        ranDist = ((abs(p1.x-randX))**2+(abs(p1.y-randY))**2)**0.5
        
    creatures.append(Creature(randX,randY, "enemy2.png", (pSize+(random.randint(10,20))),0))

for _ in range(30): # 30
    randX = random.randint(0,10000)
    randY = random.randint(0,10000)
    ranDist = ((abs(p1.x-randX))**2+(abs(p1.y-randY))**2)**0.5
    while(ranDist <= (((pSize+220)/2)+(p1.size/2))+200):
        randX = random.randint(0,10000)
        randY = random.randint(0,10000)
        ranDist = ((abs(p1.x-randX))**2+(abs(p1.y-randY))**2)**0.5

    creatures.append(Creature(randX,randY, "enemy2.png", (pSize+(random.randint(50,220))),0))



#pygame.font.init()
#my_font = pygame.font.SysFont('Comic Sans MS', 30)


count = 0
while(not p1.end):
    for c in creatures:
        #text_surface = my_font.render(str(p1.size), False, (0, 0, 0))
        #screen.blit(text_surface, (0,0))
        #if(count%100 == 0):
            #print("C: " + str(c.x) + "\n" + str(c.y))
        c.move(p1)
    p1.move(creatures,powerUps,movePUps,pointers)
    for p in powerUps:
        p.move(p1)
    
    for p in movePUps:
        p.move(p1)
    
    
    p1.trail(trails)
    p1.close(creatures,300)
    p1.anim()
    for t in trails:
        t.move(p1)
    #if(count%100 == 0):
        #print("P: " + str(p1.x) + "\n" + str(p1.y))
    count += 1
    drawBorder(p1)
    updateDisplay()
    tick(50)
        
drawRect(500-p1.x, 500-p1.y, 10000,10000, (0,0,0),0)
drawRect(500-p1.x, 500-p1.y, 10000,10000, (255,255,255),5) # image background are black, which is visible when you die, stops this from being visible
endWait()

