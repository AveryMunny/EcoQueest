import random
from tile_types import (
    TILE_SNOW, TILE_ICE, TILE_SNOWFLAKE, TILE_SNOWY_TREE,
    TILE_ICE_CRYSTAL, TILE_FROSTED_BERRIES, TILE_ICEBERG,
    TILE_PENGUIN, TILE_ARCTIC_FOX, TILE_POLAR_HARE,
    TILE_WALRUS, TILE_SEAL, TILE_BELUGA,
    TILE_SNOWMAN, TILE_IGLOO,
    TILE_EMPTY
)

BIOME_NAME = "tundra"

def generate_tundra(width, height):
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()
            if r < 0.10: row.append(TILE_SNOWY_TREE)
            elif r < 0.15: row.append(TILE_FROSTED_BERRIES)
            elif r < 0.20: row.append(TILE_ICE)
            elif r < 0.22: row.append(TILE_ICE_CRYSTAL)
            else: row.append(TILE_SNOW)
        tiles.append(row)
    return tiles

