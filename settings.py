class Settings:
    """A class to store all setting for Alien Invasion"""

    def __init__(self):
        """Initializing the game settings."""
        # screen settings.
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # ship setting.
        self.ship_speed = 2
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 20
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        # alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 15
        # fleet_direction of 1 represent right , -1 represent left.
        self.fleet_direction = 1
