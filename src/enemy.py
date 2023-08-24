import pygame as pg
from settings import *
import load

class LethalHitbox:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x, self.y = x, y
        self.w, self.h = w, h

class Enemy(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, surface: pg.Surface):
        super().__init__()
        self.image = pg.image.load('./assets/test_direction.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        self.lethal_hitbox = LethalHitbox(0, self.rect.h//2, self.rect.w, self.rect.h//2)

        self.display_surface = surface

        self.velocity = pg.math.Vector2(ENEMY_DUMMY_SPEED, 0)
        self.gravity = PLAYER_GRAVITY
        self.terminal_velocity = PLAYER_TERMINAL_VELOCITY

    def set_lethal_hitbox(self, left: float, top: float, right: float, bottom: float):
        self.lethal_hitbox.x = left * self.rect.w
        self.lethal_hitbox.y = top * self.rect.h
        self.lethal_hitbox.w = self.rect.w - (left+right) * self.rect.w
        self.lethal_hitbox.h = self.rect.h - (bottom+top) * self.rect.h

    def collide_lethal_hitbox(self, rect: pg.Rect) -> bool:
        return rect.colliderect(
            self.rect.x + self.lethal_hitbox.x, self.rect.y + self.lethal_hitbox.y,
            self.lethal_hitbox.w, self.lethal_hitbox.h)

    def get_lethal_hitbox(self) -> pg.Rect:
        return pg.Rect(
            self.rect.x + self.lethal_hitbox.x, self.rect.y + self.lethal_hitbox.y,
            self.lethal_hitbox.w, self.lethal_hitbox.h)

    def apply_gravity(self):
        self.velocity.y += min(self.gravity, self.terminal_velocity)
        self.rect.y += self.velocity.y

    def move(self):
        self.rect.x += self.velocity.x

    def reverse(self):
        self.velocity.x *= -1
        self.image = pg.transform.flip(self.image, True, False)

    def update(self, view_shift: int):
        self.rect.x += view_shift

class BasicEnemy(Enemy):
    def __init__(self, x: int, y: int, surface: pg.Surface):
        super().__init__(x, y, surface)
        self.image = pg.image.load('./assets/test_direction.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        self.velocity.x = ENEMY_BASIC_SPEED