import sys

import pygame


class AlienInvasion:
    """Overal class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create game resources."""
        pygame.init()

        # create a display window
        self.screen = pygame.display.set_mode((1200, 800))
        # create a clock for controling fps cap via pygame Clock class
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Watch for keyboard and mouse events
            for event in pygame.event.get():
                """An event is an action that the user performs while playing the game,
                such as pressing a key or moving the mouse."""

                """An event loop serves to listen for events and perform appropriate
                tasks. """
                if event.type == pygame.QUIT:
                    sys.exit()

            # Make the most recent drawn screen visible
            pygame.display.flip()
            """In other words, this method continually updates the display to show the
            new positions of game elements and hide the old ones."""

            # tick() method takes one argument: the frame rate for the game.
            self.clock.tick(60)


"""Place run_game() in an if block that only runs if the file is called directly. """
if __name__ == "__main__":
    # Make a game instant and run the game
    ai = AlienInvasion()
    ai.run_game()


# Ideally, games should run at the same speed, or frame rate, on all systems.
