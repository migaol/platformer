import pygame as pg
import numpy as np
from PIL import Image
import random
from typing import List, Tuple, Dict, Any
import load
from gui import Gui
from player import Player
from particles import ParticleEffect
from tile import *
from bg import *
from enemy import *
from settings import *
from leveldata import world_data

class Level:
    def __init__(self, current_level: Tuple[int, int], surface: pg.Surface, debug_mode: bool = False) -> None:
        random.seed(1)
        self.display_surface = surface
        self.debug_mode = debug_mode

        self._setup_background()
        self.view_shift = 0
        self.player_movement = pg.Vector2(0, 0)
        self.global_animation_frame = 0

        self.current_level = current_level
        current_world = self.current_level[0]-1
        current_stage = self.current_level[1]-1
        level_data = world_data[current_world]['levels'][current_stage]

        self._setup_entities(load.import_csv_layout(level_data['entities']))

        self.gui = Gui(self.display_surface, 1, self.player.sprite)

        self._setup_sprites(level_data)
        
    def _setup_sprites(self, level_data: Dict[str, Any]) -> None:
        self.particle_sprites = pg.sprite.Group()

        self.terrain_tiles = self._create_tile_group(
            load.import_csv_layout(level_data['terrain']), level_data['assets_path'], 'terrain')
        self.animated_z1 = self._create_tile_group(
            load.import_csv_layout(level_data['animated_z1']), level_data['assets_path'], 'animated_z1')
        self.static_z1 = self._create_tile_group(
            load.import_csv_layout(level_data['static_z1']), level_data['assets_path'],'static_z1')
        self.static_z2 = self._create_tile_group(
            load.import_csv_layout(level_data['static_z2']), level_data['assets_path'],'static_z2')

    def _create_tile_group(self, layout: List[List[str]], folder_path: str, type: str) -> pg.sprite.Group:
        sprite_group = pg.sprite.Group()
        terrain_tiles = load.import_tilesheet(folder_path + 'terrain.png')
        static_tiles, img_filenames = load.import_folder(folder_path + 'static')
        for ri, r in enumerate(layout):
            for ci, c in enumerate(r):
                if c == NULL_TILEID: continue
                pos = pg.Vector2(ci*TILE_SIZE, ri*TILE_SIZE)
                c = int(c)
                if type == 'terrain':
                    tile_img = terrain_tiles[c]
                    sprite = StaticSquareTile(pos, TILE_SIZE, tile_img)
                elif type.startswith('animated_'):
                    png_path, frame_width, frame_height = load.get_spritesheet(folder_path + 'animated', c)
                    animation_frames = load.import_tilesheet(png_path, frame_width, frame_height)
                    pos = pg.Vector2(ci*TILE_SIZE, (ri+1)*TILE_SIZE - frame_height)
                    sprite = AnimatedTile(pos, frame_width, frame_height, animation_frames)
                elif type.startswith('static_'):
                    image = Image.open(img_filenames[c])
                    image_width = image.width
                    image_height = image.height
                    pos = pg.Vector2(ci*TILE_SIZE, (ri+1)*TILE_SIZE - image_height)
                    sprite = StaticTile(pos, image_width, image_height, static_tiles[c])
                sprite_group.add(sprite)
        return sprite_group

    def _setup_entities(self, layout: List[List[str]]) -> None:
        self.player = pg.sprite.GroupSingle()
        self.enemies = pg.sprite.Group()
        for ri,r in enumerate(layout):
            for ci,c in enumerate(r):
                x, y = ci*TILE_SIZE, ri*TILE_SIZE
                if c == '0':
                    self.player.add(Player(pg.Vector2(x,y), self.display_surface))
                elif c == 'z':
                    enemy = TestEnemy(x, y, self.display_surface)
                    enemy.set_lethal_hitbox(0, 0, 0, 0)
                    self.enemies.add(enemy)

    def _setup_background(self) -> None:
        bg_files = load.import_background_files('./assets/level/level_1/background')
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

    def _animate_scroll_x(self) -> None:
        player: Player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.velocity.x

        if player_x < SCREEN_SCROLL_THRESHOLD_HORIZONTAL and direction_x < 0:
            self.view_shift = -direction_x
            self.player_movement.x = -self.view_shift
        elif player_x > SCREEN_WIDTH - SCREEN_SCROLL_THRESHOLD_HORIZONTAL and direction_x > 0:
            self.view_shift = -direction_x
            self.player_movement.x = -self.view_shift
        else:
            self.view_shift = 0

    def _update_player_horizontal_movement(self) -> None:
        player: Player = self.player.sprite
        if self.view_shift == 0:
            player.rect.x += player.velocity.x

        for sprite in self.terrain_tiles.sprites():
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
    
    def _update_player_vertical_movement(self) -> None:
        player_was_on_ground = self.player.sprite.on_ground
        player: Player = self.player.sprite

        if player.velocity.y == player.jump_speed:
            self._create_player_jump_particles()
        
        player.update_gravity()

        for sprite in self.terrain_tiles.sprites():
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
            player.jumps = min(PLAYER_MAX_JUMPS-1, player.jumps) # disable ground jump when airborne
        if not player_was_on_ground and self.player.sprite.on_ground:
            if player.animation_state != 'hurt':
                player.land()
            self._create_player_land_particles()

    def _update_player_enemy_collision(self) -> None:
        player: Player = self.player.sprite
        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect) and player.animation_state != 'hurt':
                if enemy.collide_lethal_hitbox(player.rect):
                    player.damage()
                    self.gui.hp_bar.lose_hp(1)
                else:
                    player.rect.bottom = enemy.rect.top
                    player.jump()
                    player.jumps += 1
                    enemy.kill()

    def _update_enemy_horizontal_movement(self) -> None:
        for enemy in self.enemies.sprites():
            enemy.move()
            for sprite in self.terrain_tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.velocity.x < 0:
                        enemy.rect.left = sprite.rect.right
                    elif enemy.velocity.x > 0:
                        enemy.rect.right = sprite.rect.left
                    enemy.reverse()

    def _update_enemy_vertical_movement(self) -> None:
        for enemy in self.enemies.sprites():
            enemy.apply_gravity()
            for sprite in self.terrain_tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.velocity.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.velocity.y = 0
                        enemy.on_ground = True

    def _create_player_jump_particles(self) -> None:
        x, y = self.player.sprite.rect.midbottom
        jump_particle = ParticleEffect(x, y, 'player_jumping')
        self.particle_sprites.add(jump_particle)

    def _create_player_land_particles(self) -> None:
        x, y = self.player.sprite.rect.midbottom
        landing_particle = ParticleEffect(x, y, 'player_landing')
        self.particle_sprites.add(landing_particle)

    def debug_draw_hitbox(self, hitbox: pg.Rect, type: str, stroke: int = 4) -> None:
        if type == 'hitbox':
            color = HITBOX_COLOR
        elif type == 'lethal':
            color = LETHAL_HITBOX_COLOR
        pg.draw.rect(self.display_surface, color, hitbox, stroke)

    def run(self) -> None:
        self.global_animation_frame += DEFAULT_ANIMATION_SPEED

        self._animate_scroll_x()
        bg_movement = pg.Vector2(-self.view_shift, 0)
        self.background.update(bg_movement)
        self.background.draw(self.display_surface)

        self.terrain_tiles.update(self.view_shift)
        self.terrain_tiles.draw(self.display_surface)

        self.animated_z1.update(self.view_shift, self.global_animation_frame)
        self.animated_z1.draw(self.display_surface)
        self.static_z1.update(self.view_shift)
        self.static_z1.draw(self.display_surface)
        self.static_z2.update(self.view_shift)
        self.static_z2.draw(self.display_surface)

        self.enemies.update(self.view_shift)
        self._update_enemy_horizontal_movement()
        self._update_enemy_vertical_movement()
        self.enemies.draw(self.display_surface)

        self.player.update()
        self._update_player_horizontal_movement()
        self._update_player_vertical_movement()
        self._update_player_enemy_collision()
        self.player.draw(self.display_surface)

        self.particle_sprites.update(self.view_shift)
        self.particle_sprites.draw(self.display_surface)

        self.gui.draw()

        if self.debug_mode:
            self.debug_draw_hitbox(self.player.sprite.rect, 'hitbox')
            for enemy in self.enemies.sprites():
                self.debug_draw_hitbox(enemy.rect, 'hitbox')
                self.debug_draw_hitbox(enemy.get_lethal_hitbox(), 'lethal')