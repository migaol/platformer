import pygame as pg
import random
from typing import List
import load
from player import Player
from particles import ParticleEffect
from tile import *
from bg import *
from settings import *
from leveldata import world_data

class LevelMenu:
    def __init__(self, surface: pg.Surface, current_world: int, debug_mode: bool = False):
        self.display_surface = surface
        self.debug_mode = debug_mode

        self.current_world = current_world-1

        self.view_shift = pg.Vector2(0, 0)
        self.background = TiledDynamicBackground(
            pg.Vector2(0,0),
            load.import_csv_layout(world_data[self.current_world]['map']['terrain']),
            world_data[self.current_world]['map']['assets_path']
        )

        self.player = pg.sprite.GroupSingle()
        pos = pg.Vector2(2*TILE_SIZE, 2*TILE_SIZE)
        self.player.add(LevelMenuPlayer(pos, self.display_surface))

    def scroll_x(self):
        player = self.player.sprite
        position = pg.Vector2(player.rect.center)
        direction = player.direction

        if position.x < SCREEN_SCROLL_THRESHOLD_HORIZONTAL and direction.x < 0:
            self.view_shift.x = -direction.x
        elif position.x > SCREEN_WIDTH - SCREEN_SCROLL_THRESHOLD_HORIZONTAL and direction.x > 0:
            self.view_shift.x = -direction.x
        else:
            self.view_shift.x = 0
        if position.y < SCREEN_SCROLL_THRESHOLD_VERTICAL and direction.y < 0:
            self.view_shift.y = -direction.y
        elif position.y > SCREEN_HEIGHT - SCREEN_SCROLL_THRESHOLD_VERTICAL and direction.y > 0:
            self.view_shift.y = -direction.y
        else:
            self.view_shift.y = 0
        self.view_shift *= player.speed

    def run(self):
        self.scroll_x()
        self.background.update(self.view_shift)
        self.background.draw(self.display_surface)

        self.player.update(self.view_shift)
        self.player.draw(self.display_surface)

class LevelMenuPlayer(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, surface: pg.Surface):
        super().__init__()
        self.display_surface = surface

        self.load_player_assets()
        self.load_particle_assets()
        self.animation_state = 'idle'
        self.animation_frame = 0
        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pg.Vector2(0, 0)
        self.speed = PLAYER_MAX_MOMENTUM

        self.facing_right = True

    def load_player_assets(self):
        filepath = './assets/player/blue/'
        self.animations = {'idle': [], 'walk': []}
        for animation in self.animations.keys():
            self.animations[animation] = load.import_tilesheet(filepath + 'blue_' + animation + '.png')
    
    def load_particle_assets(self):
        self.particles_walk = load.import_tilesheet('./assets/player/walk_dust.png')

    def get_input(self):
        pressed = pg.key.get_pressed()
        
        if pressed[KEY_RIGHT]:
            self.direction.x, self.direction.y = 1, 0
            self.facing_right = True
        elif pressed[KEY_LEFT]:
            self.direction.x, self.direction.y = -1, 0
            self.facing_right = False
        if pressed[KEY_UP]:
            self.direction.x, self.direction.y = 0, -1
        elif pressed[KEY_DOWN]:
            self.direction.x, self.direction.y = 0, 1

    def animate(self):
        self.animation_frame += DEFAULT_ANIMATION_SPEED
        animation = self.animations[self.animation_state]
        animation_frame = int(self.animation_frame) % len(animation)
        
        image = animation[int(animation_frame)]
        self.image = image if self.facing_right else pg.transform.flip(image, True, False)

    def animate_particles(self):
        animation_frame = int(self.animation_frame) % len(self.particles_walk)
        particle = self.particles_walk[animation_frame]
        particle_rect = particle.get_rect()
        if self.facing_right:
            self.display_surface.blit(particle,
                                    self.rect.bottomleft - pg.Vector2(0, particle_rect.height))
        else:
            self.display_surface.blit(pg.transform.flip(particle, True, False),
                                    self.rect.bottomright - pg.Vector2(particle_rect.width, particle_rect.height))
    
    def update_animation_state(self):
        if self.direction.x != 0 or self.direction.y != 0:
            self.animation_state = 'walk'
        else:
            self.animation_state = 'idle'

    def move(self, view_shift: pg.Vector2):
        if view_shift.x == 0:
            self.rect.x += self.direction.x * self.speed
        if view_shift.y == 0:
            self.rect.y += self.direction.y * self.speed

    def update(self, view_shift: pg.Vector2):
        self.get_input()
        self.update_animation_state()
        self.animate_particles()
        self.animate()
        self.move(view_shift)