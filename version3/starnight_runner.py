import pygame
import math
import random

class Player():
    """Holds player attributes like highscore, speed, x and y positions, lives etc.
    Allows the player to perform actions such as colliding with crystals, jumping, falling, moving forwards or backwards, and more."""

    def __init__(self, X, Y):
        """Initializes the player attributes (default values) like lives set to 3, score as 0 etc.
        This is only ran once when the player object is created."""
        
        self.speedUp = 0 #jumping speed of the player (will change if they press the jump button(s))
        self.jumping = False
        self.pos = [] #will hold the x and y position of the player
        self.frameR = 0 #tracks the current frame the player is at when running
        self.playerFrame = "" #loads the current frame image of the player onto the screen
        self.framesR = spriteSheet() #contains all the frames of running
        self.falling = False
        self.canJump = True
        self.reset = True #tracks if the position of all items on the screen needs to be resetted to their initial start positions and parameters (true at the start because we need the initial positions and attributes of the elements on the screen)
        self.collidedCrystals = False
        self.collided = False #tracks if the player collided with any obstacle (like a rocket, firestick etc.)
        self.lives = 3
        self.score = 0
        self.megaJump = False
        self.highscore = 0
        self.timeSurvived = 0
        self.blink = False #tracks if the player's avatar should blink (when their position has been resetted, after colliding with an obstacle)
        self.curPos = False #tracks if the player is on or off the screen
        
    def jump(self):
        """ Checks if MEGA jump ability is chosen by the user (speed would be 20).
        Choose the upward speed based on that (if MEGA jump isn't done, then the speed is 15)."""
        
        if self.jumping:
            if self.megaJump == True:
                self.speedUp = 20 #MEGA jump is selected, therefore the speed is 20
            else:
                self.speedUp = 15 #normal jump is chosen, therefore the speed is 15
               
    def collisionGaps(self, rect1, rect2, rect3, rect4, rect5, Y):
        """Detects if the player has fallen into one of the gaps (and decrease the life if so)."""
        
        if not(((self.pos[0] + 70 > rect1.left and self.pos[0] < rect1.left + rect1.w) or (self.pos[0] + 70 > rect2.left and self.pos[0] < rect2.left + rect2.w)
                or  (self.pos[0] + 70 > rect3.left and self.pos[0] < rect3.left + rect3.w) or (self.pos[0] + 70 > rect4.left and self.pos[0] < rect4.left + rect4.w)
                or (self.pos[0] + 70 > rect5.left and self.pos[0] < rect5.left + rect5.w))):
            if self.pos[1] >= Y-180 and self.falling == False:
                #object has fallen into one of the gaps
                self.lives -= 1 #life is decreased by 1
                self.falling = True #the player is now supposed to be falling as he fell into a gap
                self.canJump = False #player's ability to jump is prevented (as he would be falling)
               
    def collisionLasers(self, eLaser1, eLaser2, eLaser3, eLaser4, X, Y):
        """Detects the collision of the player with the electronic lasers (and decrease the life if so)."""
        
        if ((self.pos[0] + 30 > eLaser1[0] and self.pos[0] + 30 < eLaser1[0] + (X-1460) and self.pos[1] + 30 < eLaser1[1] + (Y-505) and self.pos[1] + 30 > eLaser1[1])
        or (self.pos[0] + 30 > eLaser2[0] and self.pos[0] + 30 < eLaser2[0] + (X-1460) and self.pos[1] + 30 < eLaser2[1] + (Y-505) and self.pos[1] + 30 > eLaser2[1])
        or (self.pos[0] + 30 > eLaser3[0] and self.pos[0] + 30 < eLaser3[0] + (X-1460) and self.pos[1] + 30 < eLaser3[1] + (Y-505) and self.pos[1] + 30 > eLaser3[1])
        or (self.pos[0] + 30 > eLaser4[0] and self.pos[0] + 30 < eLaser4[0] + (X-1460) and self.pos[1] + 30 < eLaser4[1] + (Y-505) and self.pos[1] + 30 > eLaser4[1])):
            #the player collides with a laser
            self.lives -= 1 #life is decreased by 1
            self.collided = True
            self.reset = True #resets the items on the screen to their initial start positions and parameters
            
    def collisionRockets(self, rocket1, rocket2, X, Y):
        """Detects the collision of the player with the rockets (and decrease the life if so)."""
        
        if ((self.pos[0] + 30 > rocket1[0] and self.pos[0] + 30 < rocket1[0] + (X-1420) and self.pos[1] + 30 < rocket1[1] + (Y-557) and self.pos[1] + 30 > rocket1[1])
        or (self.pos[0] + 30 > rocket2[0] and self.pos[0] + 30 < rocket2[0] + (X-1420) and self.pos[1] + 30 < rocket2[1] + (Y-557) and self.pos[1] + 30 > rocket2[1])):
            #the player collides with a rocket
            self.lives -= 1 #life is decreased by 1
            self.collided = True
            self.reset = True #resets the items on the screen to their initial start positions and parameters
            
    def collisionFirestick(self, firestick1, X, Y):
        """Detects the collision of the player with the firestick (and decrease the lives if so)."""
        
        if (self.pos[0] + 30 > firestick1[0] and self.pos[0] + 30 < firestick1[0] + (X-1460) and self.pos[1] + 30 < firestick1[1] + (Y-505) and self.pos[1] + 30 > firestick1[1]):
            #the player collides with a firestick
            self.lives -= 2 #life is decreased by 2
            self.collided = True
            self.reset = True #resets the items on the screen to their initial start positions and parameters
            
    def collisionPowerups(self, powerup1, powerup2, X, Y):
        """Detects the collision of the player with the powerups (and increase the life if so)."""
        
        if ((self.pos[0] + 30 > powerup1[0] and self.pos[0] + 30 < powerup1[0] + (X-1450) and self.pos[1] + 30 < powerup1[1] + (Y-557) and self.pos[1] + 30 > powerup1[1])
        or (self.pos[0] + 30 > powerup2[0] and self.pos[0] + 30 < powerup2[0] + (X-1450) and self.pos[1] + 30 < powerup2[1] + (Y-557) and self.pos[1] + 30 > powerup2[1])):
            if self.collidedPowerups == False:
                #the player collides with a powerup
                #make the powerup collided with disappear from the screen (meaning that it is collected)
                if (self.pos[0] + 30 > powerup1[0] and self.pos[0] + 30 < powerup1[0] + (X-1450)):
                    powerup1[1] = -500
                if (self.pos[0] + 30 > powerup2[0] and self.pos[0] + 30 < powerup2[0] + (X-1450)):
                    powerup2[1] = -500
                self.lives += 1 #life is increased by 1
            self.collidedPowerups = True
        else:
            self.collidedPowerups = False
               
    def collisionCrystals(self, crystal1, crystal2, crystal3, crystal4, X, Y):
        """Detects the collision of the player with the Radian Crystals (and increase the score if so)."""
        
        if ((self.pos[0] + 30 > crystal1[0] and self.pos[0] + 30 < crystal1[0] + (X-1460) and self.pos[1] + 30 < crystal1[1] + (Y-505) and self.pos[1] + 30 > crystal1[1])
        or (self.pos[0] + 30 > crystal2[0] and self.pos[0] + 30 < crystal2[0] + (X-1460) and self.pos[1] + 30 < crystal2[1] + (Y-505) and self.pos[1] + 30 > crystal2[1])
        or (self.pos[0] + 30 > crystal3[0] and self.pos[0] + 30 < crystal3[0] + (X-1460) and self.pos[1] + 30 < crystal3[1] + (Y-505) and self.pos[1] + 30 > crystal3[1])
        or (self.pos[0] + 30 > crystal4[0] and self.pos[0] + 30 < crystal4[0] + (X-1460) and self.pos[1] + 30 < crystal4[1] + (Y-505) and self.pos[1] + 30 > crystal4[1])):
            if self.collidedCrystals == False:
                #the player collides with a crystal
                #make the crystal collided with disappear from the screen (meaning that it is collected)
                if (self.pos[0] + 30 > crystal1[0] and self.pos[0] + 30 < crystal1[0] + (X-1460)):
                    crystal1[1] = -500
                if (self.pos[0] + 30 > crystal2[0] and self.pos[0] + 30 < crystal2[0] + (X-1460)):
                    crystal2[1] = -500
                if (self.pos[0]  + 30 > crystal3[0] and self.pos[0] + 30 < crystal3[0] + (X-1460)):
                    crystal3[1] = -500
                if (self.pos[0]  + 30 > crystal4[0] and self.pos[0] + 30 < crystal4[0] + (X-1460)):
                    crystal4[1] = -500
                self.score += 1 #score is increased by 1
            self.collidedCrystals = True
        else:
            self.collidedCrystals = False
           
    def animationPlayer(self, X, Y):
        """Loads the jumping animation (single frame) of the player.
        Loads the current frame of running."""
        
        if self.jumping == False:
            #shows motion of running
            if self.frameR == len(self.framesR.running):
                self.frameR = 0 #resets the frames of running to the first one if the last one is loaded
            self.playerFrame = self.framesR.running[self.frameR] #loads the current frame image of running (to display on the screen)
            self.playerFrame = pygame.transform.scale(self.playerFrame, (X-1430, Y-520))
            self.frameR += 1 #moves to the next frame of running once this one is loaded
        elif self.falling == False and self.jumping:
            #shows motion of jumping
            self.playerFrame = pygame.image.load("../animation/jumping/1.PNG") #loads the frame of jumping (to display on the screen)
            self.playerFrame = pygame.transform.scale(self.playerFrame, (X-1430, Y-520))
            
    def blinkPlayer(self, scrollCheck, X, Y):
        """Blinks the player's avatar, if needed."""
        
        if self.blink and scrollCheck > X-220:
            #blinks the player's avatar
            self.canJump = False #the player isn't allowed to jump during this time
            if self.curPos == False:
                self.pos[1] = -500
                self.curPos = True
            elif self.curPos:
                self.pos[1] = Y-180
                self.curPos = False
        else:
            #no blinking of the player's avatar is required
            self.canJump = True #the player can jump again
            self.blink = False
            self.collided = False
       
    def checkStatusY(self, Y):
       """Allows the player to conduct actions like falling and landing."""
       
       if self.jumping:
           if self.pos[1] <= Y-600:
               #player reaches the top height
               self.speedUp = -15.5 #reset the speed downwards (to bring the player on ground level again)
           
       if self.pos[1] >= Y-180 and self.falling == False:
           #player lands
           self.speedUp = 0 #speed is resetted to 0
           self.jumping = False #the player is not being detected normal jumping anymore
           self.megaJump = False #the player is not being detected MEGA jumping anymore
       
       if self.falling == True:
           #player falls down a gap
           if(self.pos[1] >= Y+100):
               self.collided = True
               self.reset = True #resets the items on the screen to their initial start positions and parameters
         
