import pygame as pg
from settings import *
import load

class GuiBar:
    def __init__(self, surface: pg.Surface, level: int):
        self.display_surface = surface
        self.level = level

        # self.left_bar = pg.image.load('./assets/gui/guibar_left.png').convert_alpha()
        # self.right_bar = pg.image.load('./assets/gui/guibar_right.png').convert_alpha()
        
        # self.healthbar = pg.image.load('./assets/test_heart.png').convert_alpha()

    def show_base(self):
        pass
        # self.display_surface.blit(self.left_bar, (0, 0))
        # self.display_surface.blit(self.right_bar, (SCREEN_WIDTH-self.right_bar.get_width(), 0))

    def show_healthbar(self, current_health: int, max_health: int):
        pass
        # self.display_surface.blit(self.healthbar, (20, 20))