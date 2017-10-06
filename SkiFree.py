import pygame, sys, os, math
from pygame.locals import *
from random import randint

from spriteHelper import SpriteSheet


WINDOWWIDTH = 800
WINDOWHEIGHT = 600
GAMENAME = "SkiFree-Py"
FRAMERATE = 60
BGCOLOR = (255,255,255)


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
    def getCollider(self):
        collider = self.image.get_rect()
        collider.x = self.x
        collider.y = self.y
        return collider


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
        
        self.treeSprite1 = self.spriteSheet.get_image(980,470,250,438)
        self.treeSprite1 = pygame.transform.scale(
            self.treeSprite1,(int(250*.25),int(438*.25)))
        
        self.player = self.skiDownSprite
        
        self.skiPositions = [self.skiLeftSprite,
                             self.skiLeftAngleSprite,
                             self.skiDownSprite,
                             self.skiRightAngleSprite,
                             self.skiRightSprite]
        self.position = 2
        ##########GAME LOOP##########
        while playing:
            delta = clock.tick(FRAMERATE)
            
            ##########EVENT HANDLING##########
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == KEYDOWN:
                    if event.key==K_LEFT:
                        if self.position>0:
                            self.position-=1
                    elif event.key==K_RIGHT:
                        if self.position<4:
                            self.position+=1
            ##################################
                    
            self.processLogic()
            self.drawScreen()
            pygame.display.flip()
    
    ##########MAKES CHANGES FROM LAST FRAME##########
    def processLogic(self):
        if self.position==0 or self.position==4:
            if self.skiSpeed>0:
                self.skiSpeed-=.25
        elif self.skiSpeed < self.maxSkiSpeed:
            self.skiSpeed+=.5
        r = randint(0,100)
        if r<=self.chanceTreeIsAdded:
            self.addTree()
        for t in self.trees:
            if self.position == 2:
                y = self.skiSpeed
                x = 0
            elif self.position == 1:
                y = int(self.skiSpeed*.7071)
                x = int(self.skiSpeed*.7071)
            elif self.position==3:
                y = int(self.skiSpeed*.7071)
                x = -int(self.skiSpeed*.7071)
            elif self.position == 0:
                y = int(self.skiSpeed*.1)
                x = int(self.skiSpeed*.9)
            else:
                y = int(self.skiSpeed*.1)
                x = -int(self.skiSpeed*.9)
            t.y-=y
            t.x+=x
    
    ##########DRAWS THE FRAME##########
    def drawScreen(self):
        self.surface.fill(BGCOLOR)
        skiOffset = (
            self.center[0]-(self.player.get_rect().width/2),
            self.center[1]-(self.player.get_rect().height/2)
            )
        self.surface.blit(self.skiPositions[self.position],skiOffset)
        
        for t in self.trees:
            t.draw(self.surface)
    
    def addTree(self):
        y = WINDOWHEIGHT+100
        x = randint(20,WINDOWWIDTH-20)
        tree = Obstacle(self.treeSprite1,x,y)
        sane = True
        for t in self.trees:
            if t.getCollider().colliderect(tree.getCollider()):
                sane = False
        if sane:
            self.trees.append(tree)
            print("Tree added at %d,%d" % (x,y))
        
    def quit(self):
        pygame.quit()
        sys.exit()
        
##########STARTS EVERYTHING##########
if __name__=='__main__':
    game = Game()
    game.main()


