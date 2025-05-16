import sys

import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overal class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create game resources."""
        pygame.init()
        self.settings = Settings()

        # create a display window
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # create a clock for controling fps cap via pygame Clock class
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        # self argument refers to the current instance of AlienInvasion
        # and so it gives access to the game's resources

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self._update_screen()
            # tick() method takes one argument: the frame rate for the game.
            # Ideally, games should run at the same speed, or frame rate, on all systems.
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keystrokes and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_colour)
        self.ship.blitme()
        pygame.display.flip()


"""Place run_game() in an if block that only runs if the file is called directly. """
if __name__ == "__main__":
    # Make a game instant and run the game
    ai_game = AlienInvasion()
    ai_game.run_game()


# In big projects its important to refactor chunky code. It's good to split method code into
# helper methods. A helper method does work inside a class but isn’t meant to be used by code
# outside the class. In Python, a SINGLE leading underscore indicates a helper method.
"""
Replaced code is here:


        # create a display window
        self.screen = pygame.display.set_mode((1200, 800))
        # create a clock for controling fps cap via pygame Clock class
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Alien Invasion")

        # Set the background color.
        self.bg_color = (230, 230, 230)  # such RGB values produce light grey

        # Watch for keyboard and mouse events
            for event in pygame.event.get():
                ""An event is an action that the user performs while playing the game,
                such as pressing a key or moving the mouse.""

                ""An event loop serves to listen for events and perform appropriate
                tasks. ""
                if event.type == pygame.QUIT:
                    sys.exit()


            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_colour)

            self.ship.blitme()

            self.screen.fill(self.bg_colour)

            # Make the most recent drawn screen visible
            pygame.display.flip()
            ""In other words, this method continually updates the display to show the
            new positions of game elements and hide the old ones.""
"""
