# This file is a specific module for game's settings


class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's stattic settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)

        # Ship settings
        self.ship_limmit = 3

        # Bullet settings
        self.bullet_width = 4  # base 4
        self.bullet_height = 14
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 5

        # ALien settings
        self.fleet_drop_speed = 10  # 10
        # shows how quickly fleet drops down each time it reaches either edge

        # Difficulty level
        self.difficulty_lvl = ""

        # How quickly the game speeds up
        self.speedup_scale = 1.1  # default is 1.1
        # How quickly alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 3.5
        self.bullet_speed = 5.0
        self.alien_speed = 1.0  # 1.0 base value

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = 50

        # Increase speed based on difficulty chosen
        self.increase_speed()

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        # after the game speeds up, player gains more points for alien
        # print(self.alien_points) - to check if it works
