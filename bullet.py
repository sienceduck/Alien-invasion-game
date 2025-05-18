import pygame
from pygame.sprite import Sprite

"""
When using sprites, you can group related elements in
your game and act on all the grouped elements at once. 
"""


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        # super() allows us to inherit the parent module's instance,
        # which in our case is AlienInvasion's ai_game

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = self.settings.bullet_colour

        # Create a bullet rect at (0, 0) and then set the correct position
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )  # It isn’t based on an image, so we have to build a rect from scratch
        # using the pygame.Rect() class.

        self.rect.midtop = ai_game.ship.rect.midtop
        # the bullets position will depend on the ship's position
        # now it is set on the top of ship's rect

        # Store the bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""
        # Update the exact position of the bullet
        self.y -= self.settings.bullet_speed  # it will move vertically
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.colour, self.rect)
