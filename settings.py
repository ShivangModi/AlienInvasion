class Settings:
    def __init__(self):
        # Initialize the game's static settings
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)  # colors in Pygame are specified as RGB colors

        # ship settings
        self.ship_speed = None
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = None
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)    # dark grey color
        self.bullet_allowed = 3

        # alien settings
        self.alien_speed = None
        self.alien_points = None
        self.fleet_drop_speed = 10

        # fleet direction
        self.fleet_direction = None

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # initialize settings that change throughout the game
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 1.0

        # scoring
        self.alien_points = 50

        # fleet_direction of 1 represents right 1; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        # increase speed settings and alien point values
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
