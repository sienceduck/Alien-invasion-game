"""This file is part of the 12.4, 12.5, 12.6, 13.5, 13.6, 14.8 tryit exercises"""

import pygame
from pygame.sprite import Sprite

"""
When using sprites, you can group related elements in
your game and act on all the grouped elements at once. 
"""


class Rocket(Sprite):
    """A class to manage rockets fired from the penguin"""

    def __init__(self, rp_game):
        """Create a rocket object at the penguin's current position"""
        super().__init__()
        # super() allows us to inherit the parent module's instance,
        # which in our case is RocketPenguin's rp_game

        self.screen = rp_game.screen
        self.settings = rp_game.settings

        # Create a rocket rect at (0, 0) and then set the correct position
        self.image = pygame.image.load("images/spr_missile_half.bmp")

        self.rect = self.image.get_rect()  # used to place rocket on screen

        self.rect.midright = rp_game.penguin.rect.midright
        # the rockets position will depend on the penguin's position
        # now it is set on the top of penguin's rect

        # Store the rocket's position as a float
        self.x = float(self.rect.x)

    def update(self):
        """Move the rocket up the screen"""
        # Update the exact position of the rocket
        self.x += self.settings.rocket_speed  # it will move vertically
        # Update the rect position
        self.rect.x = self.x

    def blitrocket(self):
        """Draw the rocket and it's current location"""
        self.screen.blit(self.image, self.rect)
