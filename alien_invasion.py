import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


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
        # create an instance to store game statistics
        self.stats = GameStats(self)

        self.ship = Ship(
            self
        )  # make an instance of Ship after the screen had been created
        self.bullets = pygame.sprite.Group()  # storing bullets in a group

        self.aliens = pygame.sprite.Group()  # storing aliens in a group

        self._create_fleet()

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
            self._update_bullets()
            self._update_aliens()
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
        if len(self.bullets) < self.settings.bullets_allowed:
            # if the number of bullets still available to the player then....
            new_bullet = Bullet(self)  # make an instance of Bullet
            self.bullets.add(new_bullet)  # add it to the bullet group using add()

    def _update_bullets(self):
        # update bullet position
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
        self._check_bullet_aliens_collision()

    def _check_bullet_aliens_collision(self):
        """Respond to bullet-alien collisions."""
        # check for any bullets that have hit aliens.
        # if so, get rid of the bullet and the alien.
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:  # check is alien group is empty
            # destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """check if the fleet is at an edge"""
        self._check_fleet_edges()
        """Update the positions of all aliens in the fleet."""
        self.aliens.update()
        # look for alien-ship collisions.
        # spritecollideany() takes two arguments, a sprite and a group, in this case loops through the group aliens

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()  # calling _ship_hit when an alien hits a ship

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # creating an alien and find the number of aliens in a row
        # spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = available_space_y // (2 * alien_height)

        # create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for (
            alien
        ) in (
            self.aliens.sprites()
        ):  # loop thorugh alien and call check_edges on each alien
            if alien.check_edges():
                self._change_fleet_direction()  # if check_edges returns true, the fleet changes direction
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += (
                self.settings.fleet_drop_speed
            )  # loop through all aliens, a drop each one using the fleet_drop _speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Decrement ships_left.
        self.stats.ship_left -= 1  # number of ships left is reduced by 1
        # get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        # create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()
        # pause
        sleep(0.5)  # so the play can see that they have been hit for half a second

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
        self.aliens.draw(self.screen)
        # make the most recently drawn screen visible.
        pygame.display.flip()  # tells pygame to make the most recently drawn screen visible, continually updates to show the
        # new positions of the game elements and hides the old ones


if __name__ == "__main__":
    # make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()