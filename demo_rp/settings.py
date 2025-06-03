"""This file is part of the 12.4, 12.5, 12.6, 13.5, 13.6, 14.8 tryit exercises"""

import random


class Settings:
    """A class to store all settings for Rocket Penguin"""

    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)

        # Penguin's settings
        self.penguin_limmit = 3

        # Enemy settings
        self.enemy_beaten_max = 10
        self.enemy_spawn_interval = random.randint(1000, 2000)

        # Rocket settings
        self.rockets_allowed = 20

        # Number of horizontal rows
        self.number_of_rows = 6
        self.row_margin = self.screen_height / self.number_of_rows

        # Difficulty level
        self.difficulty_lvl = ""

        # How quickly the game speeds up
        self.speedup_scale = 1.1  # default is 1.1
        # How quickly enemy point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.penguin_speed = 3.5
        self.enemy_speed = 3.0  # 1.0 base value
        self.rocket_speed = 5.0

        # Scoring settings
        self.enemy_points = 50
        self.enemy_beaten = 0

    def increase_speed(self):
        """Increase speed settings and enemy point values"""
        self.penguin_speed *= self.speedup_scale
        self.rocket_speed *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)
        # after the game speeds up, player gains more points for enemy
        # print(self.enemy_points) - to check if it works
