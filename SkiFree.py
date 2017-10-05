import pygame, sys, os, math
from pygame.locals import *
from random import randint

from spriteHelper import SpriteSheet


WINDOWWIDTH = 800
WINDOWHEIGHT = 600
GAMENAME = "SkiFree-Py"
FRAMERATE = 60
BGCOLOR = (255,255,255)

class Game:
    ##########CLASS VARIABLES##########
    player = None
    
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
        spriteSheet = SpriteSheet("SkiFreeSprites.png")
        self.skiDownSprite = spriteSheet.get_image(0,950,172,350)
        self.skiDownSprite = pygame.transform.scale(
            self.skiDownSprite,(int(172*.25),int(350*.25)))
        self.player = self.skiDownSprite
        ##########GAME LOOP##########
        while playing:
            delta = clock.tick(FRAMERATE)
            
            ##########EVENT HANDLING##########
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
            ##################################
                    
            self.processLogic()
            self.drawScreen()
            pygame.display.flip()
    
    ##########MAKES CHANGES FROM LAST FRAME##########
    def processLogic(self):
        pass
    
    ##########DRAWS THE FRAME##########
    def drawScreen(self):
        self.surface.fill(BGCOLOR)
        skiOffset = (
            self.center[0]-(self.player.get_rect().width/2),
            self.center[1]-(self.player.get_rect().height/2)
            )
        self.surface.blit(self.skiDownSprite,skiOffset)
        
    def quit(self):
        pygame.quit()
        sys.exit()
        
##########STARTS EVERYTHING##########
if __name__=='__main__':
    game = Game()
    game.main()

