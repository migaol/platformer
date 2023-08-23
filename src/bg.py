import pygame as pg
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
        self.image = pg.image.load(png_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (SCREEN_WIDTH, height))
        self.rect = self.image.get_rect(topleft = (0, y))

class DynamicBackground(Background):
    def __init__(self, pos: pg.Vector2, height: int, parallax_factor: int, png_path: str):
        super().__init__(pos.y, height)
        self.image = pg.image.load(png_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (SCREEN_WIDTH, height))
        self.rect = self.image.get_rect(topleft = pos)
        self.parallax_factor = parallax_factor

    def update(self, player_movement: pg.Vector2):
        self.rect.x -= player_movement.x * self.parallax_factor
        if self.rect.right < 0:
            self.rect.left += 2*SCREEN_WIDTH
        elif self.rect.left >= SCREEN_WIDTH:
            self.rect.right -= 2*SCREEN_WIDTH

class ParallaxBackground(pg.sprite.Group):
    def __init__(self, pos: pg.Vector2, height: int, parallax_factor: int, png_path: str):
        primary = DynamicBackground(pos, height, parallax_factor, png_path)
        secondary = DynamicBackground(pos + pg.Vector2(primary.rect.width, 0), height, parallax_factor, png_path)
        super().__init__(primary, secondary)