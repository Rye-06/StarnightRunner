import pygame
import math
import random

class Player():
   
    #player's state variabless
    def __init__(self, X, Y):
        self.speed = 0
        self.posX = X-1350
        self.posY = Y-170
        self.jumping = False
        self.lives = 3
        self.reset = True
        self.frameR = 0
        self.image = ""
        self.sprites = spriteSheet()
        self.falling = False
        self.canJump = True
   
    #allows the player to jump
    def jump(self):
        if self.jumping:
            self.speed = 15
           
    #detects collision of the player with the gaps
    def collisionGaps(self, rect1, rect2, rect3, rect4, rect5, Y):
        #player is detected to have fallen in a gap
        if not(((self.posX + 75 > rect1.left and self.posX < rect1.left + rect1.w) or (self.posX + 75 > rect2.left and self.posX < rect2.left + rect2.w)
                or  (self.posX + 75 > rect3.left and self.posX < rect3.left + rect3.w) or (self.posX + 75 > rect4.left and self.posX < rect4.left + rect4.w)
                or (self.posX + 75 > rect5.left and self.posX < rect5.left + rect5.w))):
            if self.posY >= Y-170 and self.falling == False:
                self.lives-=1
                self.canJump = False
                self.falling = True
             
    #detects collision of the player with the lasers
    def collisionLasers(self, eLaser1, eLaser2, eLaser3, eLaser4, eLaser5, X, Y):
        #checks for collision with the first laser
        if ((self.posX > eLaser1[0] and self.posX < eLaser1[0] + (X-1460) and self.posY > eLaser1[1])
        or (self.posX > eLaser2[0] and self.posX < eLaser2[0] + (X-1460) and self.posY > eLaser2[1])
        or (self.posX > eLaser3[0] and self.posX < eLaser3[0] + (X-1460) and self.posY > eLaser3[1])
        or (self.posX > eLaser4[0] and self.posX < eLaser4[0] + (X-1460) and self.posY > eLaser4[1])
        or (self.posX > eLaser5[0] and self.posX < eLaser5[0] + (X-1460) and self.posY > eLaser5[1])):
                self.lives-= 1
                self.reset = True
           
    #animate the ninja during jumping and running
    def animation(self):
        if self.jumping == False:
            #shows motion of running
            if self.frameR >= len(self.sprites.running):
                self.frameR = 0
            self.image = self.sprites.running[self.frameR]
            self.image = pygame.transform.scale(self.image, (57,67))
            self.frameR+=1
        else:
            #show motion of jumping
            self.image = pygame.image.load("../animation/jumping/1.PNG")
            self.image = pygame.transform.scale(self.image, (57,67))
       
    #allows the player to conduct actions like falling and landing
    def checkStatusY(self, Y):
       
        #player reaches top height
        if self.jumping:
            if self.posY <= Y-600:
                self.speed = -15.5
            self.reachingTop = False
           
        #player lands
        if self.posY >= Y-170 and self.falling == False:
            self.speed = 0 #speed is resetted to 0
            self.jumping = False
       
        #player falls down a gap
        if self.falling == True:
            if(self.posY >= Y+100):
                self.reset = True
                self.speed = 0
                self.jumping = False
                self.falling = False
           
class spriteSheet():
   
    #images for different frames of actions (running, jumping etc.)
    def __init__(self):
        self.running = [pygame.image.load("../animation/running/1.PNG"),
                       pygame.image.load("../animation/running/2.PNG"),
                       pygame.image.load("../animation/running/3.PNG"),
                       pygame.image.load("../animation/running/4.PNG"),
                       pygame.image.load("../animation/running/5.PNG"),
                       pygame.image.load("../animation/running/6.PNG")]
       
