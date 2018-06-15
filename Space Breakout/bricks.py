import pygame, os, sys
from pygame import *
import random as r
import globalVarsClass as gb
#GLOBALE  VARIABELEN
def main():
    pygame.init()
    pygame.display.set_mode((0,0))
    pygame.display.set_caption("Bricks")
    pygame.mouse.set_visible(0)
    pygame.mixer.music.load(os.path.join(gb.ASSETS_FOLDER,"8-bit-music-loop.wav"))
    gb.mainSurface.fill(gb.black)
    while gb.gameOn:
        pygame.mixer.music.play(-1)
        while gb.showMenu:
            showMenu()
            pygame.display.update()
            gb.FPSCLOCK.tick(10)
        gb.mainSurface.fill(gb.black)
        while gb.levelsPlaying:
            #backgrouns scrolling
            setDynamicBackground()
            #levens
            drawHUD()
            #events
            checkLevelEvents()
            if gb.changeBat:
                gb.mainSurface.blit(gb.batLangSprite, gb.batLangRect)
            if not gb.changeBat:
                gb.mainSurface.blit(gb.batSprite, gb.batRect)
            drawBricks()
            drawUpgrades()
            # teken pallet en bal
            if gb.ballServed:
                gb.bx -= gb.sx
                gb.by -=gb.sy
                gb.ballRect.topleft = (gb.bx,gb.by)
                gb.ballBigRect.topleft = (gb.bx,gb.by)
                checkBallCollides()
            if not gb.changeBall:
                gb.mainSurface.blit(gb.ballSprite, gb.ballRect)
            else:
                gb.ballBigRect.topleft = (gb.bx,gb.by)
                gb.mainSurface.blit(gb.ballBigSprite,gb.ballBigRect)
            # hoofdlogica
            # botsingen detecteren
            checkBallBatCollide()
            brickHitIndex = []
            if not gb.changeBall:
                brickHitIndex = gb.ballRect.collidelist(gb.bricksRects)
            else:
                brickHitIndex = gb.ballBigRect.collidelist(gb.bricksRects)
            if brickHitIndex >= 0: # geen botsing = -1
                if gb.changeBall and gb.scoreTemp > 4:
                    gb.scoreTemp += 4
                if not gb.changeBall and gb.scoreTemp > 2:
                    gb.scoreTemp += 2
                else:
                    gb.scoreTemp += 1
                hb = gb.bricksRects[brickHitIndex]
                for b in gb.bricks:
                    if b[-1] == 1 and b[-2]==hb:
                        upX,upY = hb[0],hb[1]
                        gb.upgradeRectList.append(( Rect(upX+8, (upY+int((hb.height/2)+8)),16,16),1))
                    elif b[-1] == 2 and b[-2]==hb:
                        upX,upY = hb[0],hb[1]
                        gb.upgradeRectList.append(( Rect(upX+8, (upY+int((hb.height/2)+8)),16,16),2))
                    elif b[-1] == 3 and b[-2]==hb:
                        upX,upY = hb[0],hb[1]
                        gb.upgradeRectList.append(( Rect(upX+8, (upY+int((hb.height/2)+8)),16,16),3))
                mx = gb.bx + 4
                if mx > hb.x + hb.width or mx < hb.x:
                    gb.sx *= -1
                else:
                    gb.sy *= -1
                del(gb.bricksRects[brickHitIndex])
            if not gb.bricksRects:
                gb.levelsPlaying = False
                gb.changeLevel = True
            pygame.display.update()
            gb.FPSCLOCK.tick(30) #FPS op juiste snelheid zetten
        gb.mainSurface.fill(gb.black)
        while gb.changeLevel:
            #draw backgroud
            showLevelChange()
            pygame.display.update()
            gb.FPSCLOCK.tick(30)
            gb.mainSurface.fill(gb.black)
        while gb.gameOverMenu:
            showGameOverMenu()
            pygame.display.update()
