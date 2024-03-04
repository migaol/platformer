import pygame as pg
import numpy as np
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
        mapdata = world_data[self.current_world]['map']
        player_pos = pg.Vector2(SCREEN_WIDTH//2 - TILE_SIZE//2, SCREEN_HEIGHT//2 - TILE_SIZE//2)
        background_offset = np.where(np.array(load.import_csv_layout(mapdata['player'])) == PLAYER_INITIALPOS_TILEID)
        background_offset = pg.Vector2(background_offset[1][0]*TILE_SIZE, background_offset[0][0]*TILE_SIZE) - player_pos
        self.background = TiledDynamicBackground(background_offset, load.import_csv_layout(mapdata['terrain']), mapdata['assets_path'])

        path_array = load.import_csv_layout(mapdata['path'])
        path_wall_array = self.create_path_outline(path_array)
        self.path_wall = TiledDynamicPath(background_offset, path_wall_array, path_wall=True)
        self.path = TiledDynamicPath(background_offset, path_array)

        self.player = pg.sprite.GroupSingle()
        self.player.add(LevelMenuPlayer(player_pos, self.display_surface))

    def create_path_outline(self, path_array: List[List[str]]):
        height, width = len(path_array), len(path_array[0])
        new_path = np.full((width, height), NULL_TILEID)
        for ri, r in enumerate(path_array):
            for ci, c in enumerate(r):
                if c == NULL_TILEID: continue
                if ri > 0 and path_array[ri-1][ci] == NULL_TILEID:
                    new_path[ri-1][ci] = PATH_TILEID
                if ri < height and path_array[ri+1][ci] == NULL_TILEID:
                    new_path[ri+1][ci] = PATH_TILEID
                if ci > 0 and path_array[ri][ci-1] == NULL_TILEID:
                    new_path[ri][ci-1] = PATH_TILEID
                if ci < width and path_array[ri][ci+1] == NULL_TILEID:
                    new_path[ri][ci+1] = PATH_TILEID
        return new_path

    def scroll(self):
        player: LevelMenuPlayer = self.player.sprite
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
    
    def move_player(self):
        player: LevelMenuPlayer = self.player.sprite
        if self.view_shift.x == 0:
            player.rect.x += player.direction.x * player.speed
        if self.view_shift.y == 0:
            player.rect.y += player.direction.y * player.speed
        collision_x = collision_y = None

        for sprite in self.path_wall.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    player.direction.x = 0
                    collision_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    player.direction.x = 0
                    collision_x = player.rect.right
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.on_ground = True
                    player.direction.y = 0
                    collision_y = player.rect.bottom
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.on_ceiling = True
                    player.direction.y = 0
                    collision_y = player.rect.top
        if player.on_left and collision_x and (player.rect.left < collision_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and collision_x and (player.rect.right > collision_x or player.direction.x <= 0):
            player.on_right = False
        if player.on_ceiling and collision_y and (player.rect.top < collision_y or player.direction.y >= 0):
            player.on_ceiling = False
        if player.on_right and collision_y and (player.rect.right > collision_y or player.direction.y <= 0):
            player.on_right = False

    def run(self):
        self.scroll()
        self.background.update(self.view_shift)
        self.background.draw(self.display_surface)

        self.path.update(self.view_shift)
        self.path.draw(self.display_surface)
        self.path_wall.update(self.view_shift)
        if self.debug_mode: self.path_wall.draw(self.display_surface)

        self.player.update()
        self.move_player()
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
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

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
        if self.animation_state == 'walk':
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
        if self.direction.x == 0 and self.direction.y == 0:
            self.animation_state = 'idle'
        else:
            self.animation_state = 'walk'

    def update(self):
        self.get_input()
        self.update_animation_state()
        self.animate_particles()
        self.animate()