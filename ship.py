import pygame

# Pygame is efficient in treating all game elements like rectangles (rects),
# cause they are simple geometric shapes, even if they’re not exactly shaped
# like rectangles. Useful for colliding objects.


class Ship:
    """A class to manage ship"""

    # referencing the AlienInvasion instance (ai_game) to obtain its parameters
    def __init__(self, ai_game):
        """Initialize the ship and place it's starting position"""

        self.screen = ai_game.screen

        # method .get_rect() allows us to place the ship
        # in the correct location on the screen.
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load("images/ship_nightraider.bmp")
        # the native image format for pygame is .bmp

        self.rect = self.image.get_rect()  # this will be used to place the ship

        """
        When working with a rect object, x and y coordinates of the top, bottom,
        left, and right edges of the rectangle can be used as well as the center,
        to place the object. 
        """
        """
        For centering a game element, work with: center, centerx, centery
        attributes of a rect. When working at an edge of the screen, work with: 
        top, bottom, left, right attributes.  
        Also combined attributes: midbottom, midtop, midleft, midright.
        """

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        """
        In Pygame, the origin (0, 0) is at the top-left corner of the screen,
        and coordinates increase as you go down and to the right, f.e. on a
        1200×800 screen, the origin is at the lowest coord are at (1200, 800).
        """

    def blitme(self):
        """Draw the ship and it's current location"""
        self.screen.blit(self.image, self.rect)
