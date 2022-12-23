class GameStats:
    def __init__(self, ai_game):
        # initialize statistics
        self.settings = ai_game.settings
        self.ships_left = None
        self.score = None
        self.level = None
        self.reset_stats()

        # start game in an inactive state
        self.game_active = False

        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        # initialize statistics that can change during the game
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
