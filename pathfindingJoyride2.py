from cmu_cs3_graphics import *
import time
import random
import math

class Zapper(object):
    def __init__(self, firstZapCoords, secondZapCoords, angle):
        
        self.firstZapCoords = firstZapCoords
        self.secondZapCoords = secondZapCoords
        self.angle = angle
        self.radius = 15
        
    
class Missile(object):

    def __init__(self, coords):
        self.coords = coords
        self.width = 45
        self.height = 25
        self.isTargeting = True
        self.timeUntilLaunch = 90
        self.isRotated = False
        self.timePathfinding = 0
        self.angle = 0
        self.isTargetingAgain = True

def onAppStart(app):

    app.rectLeft = 100
    app.rectTop = 200
    app.playerX = 250
    app.playerY = app.height/2
    app.playerR = 13
    app.stepsPerSecond = 45

    app.circleVelocity = 0
    app.isSpaceHeld = False
    app.jetpackAcceleration = 0
    app.stepsPerSecond = 45
    app.ticks = 0
    app.currentScore = 0
    app.highScore = 0
    app.speed = 4
    app.zapperList = [ ]
    app.missileList = [ ]
    app.missileAlertR = 15
    app.events = [False, False, False, False]
    (app.isMissile, app.isCoins, app.isLaser, app.isZapper) = (
        app.events[0], app.events[1], app.events[2], app.events[3])
    app.missileCount = app.coinsCount = app.laserCount = app.zapperCount = 0
    app.currentCoins = 0
    app.isDead = False

    app.missileImage = 'missile.png'
    app.rotatedMissileImage = 'rotatedMissile.png'
    app.warningImage = 'warning.png'
    app.flashingWarningImage = 'flashingWarning.png'
    app.paused = False

    app.rows = 68
    app.cols = 40
    app.grid = []
    app.possiblePath = []
    app.pathfind = False


# recursively finds any path that will get player to the end
def pathFinding(app, currentX, currentY, L):

    if currentX >= app.width:
        return L
    else:
        for dx, dy in ((app.playerR * 2, 0), (app.playerR, app.playerR * 2), (app.playerR, -app.playerR * 2)):
            if currentY + dy < 0 or currentY + dy >= app.height:
                continue
            if isValid(app, currentX + dx, currentY + dy):
                L.append((currentX + dx, currentY + dy))
                result = pathFinding(app, currentX + dx, currentY + dy, L)
                if result != None:
                    return result
                L.pop()

        return None

def isValid(app, playerX, playerY):
    if checkZapperCollisions(app, playerX, playerY) or checkMissileCollisions(app, playerX, playerY):
        return False
    return True

def onKeyPress(app, keys):
    if 'space' in keys:
        return
    if 'p' in keys:
        app.paused = not app.paused
    elif 'o' in keys:
        doStep(app)
    elif 'r' in keys:
        if app.isDead:
            restartGame(app)
            app.isDead = False
    elif 'l' in keys:
        app.pathfind = not app.pathfind

# resets necessary variables to start a new game
def restartGame(app):
    app.circleVelocity = 0
    app.isSpaceHeld = False
    app.jetpackAcceleration = 0
    app.ticks = 0
    app.currentScore = 0
    app.speed = 4
    app.zapperList = [ ]
    app.missileList = [ ]
    app.missileAlertR = 15
    app.events = [True, False, False, False]
    (app.isMissile, app.isCoins, app.isLaser, app.isZapper) = (
        app.events[0], app.events[1], app.events[2], app.events[3])
    app.missileCount = app.coinsCount = app.laserCount = app.zapperCount = 0
    app.currentCoins = 0

    app.grid = []
    app.possiblePath = []
    app.pathfind = False

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

