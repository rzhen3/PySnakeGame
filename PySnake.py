
#------------   S N A K E   G A M E ----------     By: Abeed, Roy and Zoltan

#The following is a game similar to the classical snake game. The player
#controls a snake and his goal is to accumulate as many points as possible.
#He can die if he runs into himself. There are also many useful powerups to be
#collected that can benefit the player as well as a neat feature called 'infinity wall'

#Import useful modules
import pygame, sys
from pygame.locals import *
from random import randrange
from array import *
from tkinter import *
from tkinter.font import Font
import os

pygame.display.set_caption("Snake")#sets the name of the window
pygame.init()

#Fonts and text to be used
scoreFont = pygame.font.SysFont("comicsansms", 18)
bigBoiFont = pygame.font.SysFont("comicsansms", 36)#Title fonts
font = pygame.font.SysFont("timesnewroman", 60)#sets the font (can be changed)
text = bigBoiFont.render("Snake! SsSSsss", True, (0, 128, 0))#sets the title text
lose = bigBoiFont.render("You Lose", True, (255, 0, 0))#sets the title text
scoretxt = font.render("Your score was: ", True, (255, 0, 0))#sets the title text

#Window + required element
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,50)
win = pygame.display.set_mode((601,676)) #creates a surface


#Program-wide variables
max_screen_width = 560
max_screen_height = 635
min_screen_height=75
min_screen_width = 0

#Images
jungleBack = pygame.image.load(r'Snake_assets\jungleback.jpg').convert_alpha()
appleimg = pygame.image.load(r'Snake_assets\apple.png').convert_alpha()
timerimg = pygame.image.load(r'Snake_assets\snakeTimer.png').convert_alpha()
starimg = pygame.image.load(r'Snake_assets\snakeStar.png').convert_alpha()

#Quick function for quitting game
def quitGame():
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)

#Draw menu screen
def startMenu():
        #initialize button screen with tkinter
        root = Tk()
        root.geometry('601x676')
        my_font = Font(family="Berlin Sans FB Demi", size = 64)
        #Smake background photo
        photo = PhotoImage(file=r"Snake_assets\snakeanim.png")
        snakephoto = Label(root, image=photo)
        snakephoto.pack()

        #Title
        title = Label(root,text="Snake",font=my_font,fg='green')
        title.place(x=200,y=100,in_=root)

        #Create play button
        play = Button(root,text="Play",fg="white",bg="green", command= root.destroy)
        play.config(height = 3, width = 20)
        play.place(x=240,y=300, in_=root)
        root.mainloop()
        
#Draw screen that occurs upon death
def endscreen():
        #initialize button screen with tkinter
        root = Tk()
        root.geometry('601x676+90+25')
        my_font = Font(family="Berlin Sans FB Demi", size = 64)
        #Snake background photo
        photo = PhotoImage(file=r"Snake_assets\snakeanimrotate.png")
        snakephoto = Label(root, image=photo)
        snakephoto.place(x=40,y=400,in_=root)
        #Title
        title = Label(root,text="Score:",font=my_font,fg='green')
        title.place(x=80,y=75,in_=root)
        #Create play again button
        play = Button(root,text="Play again",fg="white",bg="green",command=root.destroy)
        play.config(height = 3, width = 20)
        play.place(x=140,y=250, in_=root)

        #Function closes and exits game
        def stopPlaying():
            pygame.quit()
            root.destroy()
            exit()
        #Creates quit button that runs the definiton above
        quitButton = Button(root,text="Quit",fg="white",bg="light green",command=stopPlaying)
        quitButton.config(height = 3, width = 20)
        quitButton.place(x=330,y=250, in_=root)
        #Display score
        scoretext = Label(root,text=score,font=my_font, fg='light green')
        scoretext.place(x=400,y=75,in_=root)
        root.mainloop()
        
