import pygame as pg
import sys, time
from level import Level
from level_menu import LevelMenu
from settings import *
from leveldata import *
import tracemalloc

debug_mode = True

class Game:
    def __init__(self, surface: pg.Surface, debug_mode: bool = False):
        self.surface = surface
        self.debug_mode = debug_mode

        self.unlocked_levels = [0]

        self.level_menu = LevelMenu(self.surface, self.debug_mode)
        self.status = 'level_menu'
        
        self.player_lives = PLAYER_LIVES
        self.player_max_health = PLAYER_MAX_HEALTH
        self.player_current_health = PLAYER_MAX_HEALTH
        self.coins = 0

    def create_level(self, level: Level):
        self.level = Level(level_data=level, surface=screen, debug_mode=debug_mode)
        self.status = 'level'

    def add_health(self, amount: int):
        self.player_current_health += amount

    def check_game_over(self):
        if self.player_current_health <= 0:
            self.player_current_health = PLAYER_MAX_HEALTH
            self.coins = 0
            self.level_menu = LevelMenu()
            self.status = 'level_menu'

    def run(self):
        if self.status == 'level_menu':
            self.level_menu.run()
        elif self.status == 'level':
            self.level.run()
            self.check_game_over()

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pg.SCALED, vsync=1)
clock = pg.time.Clock()
game = Game(screen, debug_mode)
# game.create_level(level_1)

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
    
    if debug_mode: renderspeed(game.run)
    else: game.run()
    
    pg.display.update()
    clock.tick(60)