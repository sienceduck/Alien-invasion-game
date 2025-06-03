"""This file is part of the 12.4, 12.5, 12.6, 13.5, 13.6, 14.8 tryit exercises"""

from pygame.sprite import Sprite

# Pygame is efficient in treating all game elements like rectangles (rects),
# cause they are simple geometric shapes, even if they’re not exactly shaped
# like rectangles. Useful for colliding objects.


class Penguin(Sprite):
    """A class to manage rocket penguin"""

    # referencing the Rocketpenguin instance (rp_game) to obtain its parameters
    def __init__(self, rp_game, penguin_image):
        """Initialize the penguin and place it's starting position"""
        super().__init__()

        self.screen = rp_game.screen
        self.settings = rp_game.settings

        # method .get_rect() allows us to place the penguin
        # in the correct location on the screen.
        self.screen_rect = rp_game.screen.get_rect()

        # Load the penguin image and get its rect.
        self.image = penguin_image
        # the native image format for pygame is .bmp

        self.rect = (
            self.image.get_rect()
        )  # this will be used to place the penguin

        # Start each new penguin at the top of the screen
        self.rect.midleft = self.screen_rect.midleft

        # Store a float for the penguin's exact horizontal and vertical position.
        self.y = float(self.rect.y)  # needed to move by fraction of a pixel

        # Movement flag; start with a penguin that's not moving
        self.moving_top = False
        self.moving_bottom = False

    def update(self):
        """Update the penguin's position based on the movement flag"""
        # Update the penguin's y value, not the rect.

        # comparing rect and screen_rect to see if penguin has reached the border
        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            # if not, move it in this direction
            self.y += self.settings.penguin_speed
        # if it had reached, it can go no further
        if self.moving_top and self.rect.top > 0:
            self.y -= self.settings.penguin_speed

        # using if statement for continuos movement in RocketPenguin run_game
        # while loop

        # Update rect object from self.y
        self.rect.y = self.y
        # only the integer portion of self.y will be assigned to self.rect.y

    def center_penguin(self):
        """Center the ship on the screen"""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the penguin and it's current location"""
        self.screen.blit(self.image, self.rect)


"""
"""
