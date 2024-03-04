import pygame as pg
from typing import List
import load
from settings import *
import random

class SquareTile(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, size: int) -> None:
        super().__init__()
        self.image = pg.Surface((size, size))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, xshift: int) -> None:
        self.rect.x += xshift

class BlankSquareTile(SquareTile):
    def __init__(self, pos: pg.Vector2, size: int, color: str) -> None:
        super().__init__(pos, size)
        self.image.fill(color)
        self.image = pg.image.load('./assets/test_direction.png')

class StaticSquareTile(SquareTile):
    def __init__(self, pos: pg.Vector2, size: int, surface: pg.Surface) -> None:
        super().__init__(pos, size)
        self.image = surface

class Tile(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, width: int, height: int) -> None:
        super().__init__()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, xshift: int) -> None:
        self.rect.x += xshift

class StaticTile(Tile):
    def __init__(self, pos: pg.Vector2, width: int, height: int, image: pg.Surface) -> None:
        super().__init__(pos, width, height)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, xshift: int) -> None:
        self.rect.x += xshift

class AnimatedTile(Tile):
    def __init__(self, pos: pg.Vector2, width: int, height: int, animation_frames: List[pg.Surface]) -> None:
        super().__init__(pos, width, height)
        self.animation_frames = animation_frames
        self.frame_offset = random.randint(0, len(self.animation_frames)-1)
        self.image = self.animation_frames[self.frame_offset]
        self.rect = self.image.get_rect(topleft = pos)

    def animate(self, global_animation_frame: float) -> None:
        animation_frame = (int(global_animation_frame) + self.frame_offset) % len(self.animation_frames)
        self.image = self.animation_frames[int(animation_frame)]

    def update(self, xshift: int, global_animation_frame: float) -> None:
        self.rect.x += xshift
        self.animate(global_animation_frame)

class StaticBackgroundTile(SquareTile):
    def __init__(self, pos: pg.Vector2, size: int, surface: pg.Surface) -> None:
        super().__init__(pos, size)
        self.image = surface

    def update(self, shift: pg.Vector2) -> None:
        self.rect.x += shift.x
        self.rect.y += shift.y

class VariableStaticBackgroundTile(StaticBackgroundTile):
    def __init__(self, pos: pg.Vector2, size: int, surface_states: List[pg.Surface], initial_state: int = 0) -> None:
        super().__init__(pos, size, surface_states[initial_state])
        self.surface_states = surface_states
        self.state = initial_state

    def set_state(self, state: int) -> None:
        self.state = state
        self.image = self.surface_states[state]