class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ship_left = self.settings.ship_limmit

    # We’ll make one GameStats instance for the entire time Alien Invasion is
    # running, but we’ll need to reset some statistics each time the player
    # starts a new game. To do this, we’ll initialize most of the statistics
    # in the reset_stats() method, instead of directly in __init__().
