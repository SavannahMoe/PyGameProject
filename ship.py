import pygame


class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initilize the ship and its starting position."""
        self.screen = (
            ai_game.screen
        )  # assigning screen to an attribute of the ship for easy access in methods of class
        self.settings = ai_game.settings
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

        # store a decimal value for the ship's horixontal position.
        self.x = float(self.rect.x)  # attirbute can now store a decial value

        # movemnet flag
        self.moving_right = (
            False  # moving right attribute added to __init__ and initially set to false
        )
        self.moving_left = False

    def update(self):
        """update the ship's position based on the movemnet flags."""
        # update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect object from self.x
        self.rect.x = (
            self.x
        )  # usign self.x to update self.rect.x which controls the position of the ship

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)