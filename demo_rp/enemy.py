"""This file is part of the 12.4, 12.5, 12.6, 13.5, 13.6, 14.8 tryit exercises"""

import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """A class to represent a single enemy in the game."""

    def __init__(self, rp_game):
        """Initialize the enemy and set its rect"""
        super().__init__()
        self.screen = rp_game.screen  # to get game window resolution
        self.settings = rp_game.settings  # to get enemy_speed

        # Load the enemy image and set its rect attribute
        self.image = pygame.image.load("images/enemy-rp.bmp")
        self.rect = self.image.get_rect()

        # Store the enemy's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if enemy is at edge of screen"""
        # check if one or another condition is satisfied, then return - True
        return self.rect.left <= 0

    def update(self):
        """Move the enemy to the right with constant speed."""
        self.x -= self.settings.enemy_speed
        self.rect.x = self.x


"""
Refactored code is here:
"""
