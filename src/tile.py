import pygame as pg
import load
from settings import *
import random

class Tile(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, size: int):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, xshift):
        self.rect.x += xshift

class BlankTile(Tile):
    def __init__(self, x: int, y: int, size: int, color: str):
        super().__init__(x, y, size)
        self.image.fill(color)

class StaticTile(Tile):
    def __init__(self, x: int, y: int, size: int, surface: pg.Surface):
        super().__init__(x, y, size)
        self.image = surface