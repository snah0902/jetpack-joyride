from cmu_cs3_graphics import *
import time
import random
import math

class Zapper(object):
    
    def __init__(self, firstZapCoords, secondZapCoords):
        
        self.firstZapCoords = firstZapCoords
        self.secondZapCoords = secondZapCoords
        self.radius = 15
        
    
class Missile(object):

    def __init__(self, coords):
        self.coords = coords
        self.width = 60
        self.height = 25
        self.isTargeting = True
        self.timeUntilLaunch = 90

def onAppStart(app):
    app.rectLeft = 100
    app.rectTop = 200
    app.playerX = 225
    app.playerY = app.height/2
    app.playerR = 15
    app.circleVelocity = 0
    app.isSpaceHeld = False
    app.jetpackAcceleration = 0
    app.stepsPerSecond = 45
    app.ticks = 0
    app.speed = 5
    app.zapperList = [ ]
    app.missileList = [ ]
    app.missileAlertR = 15
    app.events = [True, False, False, False]
    (app.isMissile, app.isCoins, app.isLaser, app.isZapper) = (
        app.events[0], app.events[1], app.events[2], app.events[3])
    app.missileCount = app.coinsCount = app.laserCount = app.zapperCount = 0
    app.currentCoins = 0

    app.rows = 68
    app.cols = 40
    
# returns cell bounds (left, top, cellWidth, cellHeight)
def getCellBounds(app, row, col):
    gridWidth = 680
    gridHeight = 400
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    left = cellWidth * row
    top = cellHeight * col
    return left, top, cellWidth, cellHeight

def onKeyHold(app, keys):
    if 'space' in keys:
        app.isSpaceHeld = True

def onKeyRelease(app, keys):
    if 'space' in keys:
        app.isSpaceHeld = False
  
        
# returns jetpack acceleration
def jetpack(app):
    if app.isSpaceHeld:
        app.jetpackAcceleration = 0.5
    else:
        app.jetpackAcceleration = 0
    
# returns the net acceleration of player
def netAcceleration(app):
    gravityAcceleration = 0.25
    return gravityAcceleration - app.jetpackAcceleration

# changes y-position of player
def dplayerY(app, acceleration):
    
    # calculates velocity of player
    app.circleVelocity -= acceleration
    if app.circleVelocity > 12:
        app.circleVelocity = 12
    if app.circleVelocity < -6:
        app.circleVelocity = -6
    app.playerY -= app.circleVelocity
    
    # checks bounds
    if app.playerY - app.playerR <= 0:
        app.playerY = app.playerR
        app.circleVelocity = 0
    if app.playerY + app.playerR >= app.height:
        app.playerY = app.height - app.playerR
        app.circleVelocity = 0

# changes player acceleration, velocity, and position
def playerMovement(app):
    jetpack(app)
    acceleration = netAcceleration(app)
    dplayerY(app, acceleration)

# creates zapper obstacle
def createZapper(app):
    margin = 100   
    firstZapX = app.width
    firstZapY = random.randint(margin, app.height - margin)
    secondZapDistance = random.randint(30, margin)
    angle = random.choice([0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi,
                        5*math.pi/4, 3*math.pi/2, 7*math.pi/4, 2*math.pi])
    secondZapX = firstZapX + (secondZapDistance * math.cos(angle))
    secondZapY = firstZapY + (secondZapDistance * math.sin(angle))
    firstZapCoords = (firstZapX, firstZapY)
    secondZapCoords = (secondZapX, secondZapY)
    newZapper = Zapper(firstZapCoords, secondZapCoords)
    app.zapperList.append(newZapper)
    app.zapperCount -= 1

    if app.zapperCount == 0:
        app.events[3] = False

# returns distance between two points
def distance(x0, y0, x1, y1):
    return ((y1 - y0)**2 + (x1 - x0)**2)**0.5

# checks if player collides with any zappers
def checkZapperCollisions(app):
    for zapper in app.zapperList:
        
        firstZapX = zapper.firstZapCoords[0]
        firstZapY = zapper.firstZapCoords[1]

        # checking collisions of zap circles
        if (distance(app.playerX, app.playerY, firstZapX, firstZapY) <=
           (app.playerR + zapper.radius)):
            print('death skull emoji')
        secondZapX = zapper.secondZapCoords[0]
        secondZapY = zapper.secondZapCoords[1]
        if (distance(app.playerX, app.playerY, secondZapX, secondZapY) <=
           (app.playerR + zapper.radius)):
           print('death skull emoji')

        # checking collisions of zap line (currently broken)
        # if zapper.secondZapCoords[0] - zapper.firstZapCoords[0] == 0:
        #     slope = 0
        # else:
        #     slope = -((zapper.secondZapCoords[1] - zapper.firstZapCoords[1])
        #             /(zapper.secondZapCoords[0] - zapper.firstZapCoords[0]))
        # a = slope
        # b = -1
        # c = -(slope * zapper.firstZapCoords[0]) + zapper.firstZapCoords[1]
        # dist = ((abs(a * app.playerX + b * app.playerY + c)) /
        #         math.sqrt(a ** 2 + b ** 2))
    
        # if (app.playerR >= dist):
        #     print(dist)
    
