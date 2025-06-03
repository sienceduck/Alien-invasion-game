"""This file is part of the 12.4, 12.5, 12.6, 13.5, 13.6, 14.8 tryit exercises"""

import pygame


class Tutorial:
    """Create tutorial screen at the begining of the game"""

    def __init__(self, rp_game):
        """Initialize screen attributes"""
        self.screen = rp_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions
        self.settings = rp_game.settings
        self.dimensions = (
            self.settings.screen_width,
            self.settings.screen_height,
        )

        self.font = pygame.font.SysFont(None, 38)
        # None tells Pygame to use default font, 48 - size
        self.text_colour = (0, 0, 0)
        self.screen_colour = (255, 255, 255)

        # Create background surface
        self.t_surf = pygame.Surface(self.dimensions)
        self.t_surf.set_alpha(128)  # alpha level (transparency)
        self.t_surf.fill(self.screen_colour)  # this fills the entire surface

        # The messages need to be prepped only once
        self.prep_messages_for_images()

    def prep_messages_for_images(self):
        """Prepare the tutorial messages for the game"""
        self.prep_score_tutor()
        self.prep_high_score_tutor()
        self.prep_level_tutor()
        self.prep_penguin_lives_tutor()
        self.prep_start_tutor()

    def prep_score_tutor(self):
        """Explain score"""
        # prepare message and render it
        score_str = "Your current score"
        self.score_image = self.font.render(score_str, True, self.text_colour)

        # get the rect item and place it
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 47
        self.score_rect.top = 20

    def prep_high_score_tutor(self):
        """Explain high score"""
        # dict for storing items, list with sentences
        self.high_score_dict = {}
        high_score_str = ["Your highest score,", "saved from last game"]

        line_step = 60
        # render text and set the rect
        for line in range(len(high_score_str)):
            txt = self.font.render(high_score_str[line], True, self.text_colour)

            txt_rect = txt.get_rect()
            txt_rect.centerx = self.screen_rect.centerx
            txt_rect.top = line_step
            # add items to dictionary
            self.high_score_dict[txt] = txt_rect
            # get down by line step
            line_step += int(line_step / 2)

    def prep_level_tutor(self):
        """Explain levels"""
        level_str = "Level, you're currently in"
        self.level_image = self.font.render(level_str, True, self.text_colour)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 15

    def prep_penguin_lives_tutor(self):
        """Explain lives"""
        lives_str = "Lives you have left"
        self.lives_image = self.font.render(lives_str, True, self.text_colour)

        self.lives_rect = self.score_image.get_rect()
        self.lives_rect.left = self.screen_rect.left + 20
        self.lives_rect.top = 60

    def prep_start_tutor(self):
        """Explain games's objective"""
        start_str = "Survive 10 levels!"
        self.start_image = self.font.render(start_str, True, self.text_colour)

        self.start_rect = self.start_image.get_rect()
        self.start_rect.center = self.screen_rect.center
        self.start_rect.y -= 60

    def draw_tutorial(self):
        """Draw tutorail messages message"""
        # transparent background
        self.screen.blit(self.t_surf, (0, 0))
        # all the messages
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.start_image, self.start_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.lives_image, self.lives_rect)
        # draw all the lines as key - img, value - rect
        for key, value in self.high_score_dict.items():
            self.screen.blit(key, value)