#Draw rules
def rules ():
    #Rule text
    rules1 = scoreFont.render("Use the arrow keys to control the direction of your snake.", True, (0, 128, 0))#
    rules2 = scoreFont.render("Eat apples to grow in length", True, (0, 128, 0))#
    rules3 = scoreFont.render("Don't cross your self as you slither from apple to apple", True, (0, 128, 0))#
    rules4 = scoreFont.render("Run into stopwatch to slow down the time", True, (0, 128, 0))#
    rules5 = scoreFont.render("Run into star to remove shed your skin", True, (0, 128, 0))#
    rules6 = scoreFont.render("Get as high of a score as you can!", True, (0, 128, 0))# rule text
    #Draw box containing the rules
    pygame.draw.line(win, (0,0,0), (50,610), (50,420))
    pygame.draw.line(win, (0,0,0), (560,610), (560,420))
    pygame.draw.line(win, (0,0,0), (560,610), (50,610))
    pygame.draw.line(win, (0,0,0), (560,420), (50,420))    
    #Display rule text
    win.blit(rules1,(200 - text.get_width() // 2, 450 - text.get_height() // 2))#calls on rules
    win.blit(rules2,(200 - text.get_width() // 2, 480 - text.get_height() // 2))
    win.blit(rules3,(200 - text.get_width() // 2, 510 - text.get_height() // 2))
    win.blit(rules4,(200 - text.get_width() // 2, 540 - text.get_height() // 2))
    win.blit(rules5,(200 - text.get_width() // 2, 570 - text.get_height() // 2))
    win.blit(rules6,(200 - text.get_width() // 2, 600 - text.get_height() // 2))

#Draw gameplay screen
def drawGrid():
    #Clear previous screen and draw background
    win.fill((255,255,255))
    display_surface = pygame.display.set_mode((601,676),pygame.SRCALPHA)
    display_surface.blit(jungleBack, (0,0))
    #Draw the board lines
    for count in range (16):
         pygame.draw.line(win, (0,0,0), (count*40,75), (count*40,675))#draws vertical lines
         pygame.draw.line(win, (0,0,0), (0,75+count*40), (600,75+count*40))#draws horizontal lines    
    win.blit(text,(300 - text.get_width() // 2, 40 - text.get_height() // 2))#draws the title

#Draw screen before gameplay starts
def startScreen():
    #Draws text and visuals before starting game
    startgame = font.render("Press enter to start", True, (0, 128, 0))
    win.fill((255,255,255)) #refreshed the sceen (white)
    win.blit(startgame,(210 - text.get_width() // 2, 200 - text.get_height() // 2))#starts
    rules()
def gameHUD():
    #Display player score on top-right corner
    playerScore = scoreFont.render("Score:", True, (0,0,0))
    scoreVal = scoreFont.render(str(score), True, (0,0,0))
    win.blit(playerScore,(150 - text.get_width() // 2, 50 - text.get_height() // 2))
    win.blit(scoreVal,(220 - text.get_width() // 2, 50 - text.get_height() // 2))
    #Display duration of the slow time on top-left corner
    powerTimer = scoreFont.render("Slow Speed:", True, (0,0,0))
    timerVal = scoreFont.render(str(timerMoves), True, (0,0,0))
    win.blit(powerTimer,(600 - text.get_width() // 2, 50 - text.get_height() // 2))
    #Only display duration if the effect exists
    if timerMoves !=0:
        win.blit(timerVal,(700 - text.get_width() // 2, 50 - text.get_height() // 2))
        
#Determines whether item spawns
def spawn(odds):
    x = randrange(1,odds,1)
    y = randrange(1,odds,1)
    if x == y:
        return True    
    return False

class snakeHead:#Class snake
    #Constructor that sets basic snake segment (x,y)and direction
    def __init__(self,xCord, yCord,direction):
        self.PosX = xCord
        self.PosY = yCord
        self.direction = direction

class apple: #Class apple
    #Constructor that sets spple (x,y)
    def __init__(self,PosX,PosY):
        self.PosX = PosX
        self.PosY = PosY
    #Check if object collides with snake
    def checkCollision(self, snake):
        if self.PosX == snake[0].PosX and self.PosY == snake[0].PosY:
            return True
        return False
    
class timer: #Class timer power up
    def __init__(self,PosX,PosY):
        self.PosX = PosX
        self.PosY = PosY
    def checkCollision(self, snake):
        if self.PosX == snake[0].PosX and self.PosY == snake[0].PosY:
            return True
        return False
    
class molt: #Class molt power up 
    def __init__(self, PosX, PosY):
        self.PosX = PosX
        self.PosY = PosY
    def checkCollision(self,snake):
        if self.PosX == snake[0].PosX and self.PosY == snake[0].PosY:
            return True
        return False
#Draw start menu 
startMenu()
#Gameplay
while True:
    #Create molt power up instance
    moltExist = True
    moltPU = molt(randrange(min_screen_width, max_screen_width, 40), randrange(min_screen_height, max_screen_height,40))
    #Create timer power up instance
    timeSpeed = 8
    timerMoves = 0
    timerPU = timer(randrange(min_screen_width,max_screen_width,40), randrange(min_screen_height,max_screen_height,40))
    startScreen()
    pygame.display.update()
    #Gameplay wide variables
    score = 0
    start = False#Start screen continue
    addedPiece = False
    run=True#Gameplay continue
    
    #Create first snake segment instance
    head = snakeHead(280,355,"d")
    clock = pygame.time.Clock()#defines time var
    #Create apple instance at random position
    app = apple(randrange(min_screen_width,max_screen_width,40), randrange(min_screen_height,max_screen_height,40))
    win.blit(appleimg, (app.PosX, app.PosY))
    key= pygame.key.get_pressed()#variable for using keyboard input
    snake = []#stors snake segments
    turned = False
    #Draw intro page
    while not(start):
        clock.tick(1)
        for event in pygame.event.get():
            if event.type == QUIT:
                quitGame()
            #Start game on enter prssed
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    start = True
                   
    while run:
        drawGrid()        
        clock.tick(timeSpeed)#Set speed of game
        #Add new segments if snake has length
        if len(snake) !=0:
            head = snakeHead(snake[0].PosX, snake[0].PosY,snake[0].direction)
        #Check keyboard input for snake direction change. Only permit one input 
        for event in pygame.event.get():
            if event.type == QUIT:
                quitGame()
            elif event.type == KEYDOWN:
                if (event.key == K_UP and head.direction != "d") and (turned == False):
                    head.direction = "u"
                    turned = True
                elif (event.key == K_DOWN and head.direction != "u")and (turned == False):
                    head.direction = "d"
                    turned = True
                elif (event.key == K_LEFT and head.direction != "r")and (turned == False):
                    head.direction = "l"
                    turned = True
                elif (event.key == K_RIGHT and head.direction != "l")and (turned == False):
                    head.direction = "r"
                    turned = True

 
        #Move the snake based on head direction
        if head.direction =="d":
            head.PosY +=40
            pygame.draw.rect(win,(255,0,0),(head.PosX+15, head.PosY, 10,65))
        elif head.direction == "u":
            head.PosY -=40
            pygame.draw.rect(win,(255,0,0), (head.PosX+15,head.PosY, 10, -25))
        elif head.direction == "r":
            head.PosX +=40
            pygame.draw.rect(win, (255,0,0), (head.PosX+40, head.PosY+15, 25, 10))
        elif head.direction == "l":
            head.PosX -=40
            pygame.draw.rect(win, (255,0,0), (head.PosX, head.PosY+15, -25, 10))
        #Add new head based on keyboard
        snake.insert(0,head)

        #Check if an element of the snake has passed the boundaries
        #Respawn it on the opposite side if so
        for i in snake:
            if i.PosY<min_screen_height:
                i.PosY = max_screen_height
            if i.PosY>max_screen_height:
                i.PosY = min_screen_height
            if i.PosX> max_screen_width:
                i.PosX = min_screen_width
            if i.PosX< min_screen_width:
                i.PosX = max_screen_width
        
        #Check if head collides with snake body segments
        for i in range(1,len(snake)): 
            if snake[0].PosX == snake[i].PosX and snake[0].PosY == snake[i].PosY:
                run = False
#---------------------------------------------------------------------------------------------------------------------------------------
        #Check if head collides with apple 
        if app.checkCollision(snake):
            #Create new apple & regulate variables 
            app = apple(randrange(min_screen_width,max_screen_width,40), randrange(min_screen_height,max_screen_height,40))
            score +=1
            addedPiece = True
        #Draw apple
        win.blit(appleimg, (app.PosX, app.PosY))
#---------------------------------------------------------------------------------------------------------------------------------------
        #Check if head collides with timer power up
        if timerPU.checkCollision(snake)and timeSpeed == 8:
            #set duration and slow speed
            timeSpeed = 4
            timerMoves = 25
        #Check if effect duration is over
        if timerMoves ==0:
            #Create new powerup when effect ends
            if timeSpeed ==4:
                timerPU = timer(randrange(min_screen_width,max_screen_width,40), randrange(min_screen_height,max_screen_height,40))
            #Change speed back to original speed and draw poewrup
            timeSpeed = 8
            win.blit(timerimg, (timerPU.PosX,timerPU.PosY))
        else :
            #Power up effect is still lasting, subtract 1 from duration
            timerMoves -=1
#---------------------------------------------------------------------------------------------------------------------------------------
        #Check if head collides with molt power up
        if moltPU.checkCollision(snake) and moltExist:
            #Delete all snake segments except for head
            while len(snake)>1:
                del snake[len(snake)-1]
            moltExist = False
        #Check if powerup exists and whether it should spawn
        if not(moltExist):
            if spawn(100):
                moltPU = molt(randrange(min_screen_width, max_screen_width,40), randrange(min_screen_height, max_screen_height, 40))
                moltExist  = True
        #Draw powerup if it exists
        if moltExist:
            win.blit(starimg, (moltPU.PosX, moltPU.PosY))
#------------------------------------------------------------------------------------------------------------------------------------------
        #Draw all snake elements
        for i in range(len(snake)):
            pygame.draw.rect(win, (0,100,0), (snake[i].PosX, snake[i].PosY, 40,40)) #draws the head of snake
            
        #Draw extra snake aesthetics
        if head.direction =="d":
            pygame.draw.rect(win,(0,0,0),(head.PosX+5, head.PosY+25, 10,10))
            pygame.draw.rect(win,(0,0,0),(head.PosX+25, head.PosY+25, 10,10))
        elif head.direction == "u":
            pygame.draw.rect(win,(0,0,0),(head.PosX+5, head.PosY+5, 10,10))
            pygame.draw.rect(win,(0,0,0),(head.PosX+25, head.PosY+5, 10,10))
        elif head.direction == "r":
            pygame.draw.rect(win,(0,0,0),(head.PosX+25, head.PosY+5, 10,10))
            pygame.draw.rect(win,(0,0,0),(head.PosX+25, head.PosY+25, 10,10))
        elif head.direction == "l":
            pygame.draw.rect(win,(0,0,0),(head.PosX+5, head.PosY+5, 10,10))
            pygame.draw.rect(win,(0,0,0),(head.PosX+5, head.PosY+25, 10,10))
                
        gameHUD()#Draw relevant player information
        pygame.display.update() #update

        #Does not delete piece if apple eaten
        if addedPiece:
            addedPiece = False
        #If no apple is eaten, delete end of snake
        else:
            del snake[len(snake)-1]
        turned = False#Reset precise input determiner
    scorenum = font.render(str(score), True, (255, 0, 0))#update score
    endscreen()#Draw the death screen
