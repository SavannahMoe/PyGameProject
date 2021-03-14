import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()  # initilizes the background setting that pygame needs to work properly
        self.settings = Settings()  # asign instance of settings to self.settings

        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN
        )  # tells pygame to figure out a window size taht will fill screen
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption(
            "Alien Invasion"
        )  # self.screen is a SUFRACE, each element can be returned by display.set_mode

        self.ship = Ship(
            self
        )  # make an instance of Ship after the screen had been created
        self.bullets = pygame.sprite.Group()  # storing bullets in a group

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
            self.bullets.update()
            self._update_screen()

            # redraw the screen during the pass thorugh the loop.

    def _check_events(self):  # make new check events method
        """Rspond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """respond to keypress"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # exit out of screen by pressing "q"
            sys.exit()
        elif event.key == pygame.K_SPACE:  # call  _fire_bullet whith the space bar
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """respond to keyreleases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """create a new bullet and add it to the bullets group."""
        if (
            len(self.bullets) < self.settings.bullets_allowed
        ):  # if the number of bullets still available to the player then....
            new_bullet = Bullet(self)  # make an instance of Bullet
            self.bullets.add(new_bullet)  # add it to the bullet group using add()

    def _update_bullets(self):
        self.bullets.update()  # storign bullets in a group

        # get rid oof bullets that have disappeared.
        for (
            bullet
        ) in (
            self.bullets.copy()
        ):  # copy() method in the for loop allows us to modify bullets inside the loop
            if (
                bullet.rect.bottom <= 0
            ):  # check to see if each bullet has moved off the screen
                self.bullets.remove(
                    bullet
                )  # remove the bullets if they are no longer on the screen

    def _update_screen(self):
        """update images on the screen, and flip to the new screen."""
        self.screen.fill(
            self.settings.bg_color
        )  # Fill method, acts on the surface and take one argument a color
        self.ship.blitme()  # after filling background, this draw ships to appear on top of back ground
        for (
            bullet
        ) in (
            self.bullets.sprites()
        ):  # sprite method returns a list of all sprites in the group bullets, loop through the sprites
            bullet.draw_bullet()  # and call draw_bullet on each one
        # make the most recently drawn screen visible.
        pygame.display.flip()  # tells pygame to make the most recently drawn screen visible, continually updates to show the
        # new positions of the game elements and hides the old ones


if __name__ == "__main__":
    # make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()