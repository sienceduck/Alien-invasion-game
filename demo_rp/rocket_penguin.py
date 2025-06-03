"""This file is part of the 12.4, 12.5, 12.6, 13.5, 13.6, 14.8 tryit exercises"""

import random
import sys
from pathlib import Path
from time import sleep

import pygame

from button import PlayButton
from enemy import Enemy
from game_stats import GameStats
from penguin import Penguin
from rocket import Rocket
from scoreboard import Scoreboard
from settings import Settings
from tutorial import Tutorial


class RocketPenguin:
    """Overal class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create game resources."""
        pygame.init()
        self.settings = Settings()  # import settings

        # create a display window
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        # Create an instance to store game statistics and make scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        penguin_image = pygame.image.load("images/penguinrocket_image.bmp")
        self.penguin = Penguin(self, penguin_image)  # import ship

        self.rockets = pygame.sprite.Group()

        # Creating blank lists for rows and enemy positions
        self.enemies_positions = []
        self.rows = []

        self.enemies = pygame.sprite.Group()
        self._create_enemy_positions()

        # User defined events have available ID's between 24 to 32;
        # First 23 event slots (ID’s) used by Pygame;
        # Here, we use 23 + 0 -> 24th ID.
        self.spawn_event = pygame.USEREVENT + 0
        # we set the timer for this event
        pygame.time.set_timer(
            self.spawn_event, self.settings.enemy_spawn_interval
        )

        # create a clock for controling fps cap via pygame Clock class
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Rocket Penguin")
        self.save_path = Path("score_save/highest_score.txt")

        # Start Rocket Penguin in an active state
        self.game_active = False

        self.tutorial_screen = Tutorial(self)
        self.play_button = PlayButton(self, "Play")

        # self argument refers to the current instance of RocketPenguin
        # and so it gives access to the game's resources

    def _start_game(self):
        """Start the game by button press or mouse click"""
        # Reset the game statistics
        self.stats.reset_stats()
        self.game_active = True

        # Get rid of remaining rockets and enemies
        self.rockets.empty()
        self.enemies.empty()

        # Center the penguin
        self.penguin.center_penguin()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.game_active:  # runs when game is active
                self.penguin.update()
                self._update_rockets()
                self._update_enemies()

            self._update_screen()
            self.clock.tick(60)
            # print(len(self.rows)) # to test amount of rows is normal
            # print(len(self.enemies)) # to test if enemies spawn

    def _check_events(self):
        """Respond to keystrokes and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # when you closes the game's window
                self.save_path.write_text(str(self.stats.high_score))
                sys.exit()  # system call to kill process
            elif event.type == pygame.KEYDOWN:
                # Each keypress is registered as a KEYDOWN event.
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                # KEYUP event is used when the key is released
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # MOUSEBUTTONDOWN detects any click
                mouse_pos = pygame.mouse.get_pos()  # to get cursor position
                self._check_play_button(mouse_pos)
            elif event.type == self.spawn_event:
                # this event is special; it is executed by itself every
                # enemy spawn interval
                self._place_enemy()

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_DOWN:
            self.penguin.moving_bottom = True
        elif event.key == pygame.K_UP:
            self.penguin.moving_top = True
        elif event.key == pygame.K_q:  # when q is pressed, game process killed
            self.save_path.write_text(str(self.stats.high_score))
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_rocket()  # fire a rocket when SPACE is pressed

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_DOWN:
            self.penguin.moving_bottom = False
        elif event.key == pygame.K_UP:
            self.penguin.moving_top = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # will restart if button clicked and game's inactive
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_penguin_lives()
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _fire_rocket(self):
        """Create a new rocket and add it to the rockets group"""
        # check if new rockets can be fired
        if self.game_active:
            if len(self.rockets) < self.settings.rockets_allowed:
                new_rocket = Rocket(self)  # making an instance of rocket class
                self.rockets.add(new_rocket)

    def _update_rockets(self):
        """Update the position of rockets and get rid of old ones"""
        # Update rockets positions
        self.rockets.update()

        # Get rid of rockets that are off screen
        for rocket in self.rockets.copy():
            if rocket.rect.left >= self.settings.screen_width:
                # check if the left of rocket rect has the value of x = screen_width
                # if so, then delete rocket
                self.rockets.remove(rocket)
        # print(len(self.rockets)) - to see the number of rockets in console

        self._check_rocket_enemy_collisions()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_colour)
        self._draw_rows()

        # Draw the score info
        self.sb.show_score()

        for rocket in self.rockets.sprites():
            rocket.blitrocket()

        self.penguin.blitme()
        self.enemies.draw(self.screen)

        # Draw buttons if the game is inactive
        if not self.game_active:
            self.tutorial_screen.draw_tutorial()
            self.play_button.draw_button()

        pygame.display.flip()
        # flip() the display to put your work on screen

    def _draw_rows(self):
        """Draw black horizontal lines to make rows"""

        rows_step = 0
        for row in range(self.settings.number_of_rows):
            row = pygame.draw.line(
                self.screen,
                pygame.Color(0, 0, 0),
                [0, rows_step],  # row's start point
                [self.settings.screen_width, rows_step],  # end point
            )
            rows_step += self.settings.row_margin
            self.rows.append(row)

        # delete stacking rows to reduce cpu usage
        if len(self.rows) > 30:
            self.rows = []
            rows_step = 0
        else:
            pass

    def _check_rocket_enemy_collisions(self):
        """Respond to rocket-enemy collisions"""
        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.rockets, self.enemies, True, True
        )

        # check if the collision has occured
        #   if so, add points!
        if collisions:
            self.stats.score += self.settings.enemy_points
            self.settings.enemy_beaten += 1

            # update score
            self.sb.prep_score()
            self.sb.check_high_score()

        # Check if the new level was achieved
        self._new_level()
        """
        .groupcollide() compares each element from two groups: bullet’s rect
        with each alien’s rect and returns a dictionary with collided
        key -> bullet, and corresponding value -> alien pair.
        """

    def _new_level(self):
        """Moving to the next level"""
        if self.settings.enemy_beaten == self.settings.enemy_beaten_max:
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

            # Reset enemy beaten counter
            self.settings.enemy_beaten = 0

        # Stop the game if 10th level is achieved
        if self.stats.level == 10:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_enemies(self):
        """Move the alien; Check if it hit the edge; Look for collisions"""
        # .spritecollideany() function takes two arguments: sprite and group
        if pygame.sprite.spritecollideany(self.penguin, self.enemies):
            # print("penguin hit!")  # show result in console
            self._penguin_hit()

        # Look for enemies hitting the left edge of the screen.
        self._check_enemies_left_edge()

        # Update group's position
        self.enemies.update()

    def _penguin_hit(self):
        """Respond to the penguin being hit by an enemy"""
        if self.stats.penguin_lives_left > 0:
            # Decrement number of penguins left.
            self.stats.penguin_lives_left -= 1
            self.sb.prep_penguin_lives()

            # Get rid of any remaining rockets and enemies.
            self.rockets.empty()
            self.enemies.empty()

            self.penguin.center_penguin()
            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_enemies_left_edge(self):
        """Check if any enemies have reached the left edge of the screen"""
        for enemy in self.enemies.sprites():
            if enemy.rect.left <= 0:
                # Treat this the same if the penguin got hit
                self._penguin_hit()
                break  # break after one enemy hits the bottom

    def _create_enemy_positions(self):
        """Create positions off screen for placing enemies"""
        enemy = Enemy(self)  # dummy Enemy instance

        position_y_top, position_y_bottom = 0, self.settings.row_margin / 5
        position_x = self.settings.screen_width + enemy.rect.width

        for row in range(self.settings.number_of_rows):

            position_y = (position_y_top + position_y_bottom) / 2
            position_dict = [position_x, position_y]
            self.enemies_positions.append(position_dict)

            # Increase y top and bottom values
            position_y_bottom += self.settings.row_margin
            position_y_top += self.settings.row_margin

    def _place_enemy(self):
        """Place the enemy on the random location from the list"""
        random_x, random_y = random.choice(self.enemies_positions)
        self._create_enemy(random_x, random_y)  # input x and y position

    def _create_enemy(self, x_position, y_position):
        """Create an enemy and place it"""
        # x_position parameter to specify where enemy will be
        new_enemy = Enemy(self)
        new_enemy.x = x_position
        new_enemy.rect.x = x_position
        new_enemy.rect.y = y_position
        self.enemies.add(new_enemy)


"""Place run_game() in an if block that only runs if the file is called directly. """
if __name__ == "__main__":
    # Make a game instant and run the game
    rp_game = RocketPenguin()
    rp_game.run_game()

"""
Refactored code is here:
"""