# creates new zapper obstacle
def createZapper(app):
    margin = min(int(17 * app.speed + 32), 200)
    zapperR = 15
    firstZapX = app.width
    firstZapY = random.randint(zapperR, app.height - zapperR)
    secondZapDistance = random.randint(zapperR * 3, margin)

    # randomizes coords of second zapper based on first zapper coords
    if firstZapY < secondZapDistance:
        angle = random.choice([0, math.pi/4, math.pi/2])
    elif firstZapY > app.height - secondZapDistance:
        angle = random.choice([3*math.pi/2, 7*math.pi/4])
    else:
        angle = 0 # random.choice([0, math.pi/4, math.pi/2, 3*math.pi/2, 7*math.pi/4])
    secondZapX = firstZapX + (secondZapDistance * math.cos(angle))
    secondZapY = firstZapY + (secondZapDistance * math.sin(angle))
    firstZapCoords = (firstZapX, firstZapY)
    secondZapCoords = (secondZapX, secondZapY)

    # creates and makes new zapper
    newZapper = Zapper(firstZapCoords, secondZapCoords, angle)
    app.zapperList.append(newZapper)
    
    # tracks how many zappers left to create
    app.zapperCount -= 1
    if app.zapperCount == 0:
        app.events[3] = False

# returns distance between two points
def distance(x0, y0, x1, y1):
    return ((y1 - y0)**2 + (x1 - x0)**2)**0.5

# checks if player collides with any zappers
def checkZapperCollisions(app, playerX, playerY):

    for zapper in app.zapperList:
        
        firstZapX = zapper.firstZapCoords[0]
        firstZapY = zapper.firstZapCoords[1]
        secondZapX = zapper.secondZapCoords[0]
        secondZapY = zapper.secondZapCoords[1]

        # checking collisions of zap circles
        if (distance(playerX, playerY, firstZapX, firstZapY) <=
           (app.playerR + zapper.radius)):
            return True

        if (distance(playerX, playerY, secondZapX, secondZapY) <=
           (app.playerR + zapper.radius)):
           return True

        # checking collisions of zap lines
        largerX = max(firstZapX, secondZapX)
        smallerX = min(firstZapX, secondZapX)
        largerY = max(firstZapY, secondZapY)
        smallerY = min(firstZapY, secondZapY)

        if playerX + app.playerR >= smallerX and playerX - app.playerR <= largerX and playerY + app.playerR >= smallerY and playerY - app.playerR <= largerY:
            a = firstZapY - secondZapY
            b = secondZapX - firstZapX
            c = firstZapX * secondZapY - secondZapX * firstZapY
            dist = ((abs(a * playerX + b * playerY + c)) /
                math.sqrt(a **2 + b ** 2))
            if app.playerR >= dist:
                return True

    return False

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
        drawLine(zapper.firstZapCoords[0], zapper.firstZapCoords[1],
                 zapper.secondZapCoords[0], zapper.secondZapCoords[1])
        drawCircle(zapper.firstZapCoords[0], zapper.firstZapCoords[1],
                   zapper.radius, fill='orange')
        drawCircle(zapper.secondZapCoords[0], zapper.secondZapCoords[1],
                   zapper.radius, fill='orange')

# creates different patterns of coins
def createCoins(app):
    pass

# creates new missile obstacle
def createMissile(app):
    missileX = app.width
    missileY = random.randint(0, app.height - 25)
    newMissile = Missile((missileX, missileY))
    newMissile.timePathfinding = int(150 / app.speed)
    app.missileList.append(newMissile)
    app.missileCount -= 1
    if app.missileCount == 0:
        app.events[0] = False

# moves and deletes every missile on screen
def moveAndDeleteMissiles(app):
    i = 0
    while i < len(app.missileList):
        missile = app.missileList[i]
        
        # if missile is targeting, moves it a certain y-distance closer to player
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

            # stops targeting
            if missile.timeUntilLaunch == 25:
                missile.isTargeting = False
            
        # moves non-targeting missiles
        elif missile.timeUntilLaunch <= 0:
            missileX = missile.coords[0]
            missileY = missile.coords[1]       
            missileX -= 1.5 * app.speed
            missile.coords = (missileX, missile.coords[1])

        if missile.coords[0] + missile.width <= 0:
            app.missileList.pop(i)
        else:
            i += 1

        missile.timeUntilLaunch -= 1

