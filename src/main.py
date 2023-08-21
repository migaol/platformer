import pygame as pg
import sys, time
from level import Level
from settings import *
from leveldata import *

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pg.SCALED, vsync=1)
clock = pg.time.Clock()

level = Level(level_data=test_level, surface=screen)

slowest = [0]
def renderspeed(run):
    t1 = time.time()
    run()
    t2 = time.time()
    slowest[0] = max(t2-t1, slowest[0])
    print(f'{(t2-t1)*1000:.4f}ms\t{slowest[0]*1000:.4f}ms')

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == KEY_QUIT):
            pg.quit()
            sys.exit()

    screen.fill('black')
    
    renderspeed(level.run)
    # level.run()
    
    pg.display.update()
    clock.tick(60)