class eLasers():
   
    #initial electronic lasers x co-ordinate
    def init(self, rect2, rect3, rect4, rect5, Y):
        self.heights = [Y-210,Y-195]
        self.eLaser1 = [rect2.left + random.randint(100,130), self.heights[random.randint(0,1)]]
        self.eLaser2 = [rect3.left + random.randint(80, 120), self.heights[random.randint(0,1)]]
        self.eLaser3 = [rect4.left + random.randint(70, 100), self.heights[random.randint(0,1)]]
        self.eLaser4 = [rect5.left + random.randint(100, 200), self.heights[random.randint(0,1)]]
        self.eLaser5 = [rect5.left + random.randint(390, 450), self.heights[random.randint(0,1)]]
       
    #re-spawning of the electronic lasers if they get off screen
    def checkRespawn(self, rect1, rect2, rect3, X):
        if self.eLaser1[0] + X-1460 < -100:
            self.eLaser1[0] = random.randint(1700,1750)
            self.eLaser1[1] = self.heights[random.randint(0,1)]
        if self.eLaser2[0] + X-1460 < -100:
            self.eLaser2[0] = random.randint(2000,2300)
            self.eLaser2[1] = self.heights[random.randint(0,1)]
        if self.eLaser3[0] + X-1460 < -100:
            self.eLaser3[0] = random.randint(2600,2900)
            self.eLaser3[1] = self.heights[random.randint(0,1)]
        if self.eLaser4[0] + X-1460 < -100:
            self.eLaser4[0] = random.randint(3200,3300)
            self.eLaser4[1] = self.heights[random.randint(0,1)]
        if self.eLaser5[0] + X-1460 < -100:
            self.eLaser5[0] = random.randint(3550,3600)
            self.eLaser5[1] = self.heights[random.randint(0,1)]
           
