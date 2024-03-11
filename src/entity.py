import pygame as pg
from typing import List
from settings import *
import load
from tile import *

class Hitbox:
    def __init__(self, x: int, y: int, w: int, h: int, alignment: str = 'topleft') -> None:
        if   alignment == 'topleft':    self.x, self.y = x, y
        elif alignment == 'center':     self.x, self.y = x+(TILE_SIZE-w)//2, y+(TILE_SIZE-h)//2
        self.w, self.h = w, h

    def collide_hitbox(self, base: pg.Rect, other: pg.Rect) -> bool:
        return other.colliderect(base.x + self.x, base.y + self.y, self.w, self.h)
    
    def get_hitbox(self, base: pg.Rect) -> pg.Rect:
        return pg.Rect(base.x + self.x, base.y + self.y, self.w, self.h)

class Gem(AnimatedTile):
    def __init__(self, pos: pg.Vector2, gem_id: str) -> None:
        if   gem_id == TileID.GEM_RED:      frames = load.import_tilesheet('assets/items/gem_red.png')
        elif gem_id == TileID.GEM_BLUE:     frames = load.import_tilesheet('assets/items/gem_blue.png')
        elif gem_id == TileID.GEM_GREEN:    frames = load.import_tilesheet('assets/items/gem_green.png')
        else: frames = []
        super().__init__(pos, frames)
        self.hitbox = Hitbox(0, 0, *ENTITY_PICKUP_HITBOX, alignment='center')
        self.id = gem_id

class Powerup(AnimatedTile):
    def __init__(self, pos: pg.Vector2, powerup_id: str) -> None:
        if   powerup_id == TileID.POTION_HEALTH:     frames = load.import_tilesheet('assets/items/potion_health.png')
        else: frames = []
        super().__init__(pos, frames)
        self.hitbox = Hitbox(0, 0, *ENTITY_PICKUP_HITBOX, alignment='center')
        self.id = powerup_id