import pygame as pg
from settings import *
import load
from entity import Hitbox

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, surface: pg.Surface) -> None:
        super().__init__()
        self.image = pg.image.load('./assets/test_direction.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.lethal_hitbox = Hitbox(0, self.rect.h//2, self.rect.w, self.rect.h//2)

        self.display_surface = surface

        self.velocity = pg.math.Vector2(ENEMY_DUMMY_SPEED, 0)
        self.gravity = PLAYER_GRAVITY
        self.terminal_velocity = PLAYER_TERMINAL_VELOCITY

    def set_lethal_hitbox(self, left: float, top: float, right: float, bottom: float) -> None:
        self.lethal_hitbox.x = left * self.rect.w
        self.lethal_hitbox.y = top * self.rect.h
        self.lethal_hitbox.w = self.rect.w - (left+right) * self.rect.w
        self.lethal_hitbox.h = self.rect.h - (bottom+top) * self.rect.h

    def collide_lethal_hitbox(self, other: pg.Rect) -> bool:
        return self.lethal_hitbox.collide_hitbox(self.rect, other)

    def update_gravity(self) -> None:
        self.velocity.y += min(self.gravity, self.terminal_velocity)
        self.rect.y += self.velocity.y

    def move(self) -> None:
        self.rect.x += self.velocity.x

    def reverse(self) -> None:
        self.velocity.x *= -1
        self.image = pg.transform.flip(self.image, True, False)

    def update(self, view_shift: int) -> None:
        self.rect.x += view_shift

class TestEnemy(Enemy):
    def __init__(self, pos: pg.Vector2, surface: pg.Surface) -> None:
        super().__init__(pos, surface)
        self.image = pg.image.load('./assets/test_direction.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.velocity.x = ENEMY_BASIC_SPEED