import random
from tile_types import (
    TILE_SAND,          # base desert floor
    TILE_CACTUS,        # plant
    TILE_SANDSTONE,     # building material
    TILE_QUARTZ,        # rare gem
    TILE_EMPTY
)

BIOME_NAME = "desert"

def generate_desert(width, height):
    tiles = []

    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()

            if r < 0.60:
                row.append(TILE_EMPTY)          # 60% REAL empty
            elif r < 0.85:
                row.append(TILE_SAND)           # 25% subtle sand
            elif r < 0.90:
                row.append(TILE_CACTUS)         # 5% cactus
            elif r < 0.96:
                row.append(TILE_SANDSTONE)      # 6% sandstone
            else:
                row.append(TILE_QUARTZ)         # 4% quartz

        tiles.append(row)

    return tiles
