import pygame as pg
import numpy as np
import random
from typing import List, Tuple
import load
from settings import *
from leveldata import world_data
from tile import *
from bg import *
from particles import EntityParticleEffect

class LevelMenu:
    def __init__(self, surface: pg.Surface, current_world: int, debug_mode: bool = False) -> None:
        self.display_surface = surface
        self.debug_mode = debug_mode

        self.current_world = current_world

        self.view_shift = pg.Vector2(0, 0)
        mapdata = world_data[self.current_world-1]['map']
        player_pos = pg.Vector2(SCREEN_WIDTH//2 - TILE_SIZE//2, SCREEN_HEIGHT//2 - TILE_SIZE//2)
        background_offset = np.where(np.array(load.import_csv_layout(mapdata['player'])) == '0')
        background_offset = pg.Vector2(background_offset[1][0]*TILE_SIZE, background_offset[0][0]*TILE_SIZE) - player_pos
        self.background = TiledDynamicBackground(background_offset, load.import_csv_layout(mapdata['terrain']), mapdata['assets_path'])

        path_array = load.import_csv_layout(mapdata['path'])
        path_wall_array = self._setup_path_outline(path_array)
        self.path_wall = TiledDynamicPath(background_offset, path_wall_array, path_wall=True)
        path_adjustment = (0,-12) # align with player sprite feet
        self.path = TiledDynamicPath(background_offset + path_adjustment, path_array)

        level_portals_array = load.import_csv_layout(mapdata['portal'])
        self.level_portals = LevelPortalsBackground(background_offset + path_adjustment, level_portals_array)

        self.player = pg.sprite.GroupSingle(LevelMenuPlayer(player_pos, self.display_surface))

    def _setup_path_outline(self, path_array: List[List[str]]) -> List[List[str]]:
        height, width = len(path_array), len(path_array[0])
        new_path = np.full((width, height), TileID.NONE)
        for ri, r in enumerate(path_array):
            for ci, c in enumerate(r):
                if c == TileID.NONE: continue
                if ri > 0 and path_array[ri-1][ci] == TileID.NONE:
                    new_path[ri-1][ci] = TileID.DUMMY
                if ri < height and path_array[ri+1][ci] == TileID.NONE:
                    new_path[ri+1][ci] = TileID.DUMMY
                if ci > 0 and path_array[ri][ci-1] == TileID.NONE:
                    new_path[ri][ci-1] = TileID.DUMMY
                if ci < width and path_array[ri][ci+1] == TileID.NONE:
                    new_path[ri][ci+1] = TileID.DUMMY
        return new_path

    def _animate_scroll(self) -> None:
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
    
    def _update_move_player(self) -> None:
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

    def get_player_pos(self) -> Tuple[int, int]:
        return self.player.sprite.rect.center
    
    def get_level(self) -> Tuple[int, int] | None:
        collided_levels: List[LevelPortalBackgroundTile] = pg.sprite.spritecollide(self.player.sprite, self.level_portals, False)
        if not collided_levels: return None
        return (self.current_world, collided_levels[0].level)

    def run(self) -> None:
        self._animate_scroll()
        self.background.update(self.view_shift)
        self.background.draw(self.display_surface)

        self.path.update(self.view_shift)
        self.path.draw(self.display_surface)
        self.path_wall.update(self.view_shift)
        if self.debug_mode: self.path_wall.draw(self.display_surface)

        self.level_portals.update(self.view_shift)
        self.level_portals.draw(self.display_surface)
        
        self.player.update()
        self._update_move_player()
        self.player.sprite.animate_particles()
        self.player.draw(self.display_surface)

class LevelMenuPlayer(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, surface: pg.Surface) -> None:
        super().__init__()
        self.display_surface = surface

        self._load_player_assets()
        self._load_particle_assets()
        self.animation_state = 'idle'
        self.animation_frame = 0
        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pg.Vector2(0, 0)
        self.speed = PLAYER_MAX_MOMENTUM

        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def _load_player_assets(self) -> None:
        filepath = './assets/player/blue/'
        self.animations = {'idle': [], 'walk': []}
        for animation in self.animations.keys():
            self.animations[animation] = load.import_tilesheet(filepath + 'blue_' + animation + '.png')
    
    def _load_particle_assets(self) -> None:
        self.particle_sprites = pg.sprite.Group()
        self.particle_sprites.add(EntityParticleEffect('player_running', persistent=True))

    def _get_input(self) -> None:
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

    def _animate(self) -> None:
        self.animation_frame += DEFAULT_ANIMATION_SPEED
        animation = self.animations[self.animation_state]
        animation_frame = int(self.animation_frame) % len(animation)
        
        image = animation[int(animation_frame)]
        self.image = image if self.facing_right else pg.transform.flip(image, True, False)

    def animate_particles(self) -> None:
        if self.animation_state == 'walk':
            self.particle_sprites.update(self.rect, reversed=(not self.facing_right))
            self.particle_sprites.draw(self.display_surface)
    
    def _update_animation_state(self) -> None:
        if self.direction.x == 0 and self.direction.y == 0: self.animation_state = 'idle'
        else:                                               self.animation_state = 'walk'

    def update(self) -> None:
        self._get_input()
        self._update_animation_state()
        self._animate()