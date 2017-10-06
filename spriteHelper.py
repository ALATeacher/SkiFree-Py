import pygame

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # Colors
    BLACK    = (   0,   0,   0) 
    WHITE    = ( 255, 255, 255) 
    BLUE     = (   0,   0, 255)
 
    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
 
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
 
 
    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
 
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
        # Assuming black works as the transparent color
        image.set_colorkey(self.WHITE)
 
        # Return the image
        return image

class UniformSpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
 
    def __init__(self, file_name,width,height):
        """ Constructor. Pass in the file name of the sprite sheet. """
        
        # Colors
        BLACK    = (   0,   0,   0) 
        WHITE    = ( 255, 255, 255) 
        BLUE     = (   0,   0, 255)
         
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.width = width
        self.height = height
 
 
    def get_image(self, x, y):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
        # Create a new blank image
        x = x*width
        y = y*width
        image = pygame.Surface([self.width, self.height]).convert()
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
        # Assuming black works as the transparent color
        image.set_colorkey(self.BLACK)
 
        # Return the image
        return image