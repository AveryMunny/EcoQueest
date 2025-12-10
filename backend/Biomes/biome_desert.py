import random
from tile_types import (
    TILE_EMPTY,
    TILE_SAND,
    TILE_CACTUS,
    TILE_SANDSTONE,
    TILE_QUARTZ,
    TILE_OASIS,
    TILE_NPC_DESERT_MERCHANT
)

BIOME_NAME = "desert"

def generate_desert(width, height):
    tiles = []

    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()

            # BALANCED DESERT DISTRIBUTION
            if r < 0.65:
                row.append(TILE_EMPTY)          # 65% empty
            elif r < 0.85:
                row.append(TILE_SAND)           # 25% subtle sand
            elif r < 0.89:
                row.append(TILE_CACTUS)         # 4% cactus
            elif r < 0.93:
                row.append(TILE_SANDSTONE)      # 4% sandstone
            elif r < 0.95:
                row.append(TILE_OASIS)          # 2% oasis (your old version)
            else:
                row.append(TILE_QUARTZ)         # 2% quartz (rare)

        tiles.append(row)

    # Place desert merchant near spawn
    mid_x = width // 2 + 3
    mid_y = height // 2 - 2
    tiles[mid_y][mid_x] = TILE_NPC_DESERT_MERCHANT

    return tiles
