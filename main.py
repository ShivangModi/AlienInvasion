from alien_invasion import AlienInvasion

# In Alien Invasion, the player controls a rocket ship that appears at the bottom center
# of the screen. The player can move the ship left and right using the arrow keys and
# shoot bullets utilizing the space bar. When the game begins, a fleet of aliens fills
# the sky and moves across and down the screen. The player hits and destroys the aliens.
# If the player hits all the aliens, a new fleet appears that moves faster than the
# previous fleet. If any alien hits the player’s ship or reaches the bottom of the screen,
# the player loses a ship. If the player loses three ships, the game end.
if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
