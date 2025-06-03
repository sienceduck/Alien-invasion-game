"""This file is part of the 12.4, 12.5, 12.6, 13.5, 13.6, 14.8 tryit exercises"""

import pygame.font  # .font module lets write and render text

# --- constants --- (UPPER_CASE names)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# --- classes --- (CamelCase names)


class PlayButton:
    """A class to build play button for the game"""

    def __init__(self, ai_game, msg):  # msg - message text
        """Initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.dimensions = (200, 50)  # width and height
        self.button_colour = GREEN
        self.text_colour = WHITE
        self.font = pygame.font.SysFont(None, 48)
        # None tells Pygame to use default font, 48 - size

        # Build the button's rect object and center it
        self.rect = pygame.Rect((0, 0), self.dimensions)
        # self.rect_pos = self.rect.get_rect()
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Render msg into image and center text on the button"""
        # font.render turns text into an image
        self.msg_image = self.font.render(
            msg, True, self.text_colour, self.button_colour
        )
        # True refers to toggling antialiasing (smoothing edges)
        # button_colour renders a background of text same as button's colour
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        # center msg_image on button's center

    def draw_button(self):
        """Draw blank button and then draw message"""
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
