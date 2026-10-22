import pygame
from settings import Settings
"""A class to manage ship."""
class Ship:
    def __init__(self , ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # load the ship image and get its rect.
        self.image = pygame.image.load("/home/ibrahimk/work/Alien-Invasion/images/ship1.bmp")
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # store a float for the ships exact horizontal position.
        self.x = float(self.rect.x)

        # movement flag; start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on the movment flag."""
        if self.moving_right and self.rect.right < self.settings.screen_width:
            self.rect.x += self.settings.ship_speed
            
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed

        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.settings.ship_speed

        if self.moving_down and self.rect.bottom < self.settings.screen_height:
            self.rect.y += self.settings.ship_speed

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image , self.rect)

    def center_ship(self):
        """center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


