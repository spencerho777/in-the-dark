import random
import time
add_library("sound")

boxSize = 30
overMonster= False
overCoin = False
monsterCoord = []
coinCoord = []
interval = 3000
"""
Sets the position of the box to the center, makes 2-5 coins and
monster coordinates randomly, creates the sounds,
and makes the background black
"""
def setup():
    size(640, 360)
    global boxPosX, boxPosY, monsterCoord, coinCoord, scare, getCoin, monsters, m, toScare, monster, \
    toAnimateCoin, coinImg, redGlow, titleFont, pressedStartButton, regFont, ultimate
    boxPosX = width / 2.0
    boxPosY = height / 2.0
    for x in range(0, random.randint(2, 5)):
        monsterCoord.append([random.randint(0, width), random.randint(0, height)])
        coinCoord.append([random.randint(0, width), random.randint(0, height)])
    scare = SoundFile(this, "scream.mp3")
    getCoin = SoundFile(this, "coinCollect.wav")
    background(0)
    rectMode(RADIUS)
    img1 = loadImage("scary1.jpg")
    img2 = loadImage("scary2.png")
    img3 = loadImage("scary3.jpg")
    monsters = [img1, img2, img3]
    ultimate = loadImage("ultimateScare.jpg")
    m = millis()
    toScare= False
    monster = monsters[0]
    toAnimateCoin = False
    coinImg = loadImage("coin.png")
    scaryAmbience = SoundFile(this, "horrorAmbience.wav")
    redGlow = loadImage("redGlow.jpg")
    titleFont = createFont("horroroid.ttf", 72)
    regFont = createFont("Georgia", 23)
    textFont(titleFont)
    pressedStartButton=False
    scaryAmbience.play()
    
def draw():
    background(0)
    global overMonster, overCoin, mousePress, m, toScare, monster, whichMonster, whichCoin, \
        toAnimateCoin, pressedStartButton, ultimate
    if(millis() < 5000):
        
        
        stroke(255, 0, 0)
        fill(172)
        
        textFont(titleFont)
        text("Welcome to", 80, 150)
        text("In The Dark", width/2, height - 100)
        
        # Home Screen
        pressedStartButton = True
    
    if 5000<millis()<10000:
        textFont(regFont)
        fill(255, 0, 0)
        text("Collect Coins, avoid monsters.", width / 2, height /2)
        text("When you can't find anything. The red glow will show you...", width/ 2 - 300, height /2 +100)
    
    if millis() > 10000:
        
    # creates 40 x 40 rectangles representing monsters
        fill(0)
        noStroke()
        for coord in monsterCoord:
            rect(coord[0], coord[1], 40, 40)
        
        # changes the variable "overMonster" if the mouse is inside
        # the monster box
        for coord in monsterCoord:
            if coord[0] - 40 < mouseX < coord[0] + 40 and \
        coord[1] - 40 < mouseY < coord[1] + 40 and not toScare:
                overMonster = True
                whichMonster = coord
                break
            overMonster = False
                
        # creates a 30 x 30 rectangle representing coins
        for coord in coinCoord:
            #fill(255, 255, 0)
            rect(coord[0], coord[1], 30, 30)
            
        # changes the variable "overCoin" if the mouse is inside
        # the coin box
        for coord in coinCoord:
            if coord[0] - 30 < mouseX < coord[0] + 30 and \
        coord[1] - 30 < mouseY < coord[1] + 30 and not toAnimateCoin:
                overCoin = True
                whichCoin = coord
                break
            overCoin = False
    
        # creates red text telling the player how many coins are left    
        fill(255, 0, 0)
        textFont(regFont)
        text(str(len(coinCoord)) + " Coins Left", 20, 20)
        
        # creates the rectangle that represents the player
        fill(255)
        rect(boxPosX, boxPosY, boxSize, boxSize)
    
        if toScare:
            if(millis() - m < interval):
                image(monster, 0, 0)
            else:
                m = millis()
                toScare = False
                monsterCoord.remove(whichMonster)
    
        if toAnimateCoin:
            if millis() - m < interval // 2:
                image(coinImg, whichCoin[0] - 30, whichCoin[1] - 10)
                
            else:
                m = millis()
                toAnimateCoin = False
                coinCoord.remove(whichCoin)
                
        if not len(coinCoord):
            fill(255)
            if(millis() - m < interval + 2000):
                textFont(regFont)
                text("You Win!", width / 2, height / 2)
            else:
                m = millis()
                scare.play()
                if(millis() - m < interval - 2000):
                    image(ultimate, 0, 0)
                else:
                    exit()

        if(random.randint(0, 500) == 0):
                if(random.randint(0, 2) != 2 and len(monsterCoord)):
                    randomMonster = monsterCoord[random.randint(0,len(monsterCoord) - 1)]
                    image(redGlow, randomMonster[0], randomMonster[1])
                elif(len(coinCoord)):
                    image(redGlow, coinCoord[0][0], coinCoord[0][1])
        if not toAnimateCoin and not toScare:
            m = millis()
        
        if len(monsterCoord) == 0:
            if(millis() - m < interval + 2000):
                textFont(titleFont)
                text("You Lost!", width / 2, height / 2)
            else:
                m = millis()
            
            if(millis() - m < interval - 2000):
                image(ultimate, 0, 0)
                scare.play()
                
            else:
                m = millis()
                exit()
                
            
def mouseMoved():
    global boxPosX, boxPosY
    # moves rectangle box to the mouse
    boxPosX = mouseX
    boxPosY = mouseY

    
def mousePressed():
    
    # scares player if they click the monster box
    # rewards player if they click the coin box
    global m, toScare, monster, toAnimateCoin
    if(not toScare and not toAnimateCoin):
        if overMonster and overCoin:
            scare.play()
            toScare = True
            monster = monsters[random.randint(0,2)]
            
        elif overCoin:
            getCoin.play()
            toAnimateCoin = True
            #time.sleep(2)
            
        elif overMonster:
            scare.play()
            toScare = True
            monster = monsters[random.randint(0,2)]