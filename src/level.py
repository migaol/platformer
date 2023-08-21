import pygame as pg
import load
from player import Player
from guibar import GuiBar
from tile import *
from enemy import *
from settings import *

class Level:
    def __init__(self, level_data, surface) -> None:
        self.display_surface = surface
        self.guibar = GuiBar(self.display_surface, 1)

        self.setup_level(level_data)
        self.view_shift = 0

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

    def player_horizontal_movement(self):
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
        
        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect):
                player.damage()
    
    def player_vertical_movement(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.velocity.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.velocity.y = 0
                    player.on_ground = True
                    player.jumps = PLAYER_MAX_JUMPS
                elif player.velocity.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.velocity.y = 0
                    player.on_ceiling = True
        
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

    def run(self):
        self.scroll_x()
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

        self.guibar.show_base()
        self.guibar.show_healthbar(self.player.sprite.health, self.player.sprite.max_health)