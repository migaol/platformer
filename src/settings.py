import pygame as pg
from enum import Enum, StrEnum

# render
VERTICAL_TILES = 14
TILE_SIZE = 64
class TileID(StrEnum):
    NONE = '-1'
    PLAYER = '0'
    DUMMY = '1'
    STAR = '2'
    GEM_RED = '3'
    GEM_BLUE = '4'
    GEM_GREEN = '5'
    POTION_HEALTH = '6'
    CRATE_CROSS = '7'
    CRATE_SQUARE = '8'
    CRATE_SLASH = '9'
class TileIDGroup(Enum):
    GEMS = [TileID.GEM_RED, TileID.GEM_BLUE, TileID.GEM_GREEN]
    POWERUPS = [TileID.POTION_HEALTH]

# font
FONT = "./assets/font/Pixellari.ttf"
FONTSIZE = TILE_SIZE*4//5

# window
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = TILE_SIZE * VERTICAL_TILES
SCREEN_SCROLL_THRESHOLD_HORIZONTAL = SCREEN_WIDTH // 4
SCREEN_SCROLL_THRESHOLD_VERTICAL = SCREEN_HEIGHT // 4

# debug
HITBOX_COLOR =          (0, 128, 255)
LETHAL_HITBOX_COLOR =   (255, 0, 0)

# animation
DEFAULT_ANIMATION_SPEED = 0.2
PARALLAX_FACTOR = {
    'background':   {'min': 0.1, 'max': 0.3},
    'midground':    {'min': 0.4, 'max': 0.6},
    'foreground':   {'min': 0.7, 'max': 0.9}
}

# controls
KEY_QUIT = pg.K_ESCAPE
KEY_SELECT = pg.K_SPACE
# controls - player
KEY_LEFT = pg.K_a
KEY_RIGHT = pg.K_d
KEY_JUMP = pg.K_SPACE
KEY_SPRINT = pg.K_w
KEY_SNEAK = pg.K_s
KEY_UP = pg.K_w
KEY_DOWN = pg.K_s

# player behavior
PLAYER_LIVES = 5
PLAYER_HEALTH = 5
PLAYER_MAX_HEALTH = 5
PLAYER_WALK_MULTIPLIER = 1
PLAYER_SNEAK_MULTIPLIER = 0.5
PLAYER_SPRINT_MULTIPLIER = 1.5
PLAYER_MAX_MOMENTUM = 6
PLAYER_INERTIA = PLAYER_MAX_MOMENTUM/10
PLAYER_JUMP_COOLDOWN = 12
PLAYER_MAX_JUMPS = 2
PLAYER_JUMP_SPEED = -21
PLAYER_GRAVITY = 0.75
PLAYER_TERMINAL_VELOCITY = 10
PLAYER_HITBOX = (48,48) # TODO: implement

# entity behavior
ENTITY_PICKUP_HITBOX = (TILE_SIZE//2, TILE_SIZE//2)

# enemy behavior
ENEMY_DUMMY_SPEED = 5
ENEMY_BASIC_SPEED = 2