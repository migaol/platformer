import pygame as pg
import random
from typing import List
import load
from player import Player
from particles import ParticleEffect
from tile import *
from bg import *
from settings import *

class LevelMenu:
    def __init__(self, surface: pg.Surface, debug_mode: bool = False):
        self.display_surface = surface
        self.debug_mode = debug_mode

        self.background = pg.sprite.Group()
        self.background.add(StaticBackground(0, SCREEN_HEIGHT, 'assets/test_levelmap.png'))

    def run(self):
        # self.background.update(self.player_movement)
        self.background.draw(self.display_surface)