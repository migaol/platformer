import pygame as pg
from settings import *
import load

class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, type: str) -> None:
        super().__init__()
        self.frame_index = 0
        self.animation_speed = DEFAULT_ANIMATION_SPEED
        match type:
            case 'player_jumping':
                self.frames = load.import_tilesheet('./assets/particles/player_jump_dust.png')
                self.frames = [pg.transform.flip(frame, False, True) for frame in self.frames]
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(midbottom = (x, y+TILE_SIZE*3//4))
            case 'player_landing':
                self.frames = load.import_tilesheet('./assets/particles/player_jump_dust.png')
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(midbottom = (x, y+TILE_SIZE//4))
            case 'gem_pickup':
                self.frames = load.import_tilesheet('./assets/particles/gem_pickup.png')
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(center = (x, y))

    def animate(self) -> None:
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, xshift) -> None:
        self.animate()
        self.rect.x += xshift