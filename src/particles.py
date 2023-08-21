import pygame as pg
from settings import *
import load

class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, type: str):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = DEFAULT_ANIMATION_SPEED
        if type == 'player_jumping':
            self.frames = load.import_tilesheet('./assets/player/jump_dust.png')
            self.frames = [pg.transform.flip(frame, False, True) for frame in self.frames]
            offset = pg.Vector2(0, TILE_SIZE // 4 * 3)
        elif type == 'player_landing':
            self.frames = load.import_tilesheet('./assets/player/jump_dust.png')
            offset = pg.Vector2(0, TILE_SIZE // 4)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (x, y) + offset)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, xshift):
        self.animate()
        self.rect.x += xshift