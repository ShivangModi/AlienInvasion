import pygame
from pygame.sprite import Sprite


# Pygame is efficient because it lets you treat all game elements like rectangles,
# even if they’re not exactly shaped like rectangles. Treating an element as a
# rectangle is efficient because rectangles are simple geometric shapes. When Pygame
# needs to figure out whether two game elements have collided, for example, it can do
# this more quickly if it treats each object as a rectangle. This approach usually works
# well enough that no one playing the game will notice that we’re not working with the
# exact shape of each game element.
# In Pygame, the origin (0, 0) is in the top-left corner of the screen, and coordinates
# increase as you go down and to the right. On a 1200 by 800 screen, the origin is
# in the top-left corner, and the bottom-right corner has the coordinates (1200, 800).
# These coordinates refer to the game window, not the physical screen.


class Ship(Sprite):
    def __init__(self, ai_game):
        # initialize the ship and the set its starting position
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.screen_rect = ai_game.screen.get_rect()

        # load the ship image and get its rect
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()  # (x, y, w, h):- coordinates (x and y) and dimensions (w and h)

        # start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # moving flag
        self.moving_left = False
        self.moving_right = False

    def update(self):
        # update the ship's position based on the movement flag
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        # draw the ship at its current location
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
