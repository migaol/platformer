import pygame as pg
import os, csv, re
from typing import List, Tuple
from settings import *

def import_folder(folder_path: str) -> List[pg.Surface]:
    surfaces = []
    img_filenames = []
    for _, _, filenames in os.walk(folder_path):
        for file in sorted(filenames):
            if file.endswith('.png'):
                img_filename = os.path.join(folder_path, file)
                img = pg.image.load(img_filename).convert_alpha()
                img_filenames.append(img_filename)
                surfaces.append(img)
    return surfaces, img_filenames

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

def import_spritesheet(folder_path: str, id: int) -> Tuple[str, int, int]:
    for _, _, filenames in os.walk(folder_path):
        for file in sorted(filenames):
            if re.match(r"^frames.*\.png$", file):
                params = file.split('-')
                if int(params[1].split('_')[0]) == id:
                    frame_width = int(params[3].removesuffix('px'))
                    frame_height = int(params[4].removesuffix('px.png'))
                    return os.path.join(folder_path, file), frame_width, frame_height

def import_tilesheet(png_path: str, frame_width: int = TILE_SIZE, frame_height: int = TILE_SIZE) -> List[pg.Surface]:
    surface = pg.image.load(png_path).convert_alpha()
    numx = surface.get_size()[0] // frame_width
    numy = surface.get_size()[1] // frame_height

    cut_tiles = []
    for r in range(numy):
        for c in range(numx):
            x, y = c*frame_width, r*frame_height
            tile = pg.Surface((frame_width, frame_height), flags=pg.SRCALPHA)
            tile.blit(surface, (0, 0), (x, y, frame_width, frame_height))
            cut_tiles.append(tile)
    return cut_tiles