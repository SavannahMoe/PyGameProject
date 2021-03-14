class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initilize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initilize statistics that can change during the game."""
        self.ship_left = (
            self.settings.ship_limit
        )  # able to call reset_stats() any time the player starts a new game
