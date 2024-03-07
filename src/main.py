import pygame as pg
import sys, time
from typing import Tuple
from level import Level
from level_menu import LevelMenu
from settings import *
from leveldata import *
import tracemalloc

debug_mode = False

class Game:
    def __init__(self, surface: pg.Surface, debug_mode: bool = False) -> None:
        self.surface = surface
        self.debug_mode = debug_mode

        self.current_world = 1

        self.level_menu = LevelMenu(surface=self.surface, current_world=self.current_world, debug_mode=self.debug_mode)
        self.display_mode = 'level_menu'
        
        self.player_lives = PLAYER_LIVES
        self.player_max_health = PLAYER_MAX_HEALTH
        self.player_current_health = PLAYER_MAX_HEALTH
        self.coins = 0
        self.score = 0

    def create_level(self, level: Tuple[int, int]) -> None:
        self.level = Level(level=level, surface=screen, debug_mode=debug_mode)
        self.display_mode = 'level'

    def add_health(self, amount: int) -> None:
        self.player_current_health += amount

    def get_input(self) -> None:
        pressed = pg.key.get_pressed()
        if pressed[KEY_SELECT] and self.display_mode == 'level_menu':
            self.click(self.level_menu.get_player_pos())

    def click(self, pos: Tuple) -> None:
        if self.display_mode == 'level_menu':
            selected_level = self.level_menu.get_level()
            if selected_level: self.create_level(selected_level)

    def check_game_over(self) -> None:
        if self.player_current_health <= 0:
            self.player_current_health = PLAYER_MAX_HEALTH
            self.coins = 0
            self.level_menu = LevelMenu()
            self.display_mode = 'level_menu'

    def run(self) -> None:
        if self.display_mode == 'level_menu':
            self.level_menu.run()
            self.get_input()
        elif self.display_mode == 'level':
            self.level.run()
            self.check_game_over()

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pg.SCALED, vsync=1)
clock = pg.time.Clock()
game = Game(screen, debug_mode)

tracemalloc.start()
speed = {'slowest': 0, 'avg': 0, 'frames': 0}
def renderspeed(run):
    t1 = time.time()
    run()
    t2 = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    speed['slowest'] = max(t2-t1, speed['slowest'])
    speed['avg'] = (speed['avg'] * speed['frames'] + (t2-t1)*1000) / (speed['frames'] + 1)
    speed['frames'] += 1
    print(f"frames: {speed['frames']}  " +
            f"TIME current: {(t2-t1)*1000:.4f}ms  " +
            f"avg: {speed['avg']:.4f}ms  " +
            f"peak: {speed['slowest']*1000:.4f}ms  " +
            f"MEMORY current: {current_mem/100:.3f}kb  peak: {peak_mem/100:.3f}kb")

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == KEY_QUIT):
            pg.quit()
            sys.exit()
        if debug_mode and event.type == pg.MOUSEMOTION:
            print(event.pos)
        if event.type == pg.MOUSEBUTTONUP:
            game.click(event.pos)
    
    if debug_mode: renderspeed(game.run)
    else: game.run()
    
    pg.display.update()
    clock.tick(60)