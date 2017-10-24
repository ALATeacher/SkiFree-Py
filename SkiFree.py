import pygame, sys, os, math
from pygame.locals import *
from random import randint

from spriteHelper import SpriteSheet

#test
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
GAMENAME = "SkiFree-Py"
FRAMERATE = 60
BGCOLOR = (255,255,255)

GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)


class Obstacle:
    collider = None
    image = None
    def __init__(self,image,x,y):
        self.image = image
        self.x = x
        self.y = y
    def process(self,delta):
        pass
    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y))
        #pygame.draw.rect(surface,GREEN,self.getCollider()) #testing
    def getCollider(self):
        collider = self.image.get_rect()
        collider.x = self.x
        collider.y = self.y
        return collider
    

class Tree(Obstacle):
    def __init__(self,image,x,y):
        self.image = image
        self.x = x
        self.y = y
    def getCollider(self):
        x = int(82*.25)
        y= int(382*.25)
        collider = pygame.Rect(self.x+x,self.y+y,25,13)
        return collider

class Player:
    collider = None
    current = 2
    position = []
    centerOfScreen = (0,0)
    def __init__(self):
        pass
    def getCollider(self):
        centerX = (
            (WINDOWWIDTH/2)-(self.position[self.current].get_rect().width/2))
        centerY =(
            (WINDOWHEIGHT/2)-(self.position[self.current].get_rect().height/2))
        collider = self.position[self.current].get_rect()
        centerOfScreen = (centerX,centerY)
        collider.x = centerOfScreen[0]
        collider.y = centerOfScreen[1]
        return collider
    def draw(self,surface):
        centerX = (
            (WINDOWWIDTH/2)-(self.position[self.current].get_rect().width/2))
        centerY =(
            (WINDOWHEIGHT/2)-(self.position[self.current].get_rect().height/2))
        centerOfScreen = (centerX,centerY)
        surface.blit(self.position[self.current],centerOfScreen)
        #pygame.draw.rect(surface,GREEN,self.getCollider())
    def changeDirection(self,direction):
        if direction==2:
            self.current = 2
        else:
            self.current+=direction
            if self.current<0:
                self.current = 0
            elif self.current>4:
                self.current = 4
    def crashed(self):
        self.current = 5
    def getAngle(self):
        skiSpeed = 1
        x=0
        y=0
        if self.current == 2:
            x = 0
            y = 1
        elif self.current == 1:
            y = .7071
            x = .7071
        elif self.current==3:
            y = .7071
            x = -.7071
        elif self.current == 0:
            y = .1
            x = .9
        else:
            y = .1
            x = -.9
        return (x,-y)
        

class Game:
    ##########CLASS VARIABLES##########
    player = None
    position = 2
    skiSpeed = 10
    maxSkiSpeed = 20
    angle = 0
    trees = []
    chanceTreeIsAdded = 10 #out of 100
    
    ##########CONSTRUCTOR##########
    def __init__(self):
        pass        
    
    ##########MAIN FUNCTION##########
    def main(self):
        playing = True
        pygame.init()
        clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
        self.center = (WINDOWWIDTH/2,WINDOWHEIGHT/2)
        pygame.display.set_caption(GAMENAME)
        
        ##########LOAD IMAGES##########
        self.spriteSheet = SpriteSheet("SkiFreeSprites.png")
        self.skiDownSprite = self.spriteSheet.get_image(0,950,172,350)
        self.skiDownSprite = pygame.transform.scale(
            self.skiDownSprite,(int(172*.25),int(350*.25)))
        
        self.skiLeftAngleSprite = self.spriteSheet.get_image(900,1020,335,278)
        self.skiLeftAngleSprite = pygame.transform.scale(
            self.skiLeftAngleSprite,(int(335*.25),int(278*.25)))
        
        self.skiRightAngleSprite = pygame.transform.flip(
            self.skiLeftAngleSprite, True, False)
        
        self.skiLeftSprite = self.spriteSheet.get_image(570,1025,290,269)
        self.skiLeftSprite = pygame.transform.scale(
            self.skiLeftSprite,(int(290*.25),int(269*.25)))
        
        self.skiRightSprite = pygame.transform.flip(
            self.skiLeftSprite, True, False)
        
        self.skiCrashed = self.spriteSheet.get_image(250,1100,234,193)
        self.skiCrashed = pygame.transform.scale(
            self.skiCrashed,(int(234*.25),int(193*.25)))
        
        self.treeSprite1 = self.spriteSheet.get_image(980,470,250,438)
        self.treeSprite1 = pygame.transform.scale(
            self.treeSprite1,(int(250*.25),int(438*.25)))
        
        self.player = self.skiDownSprite
        
        self.skiPositions = [self.skiLeftSprite,
                             self.skiLeftAngleSprite,
                             self.skiDownSprite,
                             self.skiRightAngleSprite,
                             self.skiRightSprite,
                             self.skiCrashed]
        self.position = 2
        self.player = Player()
        self.player.position = self.skiPositions
        self.player.current = self.position
        ##########TESTING##########
        #tree = Tree(self.treeSprite1,200,200)
        #self.trees.append(tree)
        
        ##########GAME LOOP##########
        while playing:
            delta = clock.tick(FRAMERATE)
            
            ##########EVENT HANDLING##########
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == KEYDOWN:
                    if event.key==K_LEFT:
                        self.player.changeDirection(-1)
                    elif event.key==K_RIGHT:
                        self.player.changeDirection(1)
                    elif event.key==K_DOWN:
                        self.player.changeDirection(2)
            ##################################
                    
            self.processLogic()
            self.drawScreen()
            pygame.display.flip()
    
    ##########MAKES CHANGES FROM LAST FRAME##########
    def processLogic(self):
        if self.player.current==0 or self.player.current>=4:
            if self.skiSpeed>0:
                self.skiSpeed-=.25
        elif self.skiSpeed < self.maxSkiSpeed:
            self.skiSpeed+=.5
        r = randint(0,100)
        if r<=self.chanceTreeIsAdded:
            self.addTree()
        for t in self.trees:
            direction = self.player.getAngle()
            t.y+=direction[1]*self.skiSpeed
            t.x+=direction[0]*self.skiSpeed
            if t.getCollider().colliderect(self.player.getCollider()):
                #player has hit a tree
                #self.trees.remove(t)
                self.crashed()
    def crashed(self):
        self.player.crashed()
        self.skiSpeed = 0
        for t in self.trees:
            t.y-=60
    ##########DRAWS THE FRAME##########
    def drawScreen(self):
        self.surface.fill(BGCOLOR)
        self.player.draw(self.surface)
        
        for t in self.trees:
            t.draw(self.surface)
    
    def addTree(self):
        y = WINDOWHEIGHT+100
        x = randint(20,WINDOWWIDTH-20)
        tree = Tree(self.treeSprite1,x,y)
        sane = True
        for t in self.trees:
            if t.getCollider().colliderect(tree.getCollider()):
                sane = False
        if sane and self.skiSpeed>=10:
            self.trees.append(tree)
            print("Tree added at %d,%d" % (x,y))
        
    def quit(self):
        pygame.quit()
        sys.exit()
        
##########STARTS EVERYTHING##########
if __name__=='__main__':
    game = Game()
    game.main()