# moves zappers every step, deletes off-screen zappers
def moveAndDeleteZappers(app):
    i = 0        
    while i < len(app.zapperList):
        obstacle = app.zapperList[i]
        firstZapX = obstacle.firstZapCoords[0]
        secondZapX = obstacle.secondZapCoords[0]
        firstZapX -= app.speed
        secondZapX -= app.speed
        obstacle.firstZapCoords = (firstZapX, obstacle.firstZapCoords[1])
        obstacle.secondZapCoords = (secondZapX, obstacle.secondZapCoords[1])
        
        if obstacle.secondZapCoords[0] < 0:
            app.zapperList.pop(i)
        else:
            i += 1

# draws zapper in zapperList
def drawZappers(app):
    for zapper in app.zapperList:
        drawCircle(zapper.firstZapCoords[0], zapper.firstZapCoords[1],
                   zapper.radius, fill='orange')
        drawCircle(zapper.secondZapCoords[0], zapper.secondZapCoords[1],
                   zapper.radius, fill='orange')
        drawLine(zapper.firstZapCoords[0], zapper.firstZapCoords[1],
                 zapper.secondZapCoords[0], zapper.secondZapCoords[1])




def createCoins(app):
    pass


def createMissile(app):
    missileX = app.width
    missileY = random.randint(0, app.height - 25)
    newMissile = Missile((missileX, missileY))
    app.missileList.append(newMissile)
    app.missileCount -= 1
    if app.missileCount == 0:
        app.events[0] = False


def moveAndDeleteMissiles(app):
    i = 0
    while i < len(app.missileList):
        missile = app.missileList[i]
        if missile.isTargeting:
            yCoord = missile.coords[1]
            if yCoord > app.playerY:
                if abs(yCoord - app.playerY) < app.speed / 2:
                    yCoord = app.playerY
                else:  
                    yCoord -= app.speed / 2
            elif yCoord < app.playerY:
                if abs(yCoord - app.playerY) < app.speed / 2:
                    yCoord = app.playerY
                yCoord += app.speed / 2

            missile.coords = (missile.coords[0], yCoord)
            missile.timeUntilLaunch -= 1
            if missile.timeUntilLaunch == 0:
                missile.isTargeting = False
            
        else:
            missileX = missile.coords[0]
            missileX -= 1.5 * app.speed
            missile.coords = (missileX, missile.coords[1])

        if missile.coords[0] + missile.width < 0:
            app.missileList.pop(i)
        else:
            i += 1

def checkMissileCollisions(app):
    for missile in app.missileList:
        xCoord = missile.coords[0]
        yCoord = missile.coords[1]
        nearestX = max(xCoord, min(app.playerX, xCoord + missile.width))
        nearestY = max(yCoord, min(app.playerY, yCoord + missile.height))
        if distance(app.playerX, app.playerY, nearestX, nearestY) < app.playerR:
            print('you die')

def drawMissiles(app):
    for missile in app.missileList:
        missileX = missile.coords[0]
        missileY = missile.coords[1]
        if missile.isTargeting:
            drawCircle(640, missileY + missile.height / 2, app.missileAlertR)
        else:
            drawRect(missileX, missileY, missile.width, missile.height, fill='red')

def onStep(app):
    app.ticks += 1
    if app.isZapper:
        if app.ticks % 40 == 0:
            createZapper(app)
    
    elif app.isCoins:
        pass
    
    elif app.isMissile:
        if app.ticks % 40 == 0:
            createMissile(app)



    moveAndDeleteZappers(app)
    checkZapperCollisions(app)        

    moveAndDeleteMissiles(app)
    checkMissileCollisions(app)

    if (app.missileCount == 0 and app.coinsCount == 0
        and app.laserCount == 0 and app.zapperCount == 0):
        randomIdx = random.choices([0, 1, 2, 3], weights=(10, 5, 70, 15), k=1)
        app.events[randomIdx[0]] = True
        
        if app.events[1]:
            app.events[1] = False
            app.events[0] = True
        elif app.events[2]:
            app.events[2] = False
            app.events[3] = True
        print(app.events)

        (app.isMissile, app.isCoins, app.isLaser, app.isZapper) = (
        app.events[0], app.events[1], app.events[2], app.events[3])
        if app.isZapper:
            app.zapperCount += random.randint(5, 10)
        elif app.isMissile:
            app.missileCount += random.randint(1, 6)

    playerMovement(app)

    
def redrawAll(app):

    drawCircle(app.playerX, app.playerY, app.playerR)
    drawLabel(app.ticks // 10, app.width / 2, app.height / 2)
    

    drawZappers(app)
    drawMissiles(app)

def main():
    runApp(width=680, height=400)

main()