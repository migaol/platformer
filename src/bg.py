import pygame as pg
from typing import List
import load
from tile import *
from settings import *

class Background(pg.sprite.Sprite):
    def __init__(self, y: int, height: int, color: str = 'black'):
        super().__init__()
        self.image = pg.Surface((SCREEN_WIDTH, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (0, y))

class StaticBackground(Background):
    def __init__(self, y: int, height: int, png_path: str):
        super().__init__(y, height)
        self.image = pg.image.load(png_path).convert()
        self.image = pg.transform.scale(self.image, (SCREEN_WIDTH, height))
        self.rect = self.image.get_rect(topleft = (0, y))

class DynamicBackground(Background):
    def __init__(self, pos: pg.Vector2, height: int, parallax_factor: int, png_path: str):
        super().__init__(pos.y, height)
        self.image = pg.image.load(png_path).convert()
        self.image = pg.transform.scale(self.image, (SCREEN_WIDTH, height))
        self.rect = self.image.get_rect(topleft = pos)
        self.parallax_factor = parallax_factor

    def update(self, player_movement: pg.Vector2):
        self.rect.x -= player_movement.x * self.parallax_factor
        if self.rect.right < 0:
            self.rect.left += 2*SCREEN_WIDTH
        elif self.rect.left >= SCREEN_WIDTH:
            self.rect.right -= 2*SCREEN_WIDTH

class TiledDynamicBackground(pg.sprite.Group):
    def __init__(self, topleft: pg.Vector2, layout: List[List[str]], folder_path: str):
        super().__init__()
        terrain_tiles = load.import_tilesheet(folder_path + 'map_tiles.png')
        for ri, r in enumerate(layout):
            for ci, c in enumerate(r):
                if c == '-1': continue
                pos = pg.Vector2(ci*TILE_SIZE, ri*TILE_SIZE) - topleft
                tile_img = terrain_tiles[int(c)]
                sprite = StaticBackgroundTile(pos, TILE_SIZE, tile_img)
                self.add(sprite)

class TiledDynamicPath(pg.sprite.Group):
    def __init__(self, topleft: pg.Vector2, layout: List[List[str]], path_wall: bool = False):
        super().__init__()
        if not path_wall: path_tiles = load.import_tilesheet('./assets/level/level_1/map_tiles.png')
        for ri, r in enumerate(layout):
            for ci, c in enumerate(r):
                if c == '-1': continue
                pos = pg.Vector2(ci*TILE_SIZE, ri*TILE_SIZE) - topleft
                tile_img = pg.image.load('./assets/level/entities/01_path.png') if path_wall else path_tiles[int(c)]
                sprite = StaticBackgroundTile(pos, TILE_SIZE, tile_img)
                self.add(sprite)

class ParallaxBackground(pg.sprite.Group):
    def __init__(self, pos: pg.Vector2, height: int, parallax_factor: int, png_path: str):
        primary = DynamicBackground(pos, height, parallax_factor, png_path)
        secondary = DynamicBackground(pos + pg.Vector2(primary.rect.width, 0), height, parallax_factor, png_path)
        super().__init__(primary, secondary)