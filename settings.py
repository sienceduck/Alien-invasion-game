# This file is a specific module for game's settings


class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)

        # Ship settings
        self.ship_speed = 3.5

        # Bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 4
        self.bullet_height = 14
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 5
