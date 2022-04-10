from cmu_cs3_graphics import *
import time
import random
import math

class Zapper(object):
    
    def __init__(self, firstZapCoords, secondZapCoords):
        
        self.firstZapCoords = firstZapCoords
        self.secondZapCoords = secondZapCoords
        self.radius = 15
    
def onAppStart(app):
    app.rectLeft = 100
    app.rectTop = 200
    app.playerX = 30
    app.playerY = app.height/2
    app.playerR = 15
    app.circleVelocity = 0
    app.isSpaceHeld = False
    app.jetpackAcceleration = 0
    app.stepsPerSecond = 45
    app.ticks = 0
    app.speed = 5
    app.obstacleList = [ ]
    app.zapperR = 15
    
    # testing randomly picking an obstacle
    app.events = ['Missile', 'Zapper', 'Laser', 'Coins']
    print(random.choices(app.events, weights=(10, 70, 5, 15), k=1))

    

def onKeyHold(app, keys):
    if 'space' in keys:
        app.isSpaceHeld = True

def onKeyRelease(app, keys):
    if 'space' in keys:
        app.isSpaceHeld = False
        
        
# returns jetpack acceleration
def jetpack(app, key=None):
    if key == 'space':
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


# creates zapper obstacle
def createZapper(app):
    bounds = 100   
    firstZapX = app.width
    firstZapY = random.randint(bounds, app.height - bounds)
    secondZapDistance = random.randint(app.zapperR * 2, bounds)
    angle = random.choice([0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi,
                        5*math.pi/4, 3*math.pi/2, 7*math.pi/4, 2*math.pi])
    secondZapX = firstZapX + (secondZapDistance * math.cos(angle))
    secondZapY = firstZapY + (secondZapDistance * math.sin(angle))
    firstZapCoords = (firstZapX, firstZapY)
    secondZapCoords = (secondZapX, secondZapY)
    newZapper = Zapper(firstZapCoords, secondZapCoords)
    app.obstacleList.append(newZapper)

# returns distance between two points
def distance(x0, y0, x1, y1):
    return ((y1 - y0)**2 + (x1 - x0)**2)**0.5




# checks if player collides with any zappers
def checkZapperCollisions(app):
    for obstacle in app.obstacleList:
        
        firstZapX = obstacle.firstZapCoords[0]
        firstZapY = obstacle.firstZapCoords[1]

        # checking collisions of zap circles
        if (distance(app.playerX, app.playerY, firstZapX, firstZapY) <=
           (app.playerR + app.zapperR)):
            print('death skull emoji')
        secondZapX = obstacle.secondZapCoords[0]
        secondZapY = obstacle.secondZapCoords[1]
        if (distance(app.playerX, app.playerY, secondZapX, secondZapY) <=
           (app.playerR + app.zapperR)):
           print('death skull emoji')

        # checking collisions of zap line (currently broken)
        if obstacle.secondZapCoords[0] - obstacle.firstZapCoords[0] == 0:
            slope = 0
        else:
            slope = -((obstacle.secondZapCoords[1] - obstacle.firstZapCoords[1])
                    /(obstacle.secondZapCoords[0] - obstacle.firstZapCoords[0]))
        a = slope
        b = -1
        c = -(slope * obstacle.firstZapCoords[0]) + obstacle.firstZapCoords[1]
        dist = ((abs(a * app.playerX + b * app.playerY + c)) /
                math.sqrt(a ** 2 + b ** 2))
    
        if (app.playerR >= dist):
            print(dist)
        



# moves and deletes all the zappers every step
def moveAndDeleteZappers(app):
    i = 0        
    while i < len(app.obstacleList):
        obstacle = app.obstacleList[i]
        firstZapX = obstacle.firstZapCoords[0]
        secondZapX = obstacle.secondZapCoords[0]
        firstZapX -= app.speed
        secondZapX -= app.speed
        obstacle.firstZapCoords = (firstZapX, obstacle.firstZapCoords[1])
        obstacle.secondZapCoords = (secondZapX, obstacle.secondZapCoords[1])
        
        if obstacle.secondZapCoords[0] < 0:
            app.obstacleList.pop(i)
        else:
            i += 1

def onStep(app):
    app.ticks += 1


    if app.ticks % 40 == 0:
        createZapper(app)
    moveAndDeleteZappers(app)
    checkZapperCollisions(app)

    
    # adjusts player acceleration, velocity, and position
    if app.isSpaceHeld:
        jetpack(app, 'space')
    else:
        jetpack(app)
    acceleration = netAcceleration(app)
    dplayerY(app, acceleration)
    
def redrawAll(app):
    drawCircle(app.playerX, app.playerY, app.playerR)
    drawLabel(app.ticks // 10, app.width / 2, app.height / 2)
    
    # draws obstacles in obstacleList
    for obstacle in app.obstacleList:
        drawCircle(obstacle.firstZapCoords[0], obstacle.firstZapCoords[1],
                   obstacle.radius, fill='yellow')
        drawCircle(obstacle.secondZapCoords[0], obstacle.secondZapCoords[1],
                   obstacle.radius, fill='yellow')
        drawLine(obstacle.firstZapCoords[0], obstacle.firstZapCoords[1],
                 obstacle.secondZapCoords[0], obstacle.secondZapCoords[1])
    



def main():
    runApp(width=680, height=400)

main()