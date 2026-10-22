class GameStats:
    """Track Statics for Alien Invasion."""
    def __init__(self , ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
     
    def reset_stats(self):
        """Initialize statics that can change during the game."""
        self.ship_left = self.settings.ship_limit
        