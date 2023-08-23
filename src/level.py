import pygame as pg
import numpy as np
import load
from gui import Gui
from player import Player
from particles import ParticleEffect
from tile import *
from bg import *
from enemy import *
from settings import *

class Level:
    def __init__(self, level_data, surface: pg.Surface, debug_mode: bool = False) -> None:
        self.display_surface = surface
        self.debug_mode = debug_mode

        self.setup_level(level_data)
        self.setup_background()
        self.view_shift = 0
        self.player_movement = pg.Vector2(0, 0)

        self.gui = Gui(self.display_surface, 1, self.player.sprite)

        self.global_animation_frame = 0
        self.particle_sprites = pg.sprite.Group()

    def setup_level(self, layout):
        self.tiles = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()
        self.enemies = pg.sprite.Group()
        for ri,r in enumerate(layout):
            for ci,c in enumerate(r):
                x, y = ci*TILE_SIZE, ri*TILE_SIZE
                if c == 'x':
                    self.tiles.add(BlankTile(x, y, TILE_SIZE, 'gray'))
                elif c == 'p':
                    self.player.add(Player(x, y, self.display_surface))
                elif c == 'z':
                    self.enemies.add(Zombie(x, y, self.display_surface))
                elif c == 's':
                    self.enemies.add(Zombie(x, y, self.display_surface))

    def setup_background(self):
        bg_files = load.import_background_files('./assets/background/1')
        composite_layers = []
        for layer_type in bg_files:
            bg_layers = bg_files[layer_type]
            if layer_type =='static':
                for layer_png in bg_layers:
                    composite_layers.append(StaticBackground(0, SCREEN_HEIGHT, layer_png))
            elif layer_type in ['background', 'midground','foreground']:
                parallax_factors = np.linspace(PARALLAX_FACTOR[layer_type]['min'], PARALLAX_FACTOR[layer_type]['max'], len(bg_layers))
                for i, layer_png in enumerate(bg_layers):
                    composite_layers.append(ParallaxBackground(pg.Vector2(0, 0), SCREEN_HEIGHT, parallax_factors[i], layer_png))
        
        self.background = pg.sprite.Group(*composite_layers)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.velocity.x

        if player_x < SCREEN_SCROLL_THRESHOLD and direction_x < 0:
            self.view_shift = -direction_x
            self.player_movement.x = -self.view_shift
        elif player_x > SCREEN_WIDTH - SCREEN_SCROLL_THRESHOLD and direction_x > 0:
            self.view_shift = -direction_x
            self.player_movement.x = -self.view_shift
        else:
            self.view_shift = 0

    def player_horizontal_movement(self):
        player = self.player.sprite
        # player_prev_x = player.velocity.x
        if self.view_shift == 0:
            player.rect.x += player.velocity.x

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.velocity.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.collision_point_x = player.rect.left
                elif player.velocity.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.collision_point_x = player.rect.right
        if player.on_left and (player.rect.left < self.collision_point_x or player.velocity.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.collision_point_x or player.velocity.x <= 0):
            player.on_right = False
        
        if (not player.on_left) and (not player.on_right):
            self.player_movement.x = player.velocity.x
        else:
            self.player_movement.x = 0
        
        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect) and player.animation_state != 'hurt':
                player.damage()
                self.gui.hp_bar.lose_hp(1)
    
    def player_vertical_movement(self):
        player_was_on_ground = self.player.sprite.on_ground
        player = self.player.sprite

        if player.velocity.y == player.jump_speed:
            self.create_jump_particles()
        
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.velocity.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.velocity.y = 0
                    player.on_ground = True
                    player.jump_cooldown = 0
                    player.jumps = PLAYER_MAX_JUMPS
                elif player.velocity.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.velocity.y = 0
                    player.on_ceiling = True
        
        if player.on_ground and player.velocity.y < 0 or player.velocity.y > player.gravity:
            player.on_ground = False
        if not player_was_on_ground and self.player.sprite.on_ground:
            player.land()
            self.create_player_landing_particles()
        
        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect):
                if player.velocity.y > 0:
                    player.rect.bottom = enemy.rect.top
                    player.jump()
                    player.jumps += 1
                    enemy.kill()

    def enemy_horizontal_movement(self):
        for enemy in self.enemies.sprites():
            enemy.move()
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.velocity.x < 0:
                        enemy.rect.left = sprite.rect.right
                    elif enemy.velocity.x > 0:
                        enemy.rect.right = sprite.rect.left
                    enemy.reverse()

    def enemy_vertical_movement(self):
        for enemy in self.enemies.sprites():
            enemy.apply_gravity()
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.velocity.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.velocity.y = 0
                        enemy.on_ground = True

    def create_jump_particles(self):
        x, y = self.player.sprite.rect.midbottom
        jump_particle = ParticleEffect(x, y, 'player_jumping')
        self.particle_sprites.add(jump_particle)

    def create_player_landing_particles(self):
        x, y = self.player.sprite.rect.midbottom
        landing_particle = ParticleEffect(x, y, 'player_landing')
        self.particle_sprites.add(landing_particle)

    def run(self):
        self.global_animation_frame += DEFAULT_ANIMATION_SPEED

        self.scroll_x()
        self.background.update(self.player_movement)
        self.background.draw(self.display_surface)

        self.tiles.update(self.view_shift)
        self.tiles.draw(self.display_surface)

        self.enemies.update(self.view_shift)
        self.enemy_horizontal_movement()
        self.enemy_vertical_movement()
        self.enemies.draw(self.display_surface)

        self.player.update()
        self.player_horizontal_movement()
        self.player_vertical_movement()
        self.player.draw(self.display_surface)
        if self.debug_mode:
            pg.draw.rect(self.display_surface, (0, 128, 255), self.player.sprite.rect, 2)

        self.particle_sprites.update(self.view_shift)
        self.particle_sprites.draw(self.display_surface)

        self.gui.draw()