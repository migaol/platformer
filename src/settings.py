import pygame as pg

# render
VERTICAL_TILES = 14
TILE_SIZE = 64

# window
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = TILE_SIZE * VERTICAL_TILES
SCREEN_SCROLL_THRESHOLD = SCREEN_WIDTH // 4

# debug
HITBOX_COLOR = (0, 128, 255)
LETHAL_HITBOX_COLOR = (255, 0, 0)

# animation
DEFAULT_ANIMATION_SPEED = 0.2
PARALLAX_FACTOR = {
    'background': {
        'min': 0.1, 'max': 0.3},
    'midground': {
        'min': 0.4,'max': 0.6},
    'foreground': {
        'min': 0.7,'max': 0.9}
}

# controls
KEY_QUIT = pg.K_ESCAPE
KEY_LEFT = pg.K_a
KEY_RIGHT = pg.K_d
KEY_JUMP = pg.K_SPACE
KEY_SPRINT = pg.K_w
KEY_SNEAK = pg.K_s

# player behavior
PLAYER_HEALTH = 5
PLAYER_MAX_HEALTH = 5
PLAYER_WALK_MULTIPLIER = 1
PLAYER_SNEAK_MULTIPLIER = 0.5
PLAYER_SPRINT_MULTIPLIER = 1.5
PLAYER_MAX_MOMENTUM = 8
PLAYER_INERTIA = PLAYER_MAX_MOMENTUM/10
PLAYER_JUMP_COOLDOWN = 12
PLAYER_MAX_JUMPS = 2
PLAYER_JUMP_SPEED = -20
PLAYER_GRAVITY = 0.75
PLAYER_TERMINAL_VELOCITY = 10

# enemy behavior
ENEMY_DUMMY_SPEED = 5
ENEMY_BASIC_SPEED = 2