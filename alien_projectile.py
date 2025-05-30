import pygame
from pygame.sprite import Sprite


class AlienProjectile(Sprite):
    """A class to manage projectiles fired by the aliens"""

    def __init__(self, ai_game):
        """Create a projectile object and prepare the animation"""
        super().__init__()
        # super() allows us to inherit the parent module's instance,
        # which in our case is AlienInvasion's ai_game

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load projectile sheet and set the list for storing animation frames
        self.projectile_sheet = pygame.image.load("images/alien_projectile.bmp")
        self.animation_list = []

        # intialize frame update variables
        self.last_update = pygame.time.get_ticks()
        self.frame_num = 0

        self.get_animation()

        # center at the bottom of alien
        for alien in ai_game.aliens:
            self.rect.midtop = alien.rect.midbottom
        # this loop is also present in AlienInvasion class' _fire_projectile()
        # why it works this way: who knows?

        self.y = float(self.rect.y)
        # Store the projectile's position as a float

    def update(self):
        """Move the projectile up the screen"""
        # Update the exact position of the projectile
        self.y += self.settings.a_projectile_speed  # it will move vertically
        # Update the rect position
        self.rect.y = self.y

    def draw_projectile(self):
        """Draw the projectile to the screen"""
        # curren time increases as projectile moves through the screen
        current_time = pygame.time.get_ticks()

        # if the time between last update is greater the animation cooldown
        #   update animation frame
        if current_time - self.last_update >= self.settings.animation_cooldown:
            self.frame_num += 1
            self.last_update = current_time
            # reset frame if it's the last one
            if self.frame_num >= len(self.animation_list):
                self.frame_num = 0

        self.screen.blit(self.animation_list[self.frame_num], self.rect)

    def get_animation(self):
        """Create a list with animation frames"""

        # settings that depend on the source spread sheet dimensions
        frame_width = 4
        frame_height = 5
        animation_frames = 3

        for x in range(animation_frames):
            frame = self.get_frame_image(
                self.projectile_sheet, x, frame_width, frame_height
            )
            self.animation_list.append(frame)
            self.rect = frame.get_rect()

    def get_frame_image(self, sheet, frame, width, height):
        """Make a frame from sprite sheet"""
        scale = 3

        # Create surface with same dimensions as one frame
        # SRCALPHA means make background transparent
        image = pygame.Surface((width, height), pygame.SRCALPHA)

        # blit the sprite sheet on to the surface and
        # show only part of it defined by Area=((frame * width) ...)
        # so it will display a proper frame of animation
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))

        # scale it if needed
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image
