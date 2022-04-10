from cmu_cs3_graphics import *
import time
import random

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
    app.stepsPerSecond = 60
    app.ticks = 0
    app.speed = 5
    app.obstacleList = [ ]
    
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
    firstZapX = app.width
    firstZapY = random.randint(20, app.height - 50)
    secondZapX = firstZapX + random.choice([-15, 0, 15])
    secondZapY = firstZapY + random.randint(50, 200)
    while secondZapY < 0 or secondZapY > app.height:
        print(secondZapY)
        secondZapY = firstZapY + random.randint(50, 200)
    firstZapCoords = (firstZapX, firstZapY)
    secondZapCoords = (secondZapX, secondZapY)
    newZapper = Zapper(firstZapCoords, secondZapCoords)
    app.obstacleList.append(newZapper)


def onStep(app):
    app.ticks += 1
    if app.ticks % 40 == 0:
        createZapper(app)
    
    i = 0        
    while i < len(app.obstacleList):
        obstacle = app.obstacleList[i]
        print(obstacle.firstZapCoords)
        obstacle.firstZapCoords[0] -= app.speed
        obstacle.secondZapCoords[0] -= app.speed
        
        
        if obstacle.secondZapCoords[0] < 0:
            app.obstacleList.pop(i)
        else:
            i += 1

    
    # adjusts player acceleration, velocity, and position
    if app.isSpaceHeld:
        jetpack(app, 'space')
    else:
        jetpack(app)
    acceleration = netAcceleration(app)
    dplayerY(app, acceleration)
    


def main():
    runApp(width=680, height=400)

main()