import pygame as pg
from settings import *
import load

class Enemy(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, surface: pg.Surface):
        super().__init__()
        self.image = pg.image.load('./assets/test_direction.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        self.display_surface = surface

        self.velocity = pg.math.Vector2(ENEMY_DUMMY_SPEED, 0)
        self.gravity = PLAYER_GRAVITY
        self.terminal_velocity = PLAYER_TERMINAL_VELOCITY

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

class Zombie(Enemy):
    def __init__(self, x: int, y: int, surface: pg.Surface):
        super().__init__(x, y, surface)
        self.image = pg.image.load('./assets/test_direction.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        self.velocity.x = ENEMY_ZOMBIE_SPEED