class spriteSheet():
    """Sprite sheet containing the different running and flamestick burning frames"""
   
    def __init__(self):
        """Loads the different image frames of the player running.
        Loads the different image frames of the firestick burning."""
        
        #player running frames
        self.running = [pygame.image.load("../animation/running/1.PNG"),
                       pygame.image.load("../animation/running/2.PNG"),
                       pygame.image.load("../animation/running/3.PNG"),
                       pygame.image.load("../animation/running/4.PNG"),
                       pygame.image.load("../animation/running/5.PNG"),
                       pygame.image.load("../animation/running/6.PNG")]
        
        #firestick burning frames
        self.firestick = [pygame.image.load("../animation/firestick/1.PNG"),
                       pygame.image.load("../animation/firestick/2.PNG"),
                       pygame.image.load("../animation/firestick/3.PNG"),
                       pygame.image.load("../animation/firestick/4.PNG"),
                       pygame.image.load("../animation/firestick/5.PNG"),
                       pygame.image.load("../animation/firestick/6.PNG"),
                       pygame.image.load("../animation/firestick/7.PNG"),
                       pygame.image.load("../animation/firestick/8.PNG"),
                       pygame.image.load("../animation/firestick/9.PNG"),
                       pygame.image.load("../animation/firestick/10.PNG"),
                       pygame.image.load("../animation/firestick/11.PNG")]
        
