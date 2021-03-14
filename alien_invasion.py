import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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
        # create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(
            self
        )  # make an instance of Ship after the screen had been created
        self.bullets = pygame.sprite.Group()  # storing bullets in a group

        self.aliens = pygame.sprite.Group()  # storing aliens in a group

        self._create_fleet()

        # make the Play Button
        self.play_button = Button(
            self, "Play"
        )  # creates an instance of the button but does not draw button to the screen

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
            self._check_events()  # even if game is inactive, still need to call _check_events

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()  # must continually update the screen, while waiting to see the player choose to start a new game

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(
            mouse_pos
        )  # button_clicked stores T/F
        if (
            button_clicked and not self.stats.game_active
        ):  # game will only restart in Play is clicked AND the game is not currently active
            # reset the game settings.
            self.settings.initialize_dynamic_settings()
            # reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()

            # get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # hide the mouse cursor.
            pygame.mouse.set_visible(False)

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
        self._check_bullet_aliens_collisions()

    def _check_bullet_aliens_collisions(self):
        """Respond to bullet-alien collisions."""
        # check for any bullets that have hit aliens.
        # if so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)  #
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:  # check is alien group is empty
            # destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """check if the fleet is at an edge"""
        self._check_fleet_edges()
        """Update the positions of all aliens in the fleet."""
        self.aliens.update()
        # look for alien-ship collisions.
        # spritecollideany() takes two arguments, a sprite and a group, in this case loops through the group aliens

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()  # calling _ship_hit when an alien hits a ship
        # look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

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
        # the following tests to be sure that the player has atleast one ship remaining, if they do not, game_active is set to false
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1  # number of ships left is reduced by 1
            # get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # pause
            sleep(0.5)  # so the play can see that they have been hit for half a second
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottome of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # treat this the same as if the ship got hit
                self._ship_hit()
                break

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
        # draw the score information
        self.sb.show_score()
        # draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        # make the most recently drawn screen visible.
        pygame.display.flip()  # tells pygame to make the most recently drawn screen visible, continually updates to show the
        # new positions of the game elements and hides the old ones


if __name__ == "__main__":
    # make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()