import pygame as pg
import os, csv, re
from typing import List, Dict, Tuple
from settings import *

def import_folder(folder_path: str) -> List[pg.Surface]:
    """
    Loads all `.png` images from a folder into `pygame` surfaces.

    Parameters:
        - `folder_path` (`str`): The path to the folder containing `.png` images

    Returns:
        - `Tuple[List[pg.Surface], List[str]]`:
            - List of images converted to `pygame.surface`
            - Corresponding filenames
    """
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

def import_background_files(folder_path: str) -> Dict[str, List[str]]:
    """
    Imports background files and categorize by layer type.  Does not create `pygame.image` objects.
    
    Parameters:
        - `folder_path` (`str`): The path to the folder containing background `.png` images

    Returns:
        - `Dict[List[str]]`: A dictionary containing lists of filenames categorized by layer
        ('static', 'background', 'midground', 'foreground')
    """
    bg_files = {'static': [], 'background': [], 'midground': [], 'foreground': []}
    for _, _, filenames in os.walk(folder_path):
        for file in sorted(filenames):
            if file.endswith('.png'):
                for layer_type in bg_files:
                    if file.startswith(layer_type):
                        bg_files[layer_type].append(os.path.join(folder_path, file))
    return bg_files

def import_csv_layout(folder_path: str) -> List[List[str]]:
    """
    Imports a `.csv` layout file representing map tile data.
    
    Parameters:
        - `folder_path` (`str`): The path to the `.csv` file containing map tile data

    Returns:
        - `List[List[str]]`: A 2D list representing the map tile layout
    """
    terrain_map = []
    with open(folder_path) as map:
        level = csv.reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
    return terrain_map

def import_spritesheet(folder_path: str, id: int) -> Tuple[str, int, int]:
    """
    Imports a sprite with non-standard dimensions and extracts dimensions.
    Does not create `pygame.image` objects.  Non-standard spritesheet files must have the format:
    `frames-[tile id]_[optional name]-[num frames]f-[width]px-[height]px.png`;
    for example: `frames-0_bush-8f-128px-64px.png`

    Parameters:
        - `folder_path` (`str`): The path to the folder containing the spritesheet `.png`
        - `id` (`int`): The ID of the sprite to search for

    Returns:
        - `Tuple[str, int, int]`:
            - The file path of the spritesheet
            - The width of each sprite frame (px)
            - The height of each sprite frame (px)
    """
    for _, _, filenames in os.walk(folder_path):
        for file in sorted(filenames):
            if re.match(r"^frames.*\.png$", file):
                params = file.split('-')
                if int(params[1].split('_')[0]) == id:
                    frame_width = int(params[3].removesuffix('px'))
                    frame_height = int(params[4].removesuffix('px.png'))
                    return os.path.join(folder_path, file), frame_width, frame_height
    return None

def import_tilesheet(png_path: str, frame_width: int = TILE_SIZE, frame_height: int = TILE_SIZE) -> List[pg.Surface]:
    """
    Imports tiles/sprites from a tilesheet `.png` file.
    Cuts tiles/sprites according to the specified dimensions.

    Parameters:
        `png_path` (`str`): The path to the tilesheet `.png`
        `frame_width` (`int`): The width of each tile frame (px, default: `TILE_SIZE`)
        `frame_height` (`int`): The height of each tile frame in pixels (px, default: `TILE_SIZE`)

    Returns:
        `List[pg.Surface]`: List of cut images converted to `pygame.surface`
    """
    surface = pg.image.load(png_path).convert_alpha()
    dimx, dimy = surface.get_size()
    numx, numy = dimx//frame_width, dimy//frame_height

    cut_tiles = []
    for r in range(numy):
        for c in range(numx):
            x, y = c*frame_width, r*frame_height
            tile = pg.Surface((frame_width, frame_height), flags=pg.SRCALPHA)
            tile.blit(surface, (0, 0), (x, y, frame_width, frame_height))
            cut_tiles.append(tile)
    return cut_tiles