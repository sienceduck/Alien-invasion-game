from pathlib import Path


class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
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
        self.ship_lives_left = self.settings.ship_limmit
        self.score = 0
        self.level = 1

    # We’ll make one GameStats instance for the entire time Alien Invasion is
    # running, but we’ll need to reset some statistics each time the player
    # starts a new game. To do this, we’ll initialize most of the statistics
    # in the reset_stats() method, instead of directly in __init__().
