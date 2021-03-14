import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initilize the alien sat its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        # load the alien image and set its rect attribute
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # start each new alien near the top left of the screen.
        self.rect.x = (
            self.rect.width
        )  # adding a space to the left of it that is equal to the alien's width
        self.rect.y = self.rect.height  # adding a space equal to the height above alien

        # store the aliens exact horizontal position
        self.x = float(self.rect.x)