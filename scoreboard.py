import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_colour = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images
        self.prep_images()

    def prep_images(self):
        """Prepare the UI images for the game"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship_lives()

    def prep_score(self):
        """Turn the score into a rendered image"""
        # if given negative argument, funct will round to nearest 10, 100, 1000...
        rounded_score = round(self.stats.score, -1)
        # :, are FORMAT SPECIFIERS for f-strings, which
        # tells Python to place commas in big numbers
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(
            score_str, True, self.text_colour, self.settings.bg_colour
        )

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        # this all to display the changing score value correctly

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        # Round to the nearest 10 and format with commas
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_colour, self.settings.bg_colour
        )

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level value into a rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_colour, self.settings.bg_colour
        )

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ship_lives(self):
        """Show how many ship lives are left"""
        self.ships = Group()
        ship_image = pygame.image.load("images/ship_nightraider_icon.bmp")
        for ship_number in range(self.stats.ship_lives_left):
            ship = Ship(self.ai_game, ship_image)
            ship.rect.scale_by(0.5, 0.5)
            # ships appear with 10 pixel margin
            ship.rect.x = 10 + ship_number * ship.rect.width
            # ships appear at the top left corner
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            self.prep_level()

    def show_score(self):
        """Draw scores and levels to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
