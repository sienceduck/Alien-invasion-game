"""This file is part of the 12.4, 12.5, 12.6, 13.5, 13.6, 14.8 tryit exercises"""

from pathlib import Path


class GameStats:
    """Track statistics for Rocket Penguin"""

    def __init__(self, rp_game):
        """Initialize statistics"""
        self.settings = rp_game.settings
        self.reset_stats()

        # High score should never be reset
        self.high_score = 0

        # Import saved highest score
        save_path = Path("score_save/highest_score.txt")
        try:
            contents = save_path.read_text()
            self.high_score = int(contents)
            # print(self.high_score) - checking if its working
        except FileNotFoundError:
            pass

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.penguin_lives_left = self.settings.penguin_limmit
        self.score = 0
        self.level = 1

    # We’ll make one GameStats instance for the entire time Rocket Penguin is
    # running, but we’ll need to reset some statistics each time the player
    # starts a new game. To do this, we’ll initialize most of the statistics
    # in the reset_stats() method, instead of directly in __init__().