class Powerups():
    """Allows for the spawning and re-spawning of the powerups.
    Contains the x and y co-ordinates of the powerups."""
    
    def init(self, rect3, rect5, Y):
        """Allows for the spawning of the powerups.
        The initial x and y of the powerups are set."""
        
        self.heightPowerups = [Y-280, Y-175] #randomized height of the powerups
        self.powerup1 = [rect3.left + random.randint(220, 240), self.heightPowerups[random.randint(0, 1)]]
        self.powerup2 = [rect5.left + random.randint(560, 600), self.heightPowerups[random.randint(0, 1)]]
    
    def checkRespawnPowerups(self, rect3, rect5, X):
        """Allows for the re-spawning of the powerups, if they get off screen.
        The new x and y of the powerups are set."""
        
        if self.powerup1[0] + X-1450 < -100:
            self.powerup1[0] = rect3.left + random.randint(220, 260)
            self.powerup1[1] = self.heightPowerups[random.randint(0, 1)]
        if self.powerup2[0] + X-1450 < -100:
            self.powerup2[0] = rect5.left + random.randint(540, 590)
            self.powerup2[1] = self.heightPowerups[random.randint(0, 1)]
    
class eLasers():
     """Allows for the spawning and re-spawning of the electronic lasers.
    Contains the x and y co-ordinates of the lasers."""
     
     def init(self, rect2, rect3, rect4, rect5, Y):
         """Allows for the spawning of the electronic lasers.
         The initial x and y of the lasers are set."""
        
         self.heightLasers = [Y-300, Y-195] #randomized height of the lasers
         self.eLaser1 = [rect2.left + random.randint(160, 170), self.heightLasers[random.randint(0, 1)]]
         self.eLaser2 = [rect3.left + random.randint(370, 400), self.heightLasers[random.randint(0, 1)]]
         self.eLaser3 = [rect4.left + random.randint(200, 300), self.heightLasers[random.randint(0, 1)]]
         self.eLaser4 = [rect5.left + random.randint(200, 250), self.heightLasers[random.randint(0, 1)]]
        
     def checkRespawnLasers(self, X):
         """Allows for the re-spawning of the electronic lasers, if they get off screen.
         The new x and y of the lasers are set."""
        
         if self.eLaser1[0] + X-1460 < -200:
             self.eLaser1[0] = random.randint(1620, 1630)
             self.eLaser1[1] = self.heightLasers[random.randint(0, 1)]
         if self.eLaser2[0] + X-1460 < -200:
             self.eLaser2[0] = random.randint(1650, 1660)
             self.eLaser2[1] = self.heightLasers[random.randint(0, 1)]
         if self.eLaser3[0] + X-1460 < -200:
             self.eLaser3[0] = random.randint(1650, 1660)
             self.eLaser3[1] = self.heightLasers[random.randint(0, 1)]
         if self.eLaser4[0] + X-1460 < -200:
             self.eLaser4[0] = random.randint(1680, 1690)
             self.eLaser4[1] = self.heightLasers[random.randint(0, 1)]
            
