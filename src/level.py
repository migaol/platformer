import pygame as pg
import load
from player import Player
from tile import *
from settings import *

class Level:
    def __init__(self, level_data, surface) -> None:
        self.display_surface = surface

        self.setup_level(level_data)
        self.view_shift = 0

    def setup_level(self, layout):
        self.tiles = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()
        for ri,r in enumerate(layout):
            for ci,c in enumerate(r):
                x, y = ci*TILE_SIZE, ri*TILE_SIZE
                if c == 'x':
                    self.tiles.add(BlankTile(x, y, TILE_SIZE, 'gray'))
                elif c == 'P':
                    self.player.add(Player(x, y, self.display_surface))

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.velocity.x

        if player_x < SCREEN_SCROLL_THRESHOLD and direction_x < 0:
            self.view_shift = -direction_x
        elif player_x > SCREEN_WIDTH - SCREEN_SCROLL_THRESHOLD and direction_x > 0:
            self.view_shift = -direction_x
        else:
            self.view_shift = 0

    def horizontal_movement_collision(self):
        player = self.player.sprite
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
    
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.velocity.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.velocity.y = 0
                    player.on_ground = True
                    player.jumps = DEFAULT_PLAYER_MAX_JUMPS
                elif player.velocity.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.velocity.y = 0
                    player.on_ceiling = True

    def run(self):
        self.scroll_x()
        self.tiles.update(self.view_shift)
        self.tiles.draw(self.display_surface)

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)