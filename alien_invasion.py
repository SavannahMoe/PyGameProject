import sys

import pygame

from settings import Settings

from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()  # initilizes the background setting that pygame needs to work properly
        self.settings = Settings()  # asign instance of settings to self.settings

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )  # creates display window and uses tuple define deminsions
        pygame.display.set_caption(
            "Alien Invasion"
        )  # self.screen is a SUFRACE, each element can be returned by display.set_mode

        self.ship = Ship(
            self
        )  # make an instance of Ship after the screen had been created

        # set the background color.
        self.bg_color = (
            230,
            230,
            230,
        )  # light grey = background equal amounts (red, green, blue)

    def run_game(self):
        """Start the main loop for the game."""
        while (
            True
        ):  # while loop that runs continually and includes event loop (for loop)
            # watche for keyboard and mouse events. #EVENT: an action that the user performs while playing the game ( pressing key or moving the mouse)
            self._check_events()
            self.ship.update()
            self._update_screen()

            # redraw the screen during the pass thorugh the loop.
            

    def _check_events(self):  # make new check events method
        """Rspond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                    

    def _update_screen(self):
        """update images on the screen, and flip to the new screen."""
            self.screen.fill(
                self.settings.bg_color
            )  # Fill method, acts on the surface and take one argument a color
            self.ship.blitme()  # after filling background, this draw ships to appear on top of back ground

            # make the most recently drawn screen visible.
            pygame.display.flip()  # tells pygame to make the most recently drawn screen visible, continually updates to show the
            # new positions of the game elements and hides the old ones

if __name__ == "__main__":
    # make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()