class Rocket():
    """Allows for the spawning and re-spawning of the rockets.
    Contains the x and y co-ordinates of the rockets."""
   
    def init(self, eLaser1, eLaser4, Y):
        """Allows for the spawning of the rockets.
        The initial x and y of the rockets are set."""
        
        self.heightRockets = [Y-220, Y-250] #randomized height of the rockets
        self.rocket1 = [eLaser1[0] + random.randint(200, 290), self.heightRockets[random.randint(0, 1)]]
        self.rocket2 = [eLaser4[0]  + random.randint(160, 210), self.heightRockets[random.randint(0, 1)]]
       
    def checkRespawnRockets(self, eLaser1, eLaser4, X):
        """Allows for the re-spawning of the rockets, if they get off screen.
        The new x and y of the rockets are set."""
        
        if self.rocket1[0] + X-1460 < -200:
            self.rocket1[0] = eLaser1[0] + random.randint(150, 200)
            self.rocket1[1] = self.heightRockets[random.randint(0, 1)]
        if self.rocket2[0] + X-1460 < -200:
            self.rocket2[0] = eLaser4[0]  + random.randint(130, 220)
            self.rocket2[1] = self.heightRockets[random.randint(0, 1)]
   
class Firestick():
    """Allows for the spawning and re-spawning of the firestick.
    Contains the x and y co-ordinates of the firestick."""
   
    def init(self, rect2, Y):
        """Allows for the spawning of the firestick.
        The initial x and y of the firestick are set."""
        
        self.firestick1 = [rect2.left + random.randint(420, 440), Y-192]
        self.frameF = 0
        self.firestickFrame = ""
        self.framesF = spriteSheet()
       
    def checkRespawnFirestick(self, rect2, X):
        """Allows for the re-spawning of the firestick, if it gets off screen.
        The new x and y of the firestick are set."""
        
        if self.firestick1[0] + X-1460 < -200:
            self.firestick1[0] = rect2.left + random.randint(430, 440)
            
    def animationFirestick(self, X, Y):
        """Loads the animation of the firestick burning."""
        
        if self.frameF == len(self.framesF.firestick):
            self.frameF = 0 #resets the frames of the firestick to the first one if the last one is loaded
        self.firestickFrame = self.framesF.firestick[self.frameF] #loads the current frame image of firestick (to display on the screen)
        self.firestickFrame = pygame.transform.scale(self.firestickFrame, (X-1460, Y-505))
        self.frameF += 1 #moves to the next frame of the firestick once this one is loaded

class radCrystal():
    """Allows for the spawning and re-spawning of the Radian Crystals.
    Contains the x and y co-ordinates of the crystals."""
   
    def init(self, rect2, rect4, rect5, Y):
        """Allows for the spawning of the Radian Crystals.
        The initial x and y of the crystals are set."""
        
        self.heightCrystals = [Y-300, Y-200] #randomized height of the crystals
        self.crystal1 = [rect2.left + random.randint(100, 130), self.heightCrystals[random.randint(0, 1)]]
        self.crystal2 = [rect4.left + random.randint(70, 100), self.heightCrystals[random.randint(0, 1)]]
        self.crystal3 = [rect5.left + random.randint(100, 200), self.heightCrystals[random.randint(0, 1)]]
        self.crystal4 = [rect5.left + random.randint(390, 450), self.heightCrystals[random.randint(0, 1)]]

    def checkRespawnCrystals(self, rect1, rect2, rect3, rect4, rect5, X):
        """Allows for the re-spawning of the Radian Crystals, if they get off screen.
        The new x and y of the crystals are set."""
        
        if self.crystal1[0] + X-1460 < -100:
            self.crystal1[0] = rect2.left + random.randint(40, 90)
            self.crystal1[1] = self.heightCrystals[random.randint(0, 1)]
        if self.crystal2[0] + X-1460 < -100:
            self.crystal2[0] = rect4.left + random.randint(50, 95)
            self.crystal2[1] = self.heightCrystals[random.randint(0, 1)]
        if self.crystal3[0] + X-1460 < -100:
            self.crystal3[0] = rect5.left + random.randint(60, 80)
            self.crystal3[1] = self.heightCrystals[random.randint(0, 1)]
        if self.crystal4[0] + X-1460 < -100:
            self.crystal4[0] = rect1.left + random.randint(50, 100)
            self.crystal4[1] = self.heightCrystals[random.randint(0, 1)]
           
