class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initilize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # start game in an inactive state
        self.game_active = False
        # highscore should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initilize statistics that can change during the game."""
        self.ships_left = (
            self.settings.ship_limit
        )  # able to call reset_stats() any time the player starts a new game
        self.score = 0  # storing initial score in this method rather than __init__ so that the score resets with each new game
        self.level = 1