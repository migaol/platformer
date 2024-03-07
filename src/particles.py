import pygame as pg
from abc import ABC
from settings import *
import load

class ParticleEffect(pg.sprite.Sprite, ABC):
    def __init__(self, frame_index: int = 0, animation_speed: float = DEFAULT_ANIMATION_SPEED) -> None:
        super().__init__()
        self.frame_index = frame_index
        self.animation_speed = animation_speed
    
    def animate(self) -> None:
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): self.kill()
        else: self.image = self.frames[int(self.frame_index)]
    
    def update(self, xshift: int) -> None:
        self.animate()
        self.rect.x += xshift

class FreeParticleEffect(ParticleEffect):
    def __init__(self, rect: pg.Rect, type: str, **kwargs) -> None:
        super().__init__(**kwargs)
        match type:
            case 'player_jumping':
                self.frames = load.import_tilesheet('./assets/particles/player_jump_dust.png')
                self.frames = [pg.transform.flip(frame, False, True) for frame in self.frames]
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(midbottom = rect.midbottom + pg.Vector2(0, TILE_SIZE*3//4))
            case 'player_landing':
                self.frames = load.import_tilesheet('./assets/particles/player_jump_dust.png')
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(midbottom = rect.midbottom + pg.Vector2(0, TILE_SIZE//4))
            case 'gem_pickup':
                self.frames = load.import_tilesheet('./assets/particles/gem_pickup.png')
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(center = rect.center)

class EntityParticleEffect(ParticleEffect):
    def __init__(self, type: str, persistent: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.persistent = persistent
        self.rect = None
        match type:
            case 'player_running':
                self.frames = load.import_tilesheet('./assets/particles/player_walk_dust.png')
                self.image = self.frames[self.frame_index]

    def animate(self) -> None:
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            if self.persistent: self.frame_index = 0
            else:
                self.kill()
                return
        self.image = self.frames[int(self.frame_index)]
        
    def update(self, rect: pg.Rect, reversed: bool = False) -> None:
        self.animate()
        if reversed: self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(midbottom = rect.midbottom)