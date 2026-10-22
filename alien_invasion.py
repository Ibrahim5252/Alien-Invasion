import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button




class AlienInvasion:
    def __init__(self):
        """intialze game ,and create game resources."""
        pygame.init()

        # Load and play background music (looping forever)
        # pygame.mixer.music.load('E:\Alien-Invasion\songs\song.mp3')  # use your file name
        # pygame.mixer.music.play(-1)  # -1 means infinite loop

        self.clock = pygame.time.Clock()
        self.settings  = Settings()
        # set the background color.
        self.screen = pygame.display.set_mode((self.settings.screen_width ,self.settings.screen_height ))
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # start Alien Invasion is an inactive state.
        self.game_active = False

        # make the play button.
        self.play_button = Button(self , "PLAY")

        # create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
       
    def run_game(self):
        """start main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:   
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            # make the most recently drawn screen visible.
            pygame.display.flip()
            self.clock.tick(60)

    def _check_events(self):   
        # watch for keyboard and mouse events. 
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
           
    def _check_play_button(self , mouse_pos):
        """start new game when the player clicks play."""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.game_active = True

    def _check_keydown_events(self , event):
        """Responces to keypresses."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        # elif event.key == pygame.K_UP or event.key == pygame.K_w :
        #     self.ship.moving_up = True
        # elif event.key == pygame.K_DOWN or event.key ==pygame.K_s:
        #     self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        

    def _check_keyup_events(self , event):
        """Responces to key release."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
             self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        # elif event.key == pygame.K_UP or event.key == pygame.K_w:
        #     self.ship.moving_up = False
        # elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        #     self.ship.moving_down = False
        

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and get ride od old buletts."""
        # update bullet position.
        self.bullets.update()

        # get rid od bullets thst have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # check for any bullets that have hit aliens.
        # if so get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets , self.aliens  , True , True)
        

    def _create_fleet(self):
        """create the fleet of aliens."""
        """create an alien and keep adding aliens until there is no room left."""
        """spacing between aliens is one alien width and one alien height."""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_width , alien_height = alien.rect.size
        current_x , current_y = alien_width , alien_height
        while current_y <(self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x , current_y)
                current_x += 2 * alien_width
            # finished a row; reset x value, and increament y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self , x_position , y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """update the position of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        
        # look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        # look for alien hitting the bottom of the screen.
        self._check_alien_bottom()


    def _check_fleet_edges(self):
        """Respond appropriatley if any aliens have reached an edges."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ship_left > 0:
            # Decrement ship left.
            self.stats.ship_left -= 1

            # get rid of any remaining bullets and alien.
            self.bullets.empty()
            self.aliens.empty()

            # create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
           

    def _check_alien_bottom(self):
        """check if any alien have reched bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # treat this the same as if the ship got hit.
                self._ship_hit()
                break


    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

      

if __name__ == '__main__':
    # make a game instance , and run the game.
    ai = AlienInvasion()
    ai.run_game()
    
    