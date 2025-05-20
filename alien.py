import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen  # to get game window resolution
        self.settings = ai_game.settings  # to get alien_speed

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load("images/alien_ship.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        # add space to the left equall image's width
        self.rect.y = self.rect.height
        # add space to the top equall image's height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        # check if one or another condition is satisfied, then return - True
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the alien to the right or left."""
        # if the direction is right, than speed * 1; if left, speed * -1
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
