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
        self.settings = ai_game.settings

        # method .get_rect() allows us to place the ship
        # in the correct location on the screen.
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load("images/ship_nightrader_small.bmp")
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

        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)  # needed to move by fraction of a pixel

        # Movement flag; start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag"""
        # Update the ship's x value, not the rect.

        # comparing rect and screen_rect to see is ship has reached the border
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # if not, move it in this direction
            self.x += self.settings.ship_speed
        # if it had reached, it can go no further
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # using if statement for continuos movement in AlienInvasion run_game
        # while loop

        # Update rect object from self.x
        self.rect.x = self.x
        # only the integer portion of self.x will be assigned to self.rect.x

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ship and it's current location"""
        self.screen.blit(self.image, self.rect)
