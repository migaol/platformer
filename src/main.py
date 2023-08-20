import pygame as pg
import sys
from level import Level
from settings import *
from leveldata import *

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pg.SCALED, vsync=1)
clock = pg.time.Clock()

level = Level(level_data=test_level, surface=screen)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == KEY_QUIT):
            pg.quit()
            sys.exit()

    screen.fill('black')
    
    level.run()
    
    pg.display.update()
    clock.tick(60)