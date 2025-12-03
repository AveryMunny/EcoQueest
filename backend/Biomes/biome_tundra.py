import random
from tile_types import TILE_SNOW, TILE_EMPTY

def generate_tundra(width, height):
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            if random.random() < 0.85:
                row.append(TILE_SNOW)
            else:
                row.append(TILE_EMPTY)
        tiles.append(row)
    return tiles
BIOME_NAME = "tundra"