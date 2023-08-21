import pygame as pg
from settings import *
import load

class Player(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, surface: pg.Surface):
        super().__init__()
        self.image = pg.image.load('assets/test_direction.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        self.display_surface = surface

        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_MAX_HEALTH

        self.velocity = pg.math.Vector2(0, 0)
        self.speed_mode = PLAYER_WALK_MULTIPLIER
        self.max_momentum = PLAYER_MAX_MOMENTUM
        self.inertia = PLAYER_INERTIA
        self.jump_cooldown = 0
        self.jumps = PLAYER_MAX_JUMPS
        self.jump_speed = PLAYER_JUMP_SPEED
        self.gravity = PLAYER_GRAVITY
        self.terminal_velocity = PLAYER_TERMINAL_VELOCITY

        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def get_input(self):
        pressed = pg.key.get_pressed()
        if pressed[KEY_SPRINT]:
            self.speed_mode = PLAYER_SPRINT_MULTIPLIER
        elif pressed[KEY_SNEAK]:
            self.speed_mode = PLAYER_SNEAK_MULTIPLIER
        else:
            self.speed_mode = PLAYER_WALK_MULTIPLIER
        
        if pressed[KEY_RIGHT]:
            self.velocity.x = self.max_momentum * self.speed_mode
            self.facing_right = True
        elif pressed[KEY_LEFT]:
            self.velocity.x = -self.max_momentum * self.speed_mode
            self.facing_right = False
        else:
            if -self.inertia/2 <= self.velocity.x <= self.inertia/2:
                self.velocity.x = 0
            elif self.velocity.x > 0:
                self.velocity.x -= self.inertia
            elif self.velocity.x < 0:
                self.velocity.x += self.inertia

        if pressed[KEY_JUMP] and self.can_jump():
            self.jump()

    def apply_gravity(self):
        self.velocity.y += min(self.gravity, self.terminal_velocity)
        self.rect.y += self.velocity.y
        if self.jump_cooldown > -1:
            self.jump_cooldown -= 1

    def can_jump(self):
        return self.on_ground and self.jumps > 0 and self.jump_cooldown <= 0

    def jump(self):
        self.velocity.y = self.jump_speed
        self.jumps -= 1
        self.jump_cooldown = PLAYER_JUMP_COOLDOWN

    def damage(self):
        pass

    def update(self):
        self.get_input()