import pygame as pg
import os, csv
from typing import List
from settings import *

def import_folder(folder_path: str) -> List[pg.Surface]:
    surfaces = []
    for _, _, filenames in os.walk(folder_path):
        for file in sorted(filenames):
            if file.endswith('.png'):
                img = pg.image.load(os.path.join(folder_path, file)).convert_alpha()
                surfaces.append(img)
    return surfaces

def import_background_files(folder_path: str) -> List[str]:
    bg_files = {'static': [], 'background': [], 'midground': [], 'foreground': []}
    for _, _, filenames in os.walk(folder_path):
        for file in sorted(filenames):
            if file.endswith('.png'):
                for layer_type in bg_files:
                    if file.startswith(layer_type):
                        bg_files[layer_type].append(os.path.join(folder_path, file))
    return bg_files

def import_csv_layout(folder_path: str) -> List[List[str]]:
    terrain_map = []
    with open(folder_path) as map:
        level = csv.reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
    return terrain_map

def import_tilesheet(png_path: str) -> List[pg.Surface]:
    surface = pg.image.load(png_path).convert_alpha()
    numx = surface.get_size()[0] // TILE_SIZE
    numy = surface.get_size()[1] // TILE_SIZE

    cut_tiles = []
    for r in range(numy):
        for c in range(numx):
            x, y = c*TILE_SIZE, r*TILE_SIZE
            tile = pg.Surface((TILE_SIZE, TILE_SIZE), flags=pg.SRCALPHA)
            tile.blit(surface, (0, 0), (x, y, TILE_SIZE, TILE_SIZE))
            cut_tiles.append(tile)
    return cut_tiles