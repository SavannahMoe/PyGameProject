import pygame


class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initilize the ship and its starting position."""
        self.screen = (
            ai_game.screen
        )  # assigning screen to an attribute of the ship for easy access in methods of class
        self.screen_rect = (
            ai_game.screen.get_rect()
        )  # accessing the screen's rect attribute allowing us to place the ship in thecorrect location on the screen

        # load the ship image and get its rect
        self.image = pygame.image.load(
            "images/ship.bmp"
        )  # returns a surface representing the ship that we assign to self.image
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen.
        self.rect.midbottom = (
            self.screen_rect.midbottom
        )  # uses the rect attributes to position the ship image so its centered and at the bottom of the screen

        # movemnet flag
        self.moving_right = (
            False  # moving right attribute added to __init__ and initially set to false
        )
        self.moving_left = False

    def update(self):
        """update the ship's position based on the movemnet flags."""
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)