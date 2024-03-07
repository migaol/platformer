import pygame as pg
import numpy as np
from settings import *
import load
from player import Player

class Gui:
    def __init__(self, surface: pg.Surface, level: int, player: Player) -> None:
        self.display_surface = surface
        self.level = level

        self.left_bar = pg.image.load('./assets/gui/board_left.png').convert_alpha()
        # self.right_bar = pg.image.load('./assets/gui/guibar_right.png').convert_alpha()

        self.hp_bar = HealthBar(
            pos=pg.Vector2(TILE_SIZE//4, self.left_bar.get_height() + TILE_SIZE//4),
            display_surface=self.display_surface,
            player=player
        )

    def draw(self) -> None:
        self.display_surface.blit(self.left_bar, (0, 0))
        # self.display_surface.blit(self.right_bar, (SCREEN_WIDTH-self.right_bar.get_width(), 0))
        
        self.hp_bar.draw()

class HealthBar:
    def __init__(self, pos: pg.Vector2, display_surface: pg.Surface, player: Player) -> None:
        self.display_surface = display_surface
        self.player = player
        
        self.base = AttributeBar.BarBase(pos.copy(), pg.Vector2(0, 0), './assets/gui/hp_bar.png', self.display_surface)
        self.fill = AttributeBar.BarFill(pos.copy(), pg.Vector2(48, 15), './assets/gui/hp_fill.png', self.display_surface)
        self.lost = AttributeBar.BarLost(pos.copy(), pg.Vector2(48, 15), './assets/gui/hp_lost.png', self.display_surface)

        self.transition_frames = len(player.animations['hurt']) // 2
        self.max_hp = self.player.max_hp

    def lose_hp(self, amount: int) -> None:
        self.fill.change_val(self.player.current_hp, amount)
        self.lost.reduce_val(self.player.current_hp, amount, self.max_hp)
    
    def draw(self) -> None:
        self.base.draw()
        if self.player.animation_state == 'hurt':
            self.lost.animate_change(self.player.animation_frame)
            self.fill.animate_change(self.player.animation_frame, self.transition_frames, self.max_hp)
        else:
            self.fill.draw()

class AttributeBar:
    class BarBase:
        def __init__(self, pos: pg.Vector2, offset: pg.Vector2, png_path: str, display_surface: pg.Surface) -> None:
            self.image = pg.image.load(png_path).convert_alpha()
            self.display_surface = display_surface
            self.pos = pos
            self.offset = offset

        def draw(self) -> None:
            self.display_surface.blit(self.image, self.pos + self.offset)

    class BarFill(BarBase):
        def __init__(self, pos: pg.Vector2, offset: pg.Vector2, png_path: str, display_surface: pg.Surface) -> None:
            super().__init__(pos, offset, png_path, display_surface)
            self.full_width = self.image.get_width()
            self.height = self.image.get_height()
            self.val_change_target = 0
            self.val_change_amount = 0

        def change_val(self, new_val: int, amount: int) -> None:
            self.val_change_target = new_val
            self.val_change_amount = amount
        
        def animate_change(self, animation_frame: float, transition_frames: int, max_val: int) -> None:
            if animation_frame <= transition_frames:
                new_width = (
                    (self.val_change_target/max_val)*self.full_width +
                    ((transition_frames-animation_frame)/transition_frames) * (self.val_change_amount/max_val)*self.full_width)
                self.image = pg.transform.scale(self.image, (new_width, self.height))
            else:
                self.image = pg.transform.scale(self.image, ((self.val_change_target/max_val)*self.full_width, self.height))
            self.draw()

    class BarLost(BarBase):
        def __init__(self, pos: pg.Vector2, offset: pg.Vector2, png_path: str, display_surface: pg.Surface) -> None:
            super().__init__(pos, offset, png_path, display_surface)
            self.full_width = self.image.get_width()
            self.height = self.image.get_height()
            self.default_pos = pos.copy()

        def reduce_val(self, new_val: int, amount: int, max_val: int) -> None:
            self.pos.x = self.default_pos.x + (new_val/max_val) * self.full_width
            self.image = pg.transform.scale(self.image, ((amount/max_val)*self.full_width, self.height))
        
        def animate_change(self, animation_frame: float) -> None:
            if int(animation_frame) % 2 == 0:
                self.draw()