def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init() #Prepare the pygame module for use
   
    #settings to run the fps at 60 frames/sec
    clock = pygame.time.Clock()
    FPS = 60

    #screen dimensions
    X = 1500
    Y = 600

    #create the game window
    screen = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("Starnight Runner")
   
   
    #-----------------------------Program Variable Initialization----------------------------#
    
    #load the background image and store its co-ordinates
    bg = pygame.image.load("../bg.png").convert()
    bg_width = bg.get_width()
    bg_rect = bg.get_rect()
    
    #make the scrolling of the background work
    scroll = 0
    tiles = math.ceil(X  / bg_width) + 1
    
    #load the moon image
    moon = pygame.image.load("../moon.png")
    moon = pygame.transform.scale(moon, (X-1350, Y-400))
   
    #load the tree image
    trees = pygame.image.load("../tree.png")
    trees = pygame.transform.scale(trees, (X-1420, Y-520))
    
    treesX = [] #the x co-ordinates of the background trees
   
    #load the heart image (the powerup)
    powerups =  pygame.image.load("../heart.png")
    powerups = pygame.transform.scale(powerups, (X-1450,Y-557))
    
    #load the electronic laser image
    eLaser = pygame.image.load("../e-laser.png")
    eLaser = pygame.transform.scale(eLaser, (X-1460, Y-505))
   
    #load the rocket image
    rockets = pygame.image.load("../rocket.png")
    rockets = pygame.transform.scale(rockets, (X-1420, Y-557))
    
    #load the radian crystal image
    crystals = pygame.image.load("../crystal.png")
    crystals = pygame.transform.scale(crystals, (X-1460, Y-540))
       
    crystal = radCrystal() #Radian Crystal object created
    laser = eLasers() #electronic laser object created
    rocket = Rocket() #rocket object created
    firestick = Firestick() #firestick object created
    powerup = Powerups() #powerup object created
    p = Player(X, Y) #player object created
   
    #Main Screen
    mainScreen = pygame.image.load("../main.png") #load the main screen image
    onMain = True #tracks if the user is on the main screen or not
    startTime = 0 #tracks the time when the user enters the game screen (from the start of the program)
    endTime = 0 #tracks the time when the user's lives have run out (from the start of the program)
    startTracked = False #checks if the start time has already been updated or not
   
    #End Screen
    endScreen = pygame.image.load("../end.png") #load the end screen image
    onEnd = False #tracks if the user is on the end screen or not
   
    #Help and Options Screen
    onHelpOpScreen = pygame.image.load("../helpOptions.png") #load the help and options screen image
    onHelpOp = False #tracks if the user is on the help and options screen or not
    
    #Background Music
    pygame.mixer.music.load("../music.mp3") #loads the background music file
    pygame.mixer.music.play(-1) #plays the music indefinitely
    
    font = pygame.font.Font('../Algerian.ttf', 32) #renders Algerian type font
   
    #-----------------------------Main Program Loop---------------------------------------------#
   
    run = True #tracks if the program should be running or not
    
    #runs till the user wants the game to be running (no shutdown)
    while run:
        #-----------------------------Event Handling-----------------------------------------#
        clock.tick(FPS)
        
        if onMain == True:
            #the user is detected to be on the main screen
            screen.blit(mainScreen, (0, 0)) #displays the main screen image
                   
        if onHelpOp == True:
            #the user is detected to be on the help and options screen
            screen.blit(onHelpOpScreen, (0, 0))
            #checks if the back button is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] > X-240 and pos[0] < X-70 and pos[1] > Y-60 and pos[1] < Y-30:
                    #the back button has been clicked
                    onMain = True #the user is back on the main screen
                    onHelpOp = False #the user is off the help and options screen
                curVolume = pygame.mixer.music.get_volume() #the current volume of the background music
                #check if the plus volume button is pressed
                if pos[0] > X -1475 and pos[0] < X-1415 and pos[1] > Y-105 and pos[1] < Y-45:
                    #plus volume button is pressed
                    pygame.mixer.music.set_volume(curVolume+0.1) #increases the volume
                #check if the minus volume button is pressed
                if pos[0] > X -1290 and pos[0] < X-1240 and pos[1] > Y-105 and pos[1] < Y-45:
                    #minus volume button is pressed
                    pygame.mixer.music.set_volume(curVolume-0.1) #decreases the volume
       
        if onEnd == True:
            #the user is detected to be on the end screen
            screen.blit(endScreen, (0, 0)) #displays the end screen image
            fontEnd = pygame.font.Font('../Algerian.ttf', 40) #render end screen font
            #displays score, high score and time survived
            score = fontEnd.render(('Score: ' + str (p.score)), True, (192, 175, 226))
            #check if the current score is over the highscoe
            if p.score > p.highscore:
                p.highscore = p.score #the highscore is updated to the current score (which is greater)
            p.timeSurvived = endTime - startTime #calculates the time survived of the player
            highscore = fontEnd.render(('High Score: ' + str (p.highscore)), True, (192, 175, 226))
            time = fontEnd.render(('Total Time Survived: ' + str (int(p.timeSurvived/1000)) + ' seconds'), True, (192, 175, 226))
            screen.blit(score, (X-840, Y-290))
            screen.blit(highscore, (X-895, Y-235))
            screen.blit(time, (X-1020, Y-180))
            #detects if the restart button is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] > X-900 and pos[0] < X-625 and pos[1] > Y-130 and pos[1] < Y-70:
                    #the restart button has been clicked
                    onEnd = False #the user is off the end screen
                    onMain = True #the user is redirected to the main screen
                    tempScore = p.highscore #temporarily store the highscore
                    p = Player(X, Y) #player's object is re-initialized (to reset the progress, except the highscore)
                    p.highscore = tempScore #keep the highscore of the user stored
                    startTime = 0
                    endTime = 0
                    startTracked = False
                       
        elif onMain == False and onHelpOp == False:
            #the user is detected to be on the game screen
           
            #draws the scrolling background
            for i in range(0, tiles):
              screen.blit(bg, (i * bg_width + scroll, 0))
             
            screen.blit(moon, (X-200, Y-580)) #draw the moon on the screen
           
            #checks if an initial or resetted position and parameter of the player, crystals, lasers, etc. is required
            if(p.reset):
               
                #initial or resetted rectangles' co-ordinates (x position is randomized), length and width
                rect1 = pygame.Rect(-90, 500, 500, 100)
                rect2 = pygame.Rect(random.randint(510, 530), 500, 250, 100)
                rect3 = pygame.Rect(random.randint(850, 875), 500, 350, 100)
                rect4 = pygame.Rect(random.randint(1300, 1350), 500, 200, 100)
                rect5 = pygame.Rect(random.randint(1630, 1660), 500, 230, 100)
                
                laser.init(rect2,rect3,rect4,rect5, Y) #initial or resetted lasers' co-ordinates
                rocket.init(laser.eLaser1,laser.eLaser4, Y) #initial or resetted rockets' co-ordinates
                firestick.init(rect2, Y) #initial or resetted firestick co-ordinates
                crystal.init(rect2,rect4,rect5, Y) #initial or resetted crystals' co-ordinates
                powerup.init(rect3, rect5, Y) #initial or resetted powerups' co-ordinates
               
                treesX = [random.randint(200, 300), random.randint(550, 610), random.randint(950, 1100), random.randint(1400, 1420), random.randint(1690, 1700)] #generate initial or resetted x positions to place the background trees
                
                #initial or resetted y parameters of the player
                p.falling = False
                p.speedUp = False
                p.jumping = False
                
                p.pos = [X-1350, Y-180] #initial or resetted player position
                    
                p.canJump = True #the player is allowed to jump again
                
                #initial or resetted scrolling parameters of the background
                scroll = 0
                tiles = math.ceil(X  / bg_width) + 1
                
                #checks if the lives of the player has run out
                if p.lives == 0:
                    onMain = False #the user is off the main screen
                    onEnd = True #the user is redirected to the end screen
                
                #detects if the player has collided with an obstacle
                if p.collided:
                    p.blink = True #the player needs to blink
                    
                p.reset = False
            
            p.blinkPlayer(i * bg_width + scroll, X, Y) #allows the player to blink
            p.animationPlayer(X, Y) #update the current frame of the player running or jumping
            firestick.animationFirestick(X, Y) #update the current frame of the firestick burning

            p.checkStatusY(Y) #allows the player to land, fall etc.
                
            #draw the background trees on the screen
            screen.blit(trees, (treesX[0], Y-180))
            screen.blit(trees, (treesX[1], Y-180))
            screen.blit(trees, (treesX[2], Y-180))
            screen.blit(trees, (treesX[3], Y-180))
            screen.blit(trees, (treesX[4], Y-180))
           
            #scrolling of the trees
            treesX[0] -= 4
            treesX[1] -= 4
            treesX[2] -= 4
            treesX[3] -= 4
            treesX[4] -= 4
           
            #re-spawning of the trees
            if treesX[0] + X-1420 < -100:
                treesX[0] = rect1.left + random.randint(50, 100)
            if treesX[1] + X-1420  < -100:
                treesX[1] = rect2.left + random.randint(40, 50)
            if treesX[2] + X-1420  < -100:
                treesX[2] = rect3.left + random.randint(60, 120)
            if treesX[3] + X-1420  < -100:
                treesX[3] = rect4.left + random.randint(20, 40)
            if treesX[4] + X-1420  < -100:
                treesX[4] = rect5.left + random.randint(50, 70)
           
            screen.blit(p.playerFrame, (p.pos[0],p.pos[1])) #draw the current player frame (either of running or jumping)
            screen.blit(firestick.firestickFrame, (firestick.firestick1[0], firestick.firestick1[1])) #draw the current frame of the firestick burning
            
            #scroll the firestick
            firestick.firestick1[0] -= 4
            
            p.collisionGaps(rect1, rect2, rect3, rect4, rect5, Y) #checks if the player falls into a gap (decreases the life by 1)
            p.collisionRockets(rocket.rocket1, rocket.rocket2, X, Y) #checks if the player collides with a rocket (decreases the life by 1)
            p.collisionFirestick(firestick.firestick1, X, Y) #checks if the player collides with a firestick (decreases the life by 2)
            p.collisionLasers(laser.eLaser1, laser.eLaser2, laser.eLaser3, laser.eLaser4, X, Y) #checks for the collision of the player with the lasers (decreases the life by 1)
            p.collisionCrystals(crystal.crystal1, crystal.crystal2, crystal.crystal3, crystal.crystal4, X, Y) #checks for the collision of the player with the crystals (increases the score by 1)
            p.collisionPowerups(powerup.powerup1, powerup.powerup2, X, Y) #checks for the collision of the player with the powerups (increases the life by 1)
           
            #draw the electronic lasers
            screen.blit(eLaser, (laser.eLaser1[0], laser.eLaser1[1]))
            screen.blit(eLaser, (laser.eLaser2[0], laser.eLaser2[1]))
            screen.blit(eLaser, (laser.eLaser3[0], laser.eLaser3[1]))
            screen.blit(eLaser, (laser.eLaser4[0], laser.eLaser4[1]))
           
            #scroll the electronic lasers
            laser.eLaser1[0] -= 5
            laser.eLaser2[0] -= 5
            laser.eLaser3[0] -= 5
            laser.eLaser4[0] -= 5
           
            #draw the rockets
            screen.blit(rockets, (rocket.rocket1[0], rocket.rocket1[1]))
            screen.blit(rockets, (rocket.rocket2[0], rocket.rocket2[1]))
           
            #scroll the rockets
            rocket.rocket1[0] -= 5
            rocket.rocket2[0] -= 5
           
            #draw the crystals
            screen.blit(crystals, (crystal.crystal1[0], crystal.crystal1[1]))
            screen.blit(crystals, (crystal.crystal2[0], crystal.crystal2[1]))
            screen.blit(crystals, (crystal.crystal3[0], crystal.crystal3[1]))
            screen.blit(crystals, (crystal.crystal4[0], crystal.crystal4[1]))
           
            #scroll the crystals
            crystal.crystal1[0] -= 4
            crystal.crystal2[0] -= 4
            crystal.crystal3[0] -= 4
            crystal.crystal4[0] -= 4
            
            #draw the powerups
            screen.blit(powerups, (powerup.powerup1[0], powerup.powerup1[1]))
            screen.blit(powerups, (powerup.powerup2[0], powerup.powerup2[1]))
           
            #scroll the powerups
            powerup.powerup1[0] -= 4
            powerup.powerup2[0] -= 4
           
            crystal.checkRespawnCrystals(rect1, rect2, rect3, rect4, rect5, X) #re-spawns the radian crystals when they get off screen
            laser.checkRespawnLasers(X) #re-spawns the lasers when they get off screen
            rocket.checkRespawnRockets(laser.eLaser1, laser.eLaser4, X) #re-spawns the rockets when they get off screen
            firestick.checkRespawnFirestick(rect2, X) #re-spawns the firestick when it gets off screen
            powerup.checkRespawnPowerups(rect3, rect5, X) #re-spawns the powerups when they get off screen
            
            #draw the bottom surfaces
            pygame.draw.rect(screen, (0, 0, 0), rect1)
            pygame.draw.rect(screen, (0, 0, 0), rect2)
            pygame.draw.rect(screen, (0, 0, 0), rect3)
            pygame.draw.rect(screen, (0, 0, 0), rect4)
            pygame.draw.rect(screen, (0, 0, 0), rect5)
            
            randGapsX = [random.randint(595, 615), random.randint(365, 375), random.randint(475, 500), random.randint(295, 325)] #random x positions of the bottom surface (gaps)
           
            #bottom surface spawning and re-spawning
            if(rect1.left + X-1000 > -100):
                rect1.left -= 4 #scrolling the first bottom surface
            else:
                rect1.left = X #resets the first bottom surface, if it gets off screen
            if(rect2.left + X-1250 > -100):
                rect2.left -= 4 #scrolling the second bottom surface
            else:
                rect2.left = rect1.left + randGapsX[0] #resets the second bottom surface, if it gets off screen
            if(rect3.left + X-1150 > -100):
                rect3.left -= 4 #scrolling the third bottom surface
            else:
                rect3.left = rect2.left + randGapsX[1] #resets the third bottom surface, if it gets off screen
            if(rect4.left + X-1300 > -100):
                rect4.left -= 4 #scrolling the fourth bottom surface
            else:
                rect4.left = rect3.left + randGapsX[2] #resets the fourth bottom surface, if it gets off screen
            if(rect5.left + X-1000 > -100):
                rect5.left -= 4 #scrolling the fifth bottom surface
            else:
                rect5.left = rect4.left + randGapsX[3] #resets the fifth bottom surface, if it gets off screen
           
            scroll -= 5 #scroll the background
           
            #display the lives left
            livesLeft = font.render(('Lives Left: ' + str (p.lives)), True, (192, 175, 226))
            screen.blit(livesLeft, (X-1460, Y-560))
           
            #display the score
            score = font.render(('Score: ' + str (p.score)), True, (192, 175, 226))
            screen.blit(score, (X-1460, Y-500))
           
            #reset the scroll (once the background image gets off screen)
            if abs(scroll) > bg_width:
              scroll = 0
           
            #lives of the player has run out (game over)
            if p.lives <= 0 and p.falling == False:
                p.reset = True #resets the items on the screen to their initial start positions and parameters
                endTime = pygame.time.get_ticks() #store the time when the lives of the player ran out

        #event handler
        for event in pygame.event.get():
            #checks if the game has been shutdown by the user
            if event.type == pygame.QUIT:
                run = False #close the program
            #checks if the start or help and options button is clicked on the main screen
            if event.type == pygame.MOUSEBUTTONUP and onMain:
                pos = pygame.mouse.get_pos()
                #checks if the start button is pressed
                if pos[0] > X-880 and pos[0] < X-650 and pos[1] > Y-200 and pos[1] < Y-150:
                    #start button is pressed
                    onMain = False #the user is off the main screen, to the game screen
                    if (startTracked == False):
                        startTime = pygame.time.get_ticks() #stores the start time of the game
                        startTracked = True
                #checks if the help and options button is pressed
                if pos[0] > X-880 and pos[0] < X-650 and pos[1] > Y-120 and pos[1] < Y-70:
                    #help and options button is pressed
                    onMain = False #the user is off the main screen
                    onHelpOp = True #the user is redirected to the help and options screen
            
            #checks if the user is on the game screen and if a keyboard button is pressed
            if onMain == False and onHelpOp == False and event.type == pygame.KEYDOWN:
                if not p.jumping:
                    #normal jump with UP arrow key is pressed
                    if event.key == pygame.K_UP and p.canJump and p.falling == False:
                        p.jumping = True
                        #checks if the player can jump
                        if(p.canJump):
                            p.jump() #the player normal jumps
                    #MEGA jump with SPACE key is pressed
                    if event.key == pygame.K_SPACE and p.canJump and p.falling == False:
                        p.megaJump = True #MEGA jump is used
                        p.jumping = True
                        #checks if the player can jump
                        if(p.canJump):
                            p.jump() #the player MEGA jumps
                    #the player teleports towards the right
                    if event.key == pygame.K_RIGHT and p.pos[0] < X-1291 and p.blink == False:
                        p.pos[0] += 60
                    #the player teleports towards the left
                    if event.key == pygame.K_LEFT and p.pos[0] > X-1409 and p.blink == False:
                        p.pos[0] -= 60
        #-----------------------------Program Logic---------------------------------------------#
        # Update the y position and speed of the player
        if p.reset == False:
            p.pos[1] -= p.speedUp
            p.speedUp += -1.0

        #-----------------------------Drawing Everything-------------------------------------#
        pygame.display.update()

    pygame.quit() #Closes the window, once we leave the loop

main()