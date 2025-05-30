"""Import all required modules"""

import random
import sys
from pathlib import Path
from time import sleep

import pygame

from alien import Alien
from alien_projectile import AlienProjectile
from bullet import Bullet
from button import DifficultyButton, PlayButton
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overal class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create game resources."""
        pygame.init()
        self.settings = Settings()  # import settings

        # create a display window
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        """
        When creating the screen surface, we pass a size of (0, 0) and the
        parameter pygame.FULLSCREEN. This tells Pygame to figure out a window
        size that will fill the screen. 
        """
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        """
        Use the width and height attributes of the screen’s rect to update
        the settings object.
        """

        # Create an instance to store game statistics and make scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        ship_image = pygame.image.load("images/ship_nightraider_small.bmp")
        self.ship = Ship(self, ship_image)  # import ship

        self.bullets = pygame.sprite.Group()
        # Group of fired bullets will be an instance of the pygame Group class,
        # which behaves like a list with some extra functionality for games, that
        # will draw bullets on each pass through main loop and update each position.

        self.aliens = pygame.sprite.Group()  # group of aliens
        self._create_fleet()

        # two groups for projectiles functionality
        self.a_projectiles = pygame.sprite.Group()
        self.alien_last_row = pygame.sprite.Group()

        # event for spawning and firing projectiles
        self.spawn_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.spawn_event, self.settings.fire_interval)

        # create a clock for controling fps cap via pygame Clock class
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Alien Invasion")
        self.save_path = Path("score_save/highest_score.txt")

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # Create needed buttons
        self.dif_buttons = pygame.sprite.Group()
        self._create_difficulty_buttons()
        self.play_button = PlayButton(self, "Play")

        # self argument refers to the current instance of AlienInvasion
        # and so it gives access to the game's resources

    def _start_game(self):
        """Start the game by button press or mouse click"""
        # Reset the game statistics
        self.stats.reset_stats()
        self.game_active = True

        # Get rid of remaining bullets and aliens
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.game_active:  # runs when game is active
                self.ship.update()
                self._update_bullets()
                self._update_projectiles()
                self._update_aliens()

            self._update_screen()
            # tick() method takes one argument: the frame rate for the game.
            # Ideally, games should run at the same speed, or frame rate, on all systems.
            self.clock.tick(60)

    def _create_difficulty_buttons(self):
        """Create the difficulty buttons and add to group"""
        # input parameters are: self, message, x position, y position
        easy_dif = DifficultyButton(self, "Easy Mode", 944, 235)
        hard_dif = DifficultyButton(self, "Hard Mode", 944, 375)
        ext_dif = DifficultyButton(self, "Extreme Mode", 944, 515)
        self.dif_buttons.add(easy_dif, hard_dif, ext_dif)

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Make an alien and keep adding aliens until the screen is full
        # Spacing between aliens is one alien width and height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # defined from the image's width and height
        current_x, current_y = alien_width, alien_height

        # list to store y positions of aliens; used in _fire_projectile()
        self.y_positions = []

        # keep adding while there are enough room for new alien
        while current_y < (self.settings.screen_height - 4 * alien_height):
            # append y positions
            self.y_positions.append(current_y)

            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width  # make a step right
            # finished a row; reset x value, and increment y value
            current_x = alien_width  # reset x value
            current_y += 2 * alien_height  # make a step down

        # print(self.y_positions) # - for testing

    def _create_alien(self, x_position, y_position):
        # x_position parameter to specify where alien will be
        """create an alien and place it in the fleet"""
        new_alien = Alien(self)
        new_alien.x = x_position
        # new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

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
                for b in self.dif_buttons:
                    b.check_click(mouse_pos)
            elif event.type == self.spawn_event:
                # this event is special; it is executed by itself every
                # projectile spawn interval
                if self.game_active:
                    self._fire_projectile()
            # print(len(self.a_projectiles)) # - for testing

        # Whenever the key is pressed, that keypress is registered in Pygame as
        # an event. Each event is picked up by the pygame.event.get() method.

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_l:
            self.ship.moving_right = True
        elif event.key == pygame.K_h:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # when q is pressed, game process killed
            self.save_path.write_text(str(self.stats.high_score))
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # fire a bullet when SPACE is pressed

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_l:
            self.ship.moving_right = False
        elif event.key == pygame.K_h:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # will restart if button clicked and game's inactive
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship_lives()
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )  # True arguments tell pygame to delete collided elements

        # check if the collisions dictionary exists
        #   if so, add points!
        if collisions:
            # bullet is a key, aliens, that were hit with it - list of values
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                # multiply single score point by number of aliens it hit
            self.sb.prep_score()
            self.sb.check_high_score()

        # Check if the aliens group is empty after .groupcollide()
        self._new_level()
        """
        .groupcollide() compares each element from two groups: bullet’s rect
        with each alien’s rect and returns a dictionary with collided
        key -> bullet, and corresponding value -> alien pair.
        """

    def _new_level(self):
        """Moving to the next level"""
        if not self.aliens:
            # Destroy existing bullets, projectiles and create new fleet
            self.bullets.empty()
            self.a_projectiles.empty()

            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _check_aleins_edges_bottom(self):
        """Respond appropriately if any alien has reached and edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():  # if the value is True
                self._change_fleet_direction()
                break
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same if the ship got hit
                self._ship_hit()
                break  # break after one alien hits the bottom

    def _check_aliens_row(self):
        """Check if the last row should be nominaly changed"""
        # add the aliens from the last row to a seperate group
        for alien in self.aliens:
            if alien.rect.y >= max(self.y_positions):
                self.alien_last_row.add(alien)

        # remove the empty row y coordinate from the list
        if len(self.alien_last_row) == 0:
            del self.y_positions[-1]
            # print(self.y_positions) # - for testing

    def _check_projectile_ship_collisions(self):
        """Respond to projectile-ship collisions"""
        # Check for any projectile that have hit ship.
        #   If so, get call _ship_hit() function
        for projectile in self.a_projectiles:
            collisions = pygame.sprite.collide_rect(projectile, self.ship)

            if collisions:
                self._ship_hit()

    def _change_fleet_direction(self):
        """Drop the entire fleet and change fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        # if the fleet have dropped, update alien's y positions in a list
        for y in range(len(self.y_positions)):
            self.y_positions[y] += self.settings.fleet_drop_speed

        # Change direction by multiplying on -1
        self.settings.fleet_direction *= -1

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        # check if new bullets can be fired
        if self.game_active:
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self)  # making an instance of Bullet class
                self.bullets.add(new_bullet)
                # add() method is like append(), but specific to Pygame groups

    def _fire_projectile(self):
        """Create new projectile and add it to random alien"""
        # Checking if any aliens in last row is present
        self._check_aliens_row()
        # print(len(self.alien_last_row))  # - for testing

        # Try block is made for handling error from the period of time
        # when self.alien_last_row is empty,
        try:
            # pick random alien from the last row
            random_alien = random.choice(self.alien_last_row.sprites())

            for alien in self.aliens:

                # add only if the alien is present at last row
                if alien.rect.y >= max(self.y_positions):
                    new_projectile = AlienProjectile(self)
                    new_projectile.rect.midtop = random_alien.rect.midbottom
                    self.a_projectiles.add(new_projectile)

        # if so, the projectile is not fired
        except IndexError:
            pass

    def _update_bullets(self):
        """Update the position of bullets and get rid of old ones"""
        # Update bullets positions
        self.bullets.update()
        # Get rid of bullets that are off screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                # check if the bottom of bullet rect has the value of x = 0
                # if so, then delete bullet
                self.bullets.remove(bullet)
        # print(len(self.bullets)) - to see the number of bullets in console

        self._check_bullet_alien_collisions()

        """
        When using a for loop with a list (or a group in Pygame), Python
        expects list to stay the same length as long as the loop is running,
        so we have to loop over a copy of the group, using copy() method.
        """

    def _update_projectiles(self):
        """Update the position of projectiles and get rid of old ones"""
        # Update projectiles positions
        self.a_projectiles.update()

        # Get rid of projectiles that are off screen
        for projectile in self.a_projectiles.copy():
            if projectile.rect.bottom >= self.settings.screen_height:
                # if projectile is under bottom of the screen, delete it
                self.a_projectiles.remove(projectile)
        # print(len(self.bullets)) # - to see the number of bullets in console

        self._check_projectile_ship_collisions()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self._check_aleins_edges_bottom()
        self.aliens.update()  # update group's position

        # Look for alien-ship collisions
        # .spritecollideany() function takes two arguments: sprite and group
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship hit!")  # show result in console
            self._ship_hit()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ship_lives_left > 0:
            # Decrement ships left.
            self.stats.ship_lives_left -= 1
            self.sb.prep_ship_lives()

            # Get rid of any remaining bullets and projectiles.
            self.bullets.empty()
            self.a_projectiles.empty()

            # Empty aliens and last_row groups
            self.aliens.empty()
            self.alien_last_row.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False  # stop if ship_left = 0
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_colour)

        # Draw bullets and projectiles
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for projectile in self.a_projectiles.sprites():
            projectile.draw_projectile()

        self.ship.blitme()  # draw a ship
        self.aliens.draw(self.screen)  # draw aliens

        # Draw the score info
        self.sb.show_score()

        # Draw buttons if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

            # difficulty buttons are seperate cause they are sprites
            self.dif_buttons.draw(self.screen)
            for b in self.dif_buttons:
                b.draw_msg_and_outline()

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

# (To make a high-powered bullet that can travel to the top of the screen, destroying every
# alien in its path, you could set the first Boolean argument to False and keep the second
# Boolean argument set to True in .groupcollide() function. The aliens hit would disappear,
# but all bullets would stay active until they disappeared off the top of the screen.)
