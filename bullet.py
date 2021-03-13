import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create a bullet rect at (0,0) and then set correct position.
        self.rect = pygame.Rect(
            0,
            0,
            self.settings.bullet_width,  # creates the bullet's rect attribute, built froms scratch
            self.settings.bullet_height,
        )
        self.rect.midtop = (
            ai_game.ship.rect.midtop
        )  # set midtop attribute to match the ship's midtop, making the bullet emerge from the top of the ship

        # store the bullet's position as a decimal value
        self.y = float(
            self.rect.y
        )  # store a decimal value for the bullets y-coordinates to make fine/small adjustments

    def update(self):
        """Move bullet up the screen"""
        self.y -= self.settings.bullet_speed
        # update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)