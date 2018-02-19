'''
Created on 14-Nov-2017

@author: kavyareddy
'''

import pygame


import gdp1.spritesheet.constants

from gdp1.spritesheet.platforms import MovingPlatform
from gdp1.spritesheet.spritesheet_functions import SpriteSheet

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(gdp1.spritesheet.constants.BLUE)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        self.rect.x = height-20
        self.rect.y = 0
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
        
    def update(self):
        self.rect.x += self.change_x
        self.rect.y += 0
        
        # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 