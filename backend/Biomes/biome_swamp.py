import random
from tile_types import (
    TILE_MUD,
    TILE_SWAMP_GRASS,
    TILE_REEDS,
    TILE_SWAMP_WATER,
    TILE_MUSHROOM,
    TILE_PEAT,
    TILE_EMPTY
)

BIOME_NAME = "swamp"

def generate_swamp(width, height):
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()

            if r < 0.15:
                row.append(TILE_MUD)
            elif r < 0.25:
                row.append(TILE_SWAMP_GRASS)
            elif r < 0.30:
                row.append(TILE_REEDS)          # collectible → fiber
            elif r < 0.33:
                row.append(TILE_MUSHROOM)       # collectible → food
            elif r < 0.36:
                row.append(TILE_PEAT)           # collectible → fuel
            elif r < 0.38:
                row.append(TILE_SWAMP_WATER)
            else:
                row.append(TILE_EMPTY)

        tiles.append(row)
    return tiles
