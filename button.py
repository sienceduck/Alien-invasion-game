import pygame.font  # .font module lets write and render text
from pygame.sprite import Sprite

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


class DifficultyButton(Sprite):
    """Class for creating difficulty buttons"""

    def __init__(self, ai_game, msg, x, y):
        # Import Sprite funstionality and given parameters
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.msg = msg
        self.x, self.y = x, y

        # Set the dimensions and properties of the button
        self.button_colour = GREEN
        self.text_colour = BLACK
        self.font = pygame.font.SysFont(None, 48)

        # Create and fill the surface
        self.image = pygame.Surface((250, 50))
        self.image.fill(GREEN)

        # Build the button's rect object and place it
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Counter to track button clicks
        self.times_button_clicked = 0

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

    def draw_msg_and_outline(self):
        """Draw message render and outline"""
        self.screen.blit(self.msg_image, self.msg_image_rect)

        # if the button is clicked 2 times, remove outline
        if self.times_button_clicked % 2 != 0:
            self.outline_button()
            # print(self.times_button_clicked) - check if it works

    def check_click(self, mouse_pos):
        """See if any difficulty buttons was pressed"""
        button_clicked = self.rect.collidepoint(mouse_pos)
        dif_lvl = self.settings.difficulty_lvl
        if button_clicked:
            if self.msg == "Easy Mode":
                self.settings.speedup_scale = 1.1
                dif_lvl = "Easy Mode"
            elif self.msg == "Hard Mode":
                self.settings.speedup_scale = 2.0
                dif_lvl = "Hard Mode"
            elif self.msg == "Extreme Mode":
                self.settings.speedup_scale = 2.5
                dif_lvl = "Extreme Mode"
            # print(dif_lvl) - check if it works

            # increase times the button was clicked
            self.times_button_clicked += 1

    def outline_button(self):
        """Outline clicked button"""
        outline_colour = RED
        outline_thickness = 3
        pygame.draw.rect(
            self.screen,
            outline_colour,
            (self.rect.x, self.rect.y, 250, 50),
            outline_thickness,
            border_radius=1,
        )