# checks player to missile collisions
def checkMissileCollisions(app, playerX, playerY):
    for missile in app.missileList:
        xCoord = missile.coords[0] + 8
        yCoord = missile.coords[1] + 15
        nearestX = max(xCoord, min(playerX, xCoord + missile.width))
        nearestY = max(yCoord, min(playerY, yCoord + missile.height))
        if distance(playerX, playerY, nearestX, nearestY) < app.playerR:
            return True

    return False

# draws missiles on canvas
def drawMissiles(app):
    for missile in app.missileList:
        missileX = missile.coords[0]
        missileY = missile.coords[1]
        if missile.isTargeting:
                drawImage(app.warningImage, missileX + missile.width/2 - 75, missileY + missile.height/2, align='center')
        else:
            if missile.timeUntilLaunch < 25 and missile.timeUntilLaunch > 0:
                drawImage(app.flashingWarningImage, missileX + missile.width/2 - 75, missileY + missile.height/2, align='center')
            else:

                if missile.isRotated:
                    drawImage(app.rotatedMissileImage, missileX, missileY)
                else:
                    drawImage(app.missileImage, missileX, missileY)

def drawPath(app):
    if app.possiblePath == None:
        return
    for x, y in app.possiblePath:
        drawCircle(x, y, 3)


# updates high score if player beats it
def updateHighScore(app):
    if app.currentScore > app.highScore:
        app.highScore = int(app.currentScore)

# everything that should happen each step
def stepEvents(app):
    if app.isDead:
        return
    if app.ticks % 500 == 0:
        app.speed += 0.1
        app.speed = round(app.speed, 1)
    app.currentScore += int(app.speed) / 10
    app.ticks += 1
    
    if app.isZapper:
        if app.ticks % int(200 / app.speed) == 0:
            createZapper(app)
    
    elif app.isCoins:
        pass
    
    elif app.isMissile:
        if app.ticks % int(400 / app.speed) == 0:
            createMissile(app)



    updateHighScore(app)
    moveAndDeleteZappers(app)
    if checkZapperCollisions(app, app.playerX, app.playerY):
        app.isDead = True

    moveAndDeleteMissiles(app)
    if checkMissileCollisions(app, app.playerX, app.playerY):
        app.isDead = True


    if app.pathfind:
        app.possiblePath = (pathFinding(app, app.playerX, app.playerY, []))
        if app.possiblePath == None:
            app.pathfind = False


    if (app.missileCount == 0 and app.coinsCount == 0
        and app.laserCount == 0 and app.zapperCount == 0):
        randomIdx = random.choices([0, 1, 2, 3], weights=(10, 0, 0, 10), k=1)
        app.events[randomIdx[0]] = True
        
        if app.events[1]:
            app.events[1] = False
            app.events[0] = True
        elif app.events[2]:
            app.events[2] = False
            app.events[3] = True

        (app.isMissile, app.isCoins, app.isLaser, app.isZapper) = (
        app.events[0], app.events[1], app.events[2], app.events[3])
        if app.isZapper:
            app.zapperCount += random.randint(5, 10)
        elif app.isMissile:
            app.missileCount += random.randint(1, 6)

    playerMovement(app)

def doStep(app):
    stepEvents(app)

def onStep(app):
    if app.paused:
        return
    stepEvents(app)

    

def redrawAll(app):

    if app.isDead:
        drawLabel(f'You went {int(app.currentScore)} m!', 10, 20, align='left', size=15)
        drawLabel(f'Highscore: {app.highScore} m', 10, 50, align='left', size=15)
        drawLabel('I THIN KYOU PASS AWAY NOW.', app.width/2, app.height/2, size=30)
        drawLabel("Press 'r' to retry.", app.width/2, app.height/2 + 50)
        return

    if app.pathfind:
        drawPath(app)

    drawCircle(app.playerX, app.playerY, app.playerR)
    drawLabel(f'Ticks: {app.ticks}', app.width / 2, app.height / 2)
    drawLabel(f'Score: {int(app.currentScore)}', app.width / 2, app.height / 2 + 20)
    drawLabel(f'Speed: {app.speed}', app.width / 2, app.height / 2 + 40)
    
    

    drawZappers(app)
    drawMissiles(app)


def main():
    runApp(width=680, height=400)

main()
