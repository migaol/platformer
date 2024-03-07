import pygame as pg
from typing import List
from abc import ABC, abstractmethod
import random
from settings import *

class SquareTile(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, size: int) -> None:
        super().__init__()
        self.image = pg.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)

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

class Tile(pg.sprite.Sprite, ABC):
    def __init__(self) -> None:
        super().__init__()

    def update(self, xshift: int) -> None:
        self.rect.x += xshift

class StaticTile(Tile):
    def __init__(self, pos: pg.Vector2, image: pg.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

class AnimatedTile(Tile):
    def __init__(self, pos: pg.Vector2, animation_frames: List[pg.Surface]) -> None:
        super().__init__()
        self.animation_frames = animation_frames
        self.frame_offset = random.randint(0, len(self.animation_frames)-1)
        self.image = self.animation_frames[self.frame_offset]
        self.rect = self.image.get_rect(topleft=pos)

    def animate(self, global_animation_frame: float) -> None:
        animation_frame = (int(global_animation_frame) + self.frame_offset) % len(self.animation_frames)
        self.image = self.animation_frames[int(animation_frame)]

    def update(self, xshift: int, global_animation_frame: float) -> None:
        super().update(xshift)
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

class LevelPortalBackgroundTile(VariableStaticBackgroundTile):
    def __init__(self, pos: pg.Vector2, size: int, level: int,
                 surface_states: List[pg.Surface], initial_state: int = 0, font: str = FONT) -> None:
        super().__init__(pos, size, surface_states, initial_state)
        self.level = level
        self.font = pg.font.Font(font, TILE_SIZE//2)
        self.text = self.font.render(str(self.level), True, 'white')
        self.text_rect = self.text.get_rect(center=(TILE_SIZE//2, TILE_SIZE//2))

    def update(self, shift: pg.Vector2) -> None:
        super().update(shift)
        self.image.blit(self.text, self.text_rect)