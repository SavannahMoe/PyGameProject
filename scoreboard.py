import pygame.font


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings for scoreboard information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the initial score image.
        self.prep_score()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(
            self.stats.score, -1
        )  # tells pythonn so round the value to the nearest 10 and store in rounded_score
        score_str = "{:,}".format(
            rounded_score
        )  # tells python to insert commas to covert numerical value to a string
        # score_str = str(self.stats.score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20  # 20 pixels from the right
        self.score_rect.top = 20  # 20 pixels from the top

    def show_score(self):
        """draw sscore on the screen"""
        self.screen.blit(self.score_image, self.score_rect)