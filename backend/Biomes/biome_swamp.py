import random
from tile_types import TILE_MUD, TILE_SWAMP_GRASS, TILE_REEDS, TILE_SWAMP_WATER, TILE_EMPTY
BIOME_NAME = "swamp"

def generate_swamp(width, height):
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()
            if r < 0.15: row.append(TILE_MUD)
            elif r < 0.25: row.append(TILE_SWAMP_GRASS)
            elif r < 0.30: row.append(TILE_REEDS)
            elif r < 0.32: row.append(TILE_SWAMP_WATER)
            else: row.append(TILE_EMPTY)
        tiles.append(row)
    return tiles