def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init() #Prepare the pygame module for use
   
    clock = pygame.time.Clock()
    FPS = 60

    #screen dimensions
    X = 1500
    Y = 600

    #create game window
    screen = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("Starnight Runner")
   
   
    #-----------------------------Program Variable Initialization----------------------------#
    #load background image
    bg = pygame.image.load("../bg.png").convert()
    bg_width = bg.get_width()
    bg_rect = bg.get_rect()
   
    #load moon image
    moon = pygame.image.load("../moon.png")
    moon = pygame.transform.scale(moon, (X-1350,Y-400))
   
    #load the trees in the background
    trees = pygame.image.load("../tree.png")
    trees = pygame.transform.scale(trees, (X-1420,Y-520))
   
    treesX = [random.randint(200,300), random.randint(550,610), random.randint(950,1100), random.randint(1300,1400), random.randint(1650, 1700)] #generate initial x positions to place the background trees
   
    #make scrolling work
    scroll = 0
    tiles = math.ceil(X  / bg_width) + 1
   
    #load the electronic laser
    eLaser = pygame.image.load("../e-laser.png")
    eLaser = pygame.transform.scale(eLaser, (X-1460,Y-505))
   
    laser = eLasers() #e-laser object created
   
    p = Player(X,Y) #player object created
   
    font = pygame.font.Font('freesansbold.ttf', 32) #render font

    #-----------------------------Main Program Loop---------------------------------------------#
    run = True
    while run:
        #-----------------------------Event Handling-----------------------------------------#
        clock.tick(FPS)
       
        #draw scrolling background
        for i in range(0, tiles):
          screen.blit(bg, (i * bg_width + scroll, 0))
         
        screen.blit(moon, (X-200,Y-580)) #draw the moon on the screen
       
        p.animation() #update current frame

        p.checkStatusY(Y) #allows the player to land, fall etc.
           
        if(p.reset):
            p.posY = Y-170
            
            #initial rectangles co-ordinates + length and width
            rect1 = pygame.Rect(-90, 500, 500, 100)
            rect2 = pygame.Rect(random.randint(510,530), 500, 250, 100)
            rect3 = pygame.Rect(random.randint(850,875), 500, 350, 100)
            rect4 = pygame.Rect(random.randint(1300,1350), 500, 200, 100)
            rect5 = pygame.Rect(random.randint(1630,1660), 500, 230, 100)
           
            laser.init(rect2,rect3,rect4, rect5, Y) #initial laser co-ordinates
           
            treesX = [random.randint(200,300), random.randint(550,610), random.randint(950,1100), 1400, 1700] #generate initial x positions to place the background trees
           
            p.reset = False
            p.canJump = True
       
        #draw the background trees on the screen
        screen.blit(trees, (treesX[0],Y-180))
        screen.blit(trees, (treesX[1],Y-180))
        screen.blit(trees, (treesX[2],Y-180))
        screen.blit(trees, (treesX[3],Y-180))
        screen.blit(trees, (treesX[4],Y-180))
       
        #scrolling of the trees
        treesX[0] -= 4
        treesX[1] -= 4
        treesX[2] -= 4
        treesX[3] -= 4
        treesX[4] -= 4
       
        #re-spawning of the trees
        if treesX[0] + 80 < -100:
            treesX[0] = rect1.left + random.randint(50, 100)
        if treesX[1] + 80 < -100:
            treesX[1] = rect2.left + random.randint(40, 50)
        if treesX[2] + 80 < -100:
            treesX[2] = rect3.left + random.randint(60, 120)
        if treesX[3] + 80 < -100:
            treesX[3] = rect4.left + random.randint(20, 40)
        if treesX[4] + 80 < -100:
            treesX[4] = rect5.left + random.randint(50, 70)
       
        screen.blit(p.image, (p.posX,p.posY)) #draw current player frame
       
        p.collisionGaps(rect1,rect2,rect3,rect4,rect5, Y) #check if the player falls into a gap
        
        #draw the electronic lasers
        screen.blit(eLaser, (laser.eLaser1[0],laser.eLaser1[1]))
        screen.blit(eLaser, (laser.eLaser2[0],laser.eLaser2[1]))
        screen.blit(eLaser, (laser.eLaser3[0],laser.eLaser3[1]))
        screen.blit(eLaser, (laser.eLaser4[0],laser.eLaser4[1]))
        screen.blit(eLaser, (laser.eLaser5[0],laser.eLaser5[1]))
       
        #scroll the electronic lasers
        laser.eLaser1[0] -= 5
        laser.eLaser2[0] -= 5
        laser.eLaser3[0] -= 5
        laser.eLaser4[0] -= 5
        laser.eLaser5[0] -= 5
           
        #draw the bottom surfaces
        pygame.draw.rect(screen, (0,0,0), rect1)
        pygame.draw.rect(screen, (0,0,0), rect2)
        pygame.draw.rect(screen, (0,0,0), rect3)
        pygame.draw.rect(screen, (0,0,0), rect4)
        pygame.draw.rect(screen, (0,0,0), rect5)
        
        laser.checkRespawn(rect1,rect2,rect3, X) #re-spawns the lasers when they get off screen
        
        p.collisionLasers(laser.eLaser1, laser.eLaser2, laser.eLaser3, laser.eLaser4, laser.eLaser5, X, Y) #checks for the collision of the player with the lasers
       
        randGapsX = [random.randint(595, 615), random.randint(365,375), random.randint(475,500), random.randint(295,325)] #random x positions of the bottom surface (gaps)
       
        #bottom surface spawning
        if(rect1.left + 500 > -100):
            rect1.left -= 4 #scrolling the bottom surface
        else:
            rect1.left = 1500 #resets the bottom surface if it gets off screen
        if(rect2.left + 250 > -100):
            rect2.left -= 4 #scrolling the bottom surface
        else:
            rect2.left = rect1.left + randGapsX[0] #resets the bottom surface if it gets off screen
        if(rect3.left + 350 > -100):
            rect3.left -= 4 #scrolling the bottom surface
        else:
            rect3.left = rect2.left + randGapsX[1] #resets the bottom surface if it gets off screen
        if(rect4.left + 200 > -100):
            rect4.left -= 4 #scrolling the bottom surface
        else:
            rect4.left = rect3.left + randGapsX[2] #resets the bottom surface if it gets off screen
        if(rect5.left + 500 > -100):
            rect5.left -= 4 #scrolling the bottom surface
        else:
            rect5.left = rect4.left + randGapsX[3] #resets the bottom surface if it gets off screen
       
        scroll -= 5 #scroll background

        #display the lives left
        livesLeft = font.render(('Lives Left: ' + str (p.lives)), True, (255,255,255))
        livesLeftRect = livesLeft.get_rect()
        livesLeftRect.center = (X-1375, Y-560)
        screen.blit(livesLeft, livesLeftRect)

        #reset scroll
        if abs(scroll) > bg_width:
          scroll = 0
       
        #lives of the player has run out (game over)
        if p.lives == 0 and p.falling == False:
            run = False
            print("Game Over!")
       
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #detect if a key has been pressed
            if event.type == pygame.KEYDOWN:
                #detect if that key is the upper arrow
                if event.key == pygame.K_UP and not p.jumping:
                    p.jumping = True
                    if(p.canJump):
                        p.jump()
        #-----------------------------Program Logic---------------------------------------------#
        # Update the y position and speed of the player
        p.posY -= p.speed
        p.speed += -1.0

        #-----------------------------Drawing Everything-------------------------------------#
        pygame.display.update()

    pygame.quit() #Closes the window, once we leave the loop

main()