#######################################################################################################
#Shows the Game Over Screen.
#includes "Eindscore" & press space to play again
def showGameOverMenu():
    eindScore = gb.fontobjTITEL.render("Eindscore: " + str(gb.score), True, gb.white, None)
    gb.mainSurface.blit(gb.gameOverBg,(0,0))
    gb.mainSurface.blit(eindScore,(400-int(eindScore.get_width()/2),290))
    drawMultipleLines(gb.gameOverStringList,gb.white,270,50)
    for event in pygame.event.get():
        checkKeyQuit(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                resetForNewGame()
            elif event.key == pygame.K_ESCAPE:
                gb.gameOn = False
                pygame.quit()
                sys.exit()


#Shows the "Completed level" screen
#Ability to setup all variables needed in setupNextLevel()
def showLevelChange():
    relatief_X = gb.xBg % gb.mainSurface.get_rect().height
    gb.mainSurface.blit(gb.nextLevelBg,(relatief_X - gb.mainSurface.get_rect().width,0))
    if relatief_X < gb.WIDTH:
        gb.mainSurface.blit(gb.nextLevelBg, (relatief_X,0))
    gb.xBg += 1
    #draw labels
    levelLabel1 = gb.fontobjCOMBO.render("Congratulation!",True,gb.white,None)
    levelLabel2 = gb.fontobjCOMBO.render("You completed LEVEL "+ str(gb.level) + "!",True,gb.white,None)
    nextLevelLabel = gb.fontobjTITEL.render("proceed to next level, press SPACE..",True,gb.white,None)
    gb.mainSurface.blit(levelLabel1,(400-int(levelLabel1.get_width()/2),int(gb.HEIGHT/4)))
    gb.mainSurface.blit(levelLabel2,(400-int(levelLabel2.get_width()/2),int(gb.HEIGHT/4)+40))
    gb.mainSurface.blit(nextLevelLabel,(400-int(nextLevelLabel.get_width()/2),int(gb.HEIGHT/2)+50))
    for event in pygame.event.get():
        checkKeyQuit(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                setupNextLevel()


#Shows the Menu screen
#This screen only shown in beginning, ability to show instructions to the player
def showMenu():
    for event in pygame.event.get():
        checkKeyQuit(event)
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
            gb.showMenu = False
            gb.levelsPlaying = True
            gb.bricksRects,gb.bricks = createBricks(4,2,2)
    gb.mainSurface.blit(gb.bgMain,(0,0))
    gb.mainSurface.blit(gb.welkomLabel,(400-int(gb.welkomLabel.get_width()/2),50))
    drawMultipleLines(gb.stringMenuList,gb.white,gb.welkomLabel.get_width(),300)


#generates the bricksets in levels
#Returns 1 list of all bricks with ID's and 1 list with only Rectangles
#Ability to randomise
def createBricks(specials1PerLevel,specials2PerLevel,sleutels,height = gb.HEIGHT, width = gb.WIDTH):
    rands = specials1PerLevel*gb.level
    rands2 = specials2PerLevel*gb.level
    rands3 = sleutels
    bricksTemp,bricksRectsTemp,randomIndex1,randomIndex2,randomIndex3 = [],[],[],[],[]
    YrangeVoorX,YrangeVoorY = 4+gb.level,8+gb.level
    XrangeVoorX,XrangeVoorY = 5+gb.level,9+gb.level
    if(YrangeVoorY >= 20):
        YrangeVoorX,YrangeVoorY = 13,20
    if (XrangeVoorY >= 16):
        XrangeVoorX,XrangeVoorY = 13,16
    yRange = r.randrange(YrangeVoorX,YrangeVoorY)
    xRange = r.randrange(XrangeVoorX,XrangeVoorY) #max 16
    for i in range(rands):
        randomIndex1.append((r.randrange(xRange),r.randrange(yRange)))
    for i in range(rands2):
        randomIndex2.append((r.randrange(xRange),r.randrange(yRange)))
    for i in range(rands3):
        randomIndex3.append((r.randrange(xRange),r.randrange(yRange)))
    for y in range(yRange):
        brickY = (y * 16) -100 + ((height-(yRange*16))/2)
        for x in range(xRange):
            brickX = (x*48) + ((width-(xRange*48))/2)
            if gb.level >= 10:
                tekenkansY = r.randrange(0,2)
            else:
                tekenkansY = r.randrange(0,12-gb.level)
            if tekenkansY != 0 or (x,y) in randomIndex3: #100% kans voor 2 sleutels
                if (x,y) in randomIndex3:
                    bricksTemp.append((Rect(brickX,brickY,48,16),3)) #brick_sleutel
                elif (x,y) in randomIndex2:
                    bricksTemp.append((Rect(brickX,brickY,48,16),2)) #brick_geel
                elif(x,y) in randomIndex1:
                    bricksTemp.append((Rect(brickX,brickY,48,16),1)) #brick_blauw
                else:
                    bricksTemp.append((Rect(brickX,brickY,48,16),0)) #brick
                bricksRectsTemp.append(Rect(brickX,brickY,48,16))
    return bricksRectsTemp,bricksTemp


#Shows and Handles the Cheat menu
#ability to cheat using keyhandles & set show or hide cheat menu
def handleCheatMenu(event):
    if event.key == pygame.K_RETURN:
        if gb.showCheatKeys:
            gb.showCheatKeys = False
        else:
            gb.showCheatKeys = True
    if event.key == pygame.K_1:
        gb.scoreTemp +=1
    if event.key == pygame.K_2:
        del gb.bricksRects[0]
        gb.scoreTemp += 1
    if event.key == pygame.K_3:
        del(gb.bricksRects[:])
    if event.key == pygame.K_4:
        if(gb.lives < gb.maxLives):
            gb.lives += 1
    if event.key == pygame.K_5:
        gb.changeBall = True
    if event.key == pygame.K_6:
        gb.changeBat = True
    if event.key == pygame.K_7:
        if gb.ballSpeed < gb.ballMaxSpeed:
            gb.ballSpeed += 1
            if gb.sx < 0 and gb.sy < 0:
                gb.sx,gb.sy = (gb.ballSpeed,gb.ballSpeed)
            elif gb.sx > 0 and gb.sy > 0:
                gb.sx,gb.sy = (gb.ballSpeed,gb.ballSpeed)


#draws the Head-Up Display
#Hud includes: Lives, score, comboscore and levelindicator
def drawHUD():
    for i in range(gb.lives): #3 levens = 0,1,2
        x,y = ((gb.heartRect[2]*i)+5,5)
        gb.mainSurface.blit(gb.heartSprite,(x,y))
    #onscreen text
    scoreLabel = gb.fontobjTITEL.render(str(gb.score),True,gb.white,None)
    scoreComboLabel = gb.fontobjCOMBO.render("combo!  "+ str(gb.scoreTemp),True,gb.white,None)
    LevelindicatorLabel = gb.fontobj.render("Level:"+str(gb.level),True,gb.white,None)
    gb.mainSurface.blit(scoreLabel,(gb.WIDTH-scoreLabel.get_width()-5,5))
    if gb.DEVELOPER_TOOLS and gb.showCheatKeys:
        drawMultipleLines(gb.cheatStringList,gb.white)
    if gb.scoreTemp > 4 and gb.changeBall:
        gb.mainSurface.blit(scoreComboLabel,(400-int(scoreComboLabel.get_width()/2),6))
    if gb.scoreTemp > 2 and not gb.changeBall:
        gb.mainSurface.blit(scoreComboLabel,(400-int(scoreComboLabel.get_width()/2),6))
    gb.mainSurface.blit(LevelindicatorLabel,(0,gb.HEIGHT-LevelindicatorLabel.get_height()-10))


#sets up all variables for a New Game
#ability to create a new brickSet for the next New game
def resetForNewGame():
    gb.gameOverMenu = False
    gb.levelsPlaying = True
    gb.eindScore,gb.score,gb.scoreTemp = 0,0,0
    gb.lives = 3
    del gb.upgradeRectList[:]
    gb.ballServed = False
    gb.changeBall = False
    gb.ballSpeed = 4
    gb.sx,gb.y = (gb.ballSpeed,gb.ballSpeed)
    gb.level = 1
    gb.keyDown = ""
    gb.bricksRects,gb.bricks = createBricks(4,2,2)


#Create x amount of randoms between 0 and 9
#returns them in a list
def createRandoms(randoms):
    rands = []
    for i in range(randoms):
        rands.append(r.randrange(1,10))
    return rands


#checks all mouseEvents
#ability to change the bat, with ball served or not
def checkMouseEvents(event):
    gb.mouseX = event.pos[0] #mousex = X positie van de muis
    if(gb.mouseX < gb.WIDTH or gb.mouseX <= 0 ):#
        if gb.changeBat:
            gb.batLangRect.topleft = (gb.mouseX-int(gb.batLangRect[2]/2),gb.playerY)
            gb.ballRect.topleft = (gb.batLangRect[2]/2,gb.playerY)
        elif not gb.changeBat:
            gb.batRect.topleft = (gb.mouseX-int(gb.batRect[2]/2),gb.playerY)
            gb.ballRect.topleft = (gb.batRect[2]/2,gb.playerY)
    if not gb.ballServed:
        if gb.changeBat:
            if gb.changeBall:
                gb.bx,gb.by = (gb.mouseX-int(gb.ballBigRect[2]/2),gb.playerY-gb.batLangRect[3])
            elif not gb.changeBall:
                gb.bx,gb.by = (gb.mouseX-int(gb.ballRect[2]/2),gb.playerY-gb.batLangRect[3])
            gb.ballRect.topleft = (gb.bx,gb.by)
        elif not gb.changeBat:
            if gb.changeBall:
                gb.bx,gb.by = (gb.mouseX-int(gb.ballBigRect[2]/2),gb.playerY-gb.batRect[3])
            elif not gb.changeBall:
                gb.bx,gb.by = (gb.mouseX-int(gb.ballRect[2]/2),gb.playerY-gb.batRect[3])
            gb.ballRect.topleft = (gb.bx,gb.by)


#Dictionary with backgrouds
def bg(x):
    return ((gb.bg1,gb.bg2,gb.bg3,gb.bg4)[x])


#Sets and draws the dynamicBackgroud frame
#background slides down endlessly
def setDynamicBackground():
    lvl = gb.level
    background = bg(lvl%4)
    gbRect = bg(lvl%4).get_rect()
    relatief_Y = gb.yBg % gbRect.height
    gb.mainSurface.blit(background,(0,int(relatief_Y - gbRect.height)))
    if relatief_Y < gb.HEIGHT:
        gb.mainSurface.blit(background, (0,relatief_Y))
    gb.yBg += 1


#sets up and resets all variables
#ability to speed up the ballspeed and create new list
def setupNextLevel():
    gb.keyDown = ""
    gb.scoreTemp = 0
    gb.changeLevel = False
    gb.levelsPlaying = True
    gb.level += 1
    gb.yBg = 0
    del gb.upgradeRectList[:]
    gb.ballServed = False
    gb.changeBall = False
    if gb.ballSpeed <gb.ballMaxSpeed:
        gb.ballSpeed += 1
    gb.sx, gb.sy = (gb.ballSpeed, gb.ballSpeed)
    gb.bx,gb.by = (gb.mouseX-int(gb.ballRect[2]/2),gb.playerY-gb.batRect[3])
    gb.ballRect.topleft = (gb.bx,gb.by) = ((gb.WIDTH/2)-int(gb.ballRect[2]/2),gb.playerY-gb.ballRect[3])
    gb.batRect.topleft = gb.batLangRect.topleft = ((gb.WIDTH/2)-int(gb.batRect[2]/2),gb.playerY)
    gb.bricksRects,gb.bricks = createBricks(4,2,2)

#Definition to draw multiple lines at once
#using a list of strings, draws lines with offsets
def drawMultipleLines(stringArray,color = (0,0,0),  widthOffset = 0, heightOffset = 0,bgcolor = None,AA = True):
    count = 0
    for string in stringArray:
        stringLabel = gb.fontCheatKeys.render(string,AA,color,bgcolor)
        gb.mainSurface.blit(stringLabel,(gb.WIDTH-stringLabel.get_width() - widthOffset,(gb.HEIGHT-stringLabel.get_height()*count) - heightOffset ))
        count += 1


#draws all bricks in the list
#using the ID draws the correct brick
def drawBricks():
    for c in gb.bricksRects:
        for b in gb.bricks:
            if b[-1] == 0 and b[-2]==c:
                index = gb.bricks.index((c,0))
                gb.mainSurface.blit(gb.brick,gb.bricks[index][-2])
            elif b[-1] == 1 and b[-2]==c:
                index = gb.bricks.index((c,1))
                gb.mainSurface.blit(gb.brickBlauw,gb.bricks[index][-2])
            elif b[-1] == 2 and b[-2]==c:
                index = gb.bricks.index((c,2))
                gb.mainSurface.blit(gb.brickGeel,gb.bricks[index][-2])
            elif b[-1] == 3 and b[-2]==c:
                index = gb.bricks.index((c,3))
                gb.mainSurface.blit(gb.brickSleutel,gb.bricks[index][-2])


#main checker for ALL events in the level
#includes mouse, keypresses and keyholds
def checkLevelEvents():
    for event in pygame.event.get():
        checkKeyQuit(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if not gb.ballServed:
                gb.ballServed = True
        elif event.type == pygame.MOUSEMOTION:
            checkMouseEvents(event)
        elif event.type == pygame.KEYDOWN:
            checkKeyDownEvents(event)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and gb.keyDown == "K_LEFT":
                gb.keyDown = None
            elif event.key == pygame.K_RIGHT and gb.keyDown == "K_RIGHT":
                gb.keyDown = None
    if gb.keyDown:
        checkKeyHoldingEvents(gb.keyDown)


#checks all keydownevents
#includes Left,Right and Space
def checkKeyDownEvents(event ):
    if event.key == pygame.K_LEFT:
        gb.keyDown = "K_LEFT"
        doKeyLeft()
    if event.key == pygame.K_RIGHT:
        gb.keyDown = "K_RIGHT"
        doKeyRight()
    if(gb.DEVELOPER_TOOLS):
        handleCheatMenu(event)
    if event.key == pygame.K_SPACE:
        if not gb.ballServed:
            gb.ballServed = True


#checks all keyholding events
#includes left and right
def checkKeyHoldingEvents(keyDown):
    if keyDown == "K_LEFT":
        doKeyLeft()
    if keyDown == "K_RIGHT":
        doKeyRight()


#sets the location of bat if ball not served
#Use KEYBOARD_SPEED to change the speed of the bat
def doKeyLeft():
    if gb.changeBat and gb.batLangRect[0] > 0:
        gb.batLangRect.topleft = (gb.batLangRect[0]-gb.KEYBOARD_SPEED,gb.playerY)
    elif not gb.changeBat and gb.batRect[0] > 0:
        gb.batRect.topleft = (gb.batRect[0]-gb.KEYBOARD_SPEED,gb.playerY)
    if not gb.ballServed:
        gb.bx,gb.by = setLocationUnservedBall(gb.changeBat)
        gb.ballRect.topleft = (gb.bx,gb.by)


#sets the location of the bat if balll not served

def doKeyRight():
    if gb.changeBat and gb.batLangRect[0] < gb.WIDTH-gb.batLangRect[2]:
        gb.batLangRect.topleft = (gb.batLangRect[0]+gb.KEYBOARD_SPEED,gb.playerY)
    elif not gb.changeBat and ( gb.batRect[0] < gb.WIDTH-gb.batRect[2]):
        gb.batRect.topleft = (gb.batRect[0]+gb.KEYBOARD_SPEED,gb.playerY)
    if not gb.ballServed:
        gb.bx,gb.by = setLocationUnservedBall(gb.changeBat)
        gb.ballRect.topleft = (gb.bx,gb.by)


#sets the location of the bat with ball on top
def setLocationUnservedBall(changeBat):
    if changeBat:
        return (gb.batLangRect[0]+int(gb.batLangRect[2]/2)-int(gb.ballRect[2]/2),gb.playerY-gb.batLangRect[3])
    else:
        return (gb.batRect[0]+int(gb.batRect[2]/2)-int(gb.ballRect[2]/2),gb.playerY-gb.batRect[3])


#draws all upgrades according to the ID
#also goes to check if current upgrades is not collided
def drawUpgrades():
    for upgrade in gb.upgradeRectList:
        #collision detection
        if(upgrade[-1]==1):
            gb.mainSurface.blit(gb.upgradeBlauw,(upgrade[-2].topleft))
        elif(upgrade[-1]==2):
            gb.mainSurface.blit(gb.upgradeGeel,(upgrade[-2].topleft))
        elif(upgrade[-1]==3):
            gb.mainSurface.blit(gb.upgradeSleutel,(upgrade[-2].topleft))
        upgrade[-2].topleft = (upgrade[-2][0],upgrade[-2][1]+gb.ballSpeed-2) #upgrades naar beneden laten vallen, speed = 2
        checkBallUpgradeCollide(upgrade)


#check for the ball collides
#ability to check for up, down, left and right of the screen
def checkBallCollides():
    #Onderkant
    if(gb.by <= 0):
        gb.by = 0
        gb.sy *= -1
    #Bovenkant
    if(gb.changeBall and gb.by >= gb.HEIGHT-24 ) or (not gb.changeBall and gb.by >= gb.HEIGHT-16):
        if not gb.changeBall:
            gb.by = gb.HEIGHT-16
        else:
            gb.by = gb.HEIGHT-24
        gb.sy *= -1
        gb.ballServed = False
        if gb.changeBall:
            gb.changeBall = False
        gb.scoreTemp = 0
        gb.bx,gb.by = (gb.batRect[0]+int((gb.batRect[2]/2)-gb.ballRect[2]/2),gb.playerY-gb.ballRect[3])
        gb.ballRect.topleft = gb.bx,gb.by
        gb.lives -= 1
        if gb.lives == 0:
            gb.levelsPlaying = False
            gb.gameOverMenu = True
    #Rechts
    if(gb.bx <= 0):
        gb.sx *= -1
        gb.bx = 0
    #Links
    if(gb.bx >= gb.WIDTH):
        gb.sx *= -1
        gb.bx = gb.WIDTH


#check if the ball collide with bat
#if collides then change bat and/or ball to normal & play sound
def checkBallBatCollide():
    collide = False
    if not gb.changeBall and ((gb.ballRect.colliderect(gb.batRect) and not gb.changeBat)or(gb.ballRect.colliderect(gb.batLangRect) and gb.changeBat)):
        #botsting met kleine bal
        gb.by = gb.playerY-16
        gb.score += gb.scoreTemp
        collide = True
    elif gb.changeBall and ((gb.ballBigRect.colliderect(gb.batRect) and not gb.changeBat)or(gb.ballBigRect.colliderect(gb.batLangRect) and gb.changeBat)):
        #botsing met grote bal
        gb.by = gb.playerY-24
        gb.changeBall = False
        gb.score += gb.scoreTemp*gb.scoreComboMultiplier
        collide = True
    if collide:
        pygame.mixer.Sound.play(gb.batBotsingSound)
        gb.scoreTemp = 0
        gb.sy *= -1
        if gb.scoreTemp >= gb.SCORE_FOR_EXTRA_LIFE and gb.lives < gb.maxLives:
            gb.lives += 1
        if gb.changeBat:
            gb.batRect.topleft = gb.batLangRect.topleft
            gb.changeBat = False


#checks if the upgrades collided with ball
#goes to deletes the nessecary upgrade and upgrades the player
def checkBallUpgradeCollide(upgrade):
    if(upgrade[-1]==1):
        gb.mainSurface.blit(gb.upgradeBlauw,(upgrade[-2].topleft))
    elif(upgrade[-1]==2):
        gb.mainSurface.blit(gb.upgradeGeel,(upgrade[-2].topleft))
    elif(upgrade[-1]==3):
        gb.mainSurface.blit(gb.upgradeSleutel,(upgrade[-2].topleft))
    upgrade[-2].topleft = (upgrade[-2][0],upgrade[-2][1]+gb.ballSpeed-2) #upgrades naar beneden laten vallen, speed = 2
    if gb.batLangRect.colliderect(upgrade[-2]):
        deleteUpgradeByRect(upgrade)
        if upgrade[-1]==1:
            gb.changeBall = True
        elif upgrade[-1]==2:
            gb.batLangRect.topleft = gb.batRect.topleft
    elif gb.batRect.colliderect(upgrade[-2]):
        deleteUpgradeByRect(upgrade)
        if upgrade[-1]==1:
            gb.changeBall = True
        elif upgrade[-1]==2:
            gb.batLangRect.topleft = gb.batRect.topleft
            gb.changeBat = True
    elif(upgrade[-2][1] >= gb.HEIGHT-8):
        deleteUpgradeByRect(upgrade)
    if(gb.batRect.colliderect(upgrade[-2]) and upgrade[-1]==3) or (gb.batLangRect.colliderect(upgrade[-2]) and upgrade[-1]==3):
        gb.changeBat = False
        gb.levelsPlaying = False
        gb.changeLevel = True
        gb.score += gb.scoreTemp
    #out of bound detection


#easy delete of the upgrade using the object
def deleteUpgradeByRect(upgrade):
    del(gb.upgradeRectList[gb.upgradeRectList.index(upgrade)])


#check for the quit event in event.type
def checkKeyQuit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


#do main as last
if __name__ == '__main__':
    main()