import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_states import GameStats
from scoreboard import Scoreboard
from button import Button


class AlienInvasion:
    # Overall class to manage game assets and behavior
    def __init__(self):
        # Initialize the game, and create game resources
        pygame.init()
        self.settings = Settings()

        # self.screen is called a surface.
        # A surface in Pygame is a part of the screen where a game element can be displayed.
        # Each element in the game, like an alien or a ship, is its own surface.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # create an instance to store game statistics,
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.__create_fleet()

        # make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        # Start the main loop for the game
        while True:
            self.__check_events()
            if self.stats.game_active:
                self.ship.update()
                self.__update_bullets()
                self.__update_aliens()
            self.__update_screen()

    def __check_events(self):
        # An event is an action that user performs while playing the game, such as pressing,
        # a key or moving the mouse.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.__check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.__check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.__check_play_button(mouse_pos)

    def __check_play_button(self, mouse_pos):
        # start a new game when the player clicks play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset the game settings
            self.settings.initialize_dynamic_settings()

            # reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet and center the ship
            self.__create_fleet()
            self.ship.center_ship()

            # hide the moue cursor
            pygame.mouse.set_visible(False)

    def __check_keydown_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.__fire_bullet()

    def __check_keyup_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def __fire_bullet(self):
        # create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def __update_bullets(self):
        # update position of bullets and get rid of old bullets
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self.__check_bullet_alien_collisions()

    def __check_bullet_alien_collisions(self):
        # respond to bullet-alien collisions
        # remove any bullets and aliens that have collide
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.prep_high_score()

        if not self.aliens:
            # destroy existing bullets and create new fleet
            self.bullets.empty()
            self.__create_fleet()
            self.settings.increase_speed()

            # increase level
            self.stats.level += 1
            self.sb.prep_level()

    def __update_aliens(self):
        # check if the fleet is at an edge
        # update the positions of all aliens in the fleet
        self.__check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.__ship_hit()

        # look for aliens hitting the bottom of the screen
        self.__check_aliens_bottom()

    def __create_fleet(self):
        # create the fleet of aliens.
        # create an alien and find the number of aliens in row.
        # spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # create the first row of aliens
        for row_number in range(number_rows-2):
            for alien_number in range(number_aliens_x+1):
                self.__create_alien(alien_number, row_number)

    def __create_alien(self, alien_number, row_number):
        # create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_number)
        self.aliens.add(alien)

    def __check_fleet_edges(self):
        # respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.__check_fleet_direction()
                break

    def __check_fleet_direction(self):
        # drop the entire fleet if any aliens have reached an edge
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def __ship_hit(self):
        # respond to the ship being hit by an alien
        if self.stats.ships_left > 0:
            # decrement ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # get rid of any remaining aliens and bullets
            self.__create_fleet()
            self.ship.center_ship()

            # pause
            sleep(3)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def __check_aliens_bottom(self):
        # check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # treat this the same as if the ship got hit
                self.__ship_hit()
                break

    def __update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()

        # draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()
