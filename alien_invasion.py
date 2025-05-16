import sys

import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overal class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create game resources."""
        pygame.init()
        self.settings = Settings()  # import settings

        # create a display window
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        """
        When creating the screen surface, we pass a size of (0, 0) and the
        parameter pygame.FULLSCREEN. This tells Pygame to figure out a window
        size that will fill the screen. 
        """
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        """
        Use the width and height attributes of the screen’s rect to update
        the settings object.
        """

        self.ship = Ship(self)  # import ship

        # create a clock for controling fps cap via pygame Clock class
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Alien Invasion")

        # self argument refers to the current instance of AlienInvasion
        # and so it gives access to the game's resources

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            # tick() method takes one argument: the frame rate for the game.
            # Ideally, games should run at the same speed, or frame rate, on all systems.
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keystrokes and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # when you closes the game's window
                sys.exit()  # system call to kill process

            elif event.type == pygame.KEYDOWN:
                # Each keypress is registered as a KEYDOWN event.
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                # KEYUP event is used when the key is released
                self._check_keyup_events(event)

        # Whenever the key is pressed, that keypress is registered in Pygame as
        # an event. Each event is picked up by the pygame.event.get() method.

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # when q is pressed, game process killed
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_colour)
        self.ship.blitme()
        pygame.display.flip()
        # flip() the display to put your work on screen


"""Place run_game() in an if block that only runs if the file is called directly. """
if __name__ == "__main__":
    # Make a game instant and run the game
    ai_game = AlienInvasion()
    ai_game.run_game()


# In big projects its important to refactor chunky code. It's good to split method code into
# helper methods. A helper method does work inside a class but isn’t meant to be used by code
# outside the class. In Python, a SINGLE leading underscore indicates a helper method.
