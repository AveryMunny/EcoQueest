import random
from tile_types import (
    TILE_SNOW,
    TILE_ICE,
    TILE_SNOWY_TREE,
    TILE_ICE_CRYSTAL,
    TILE_SNOWFLAKE,
    TILE_FROSTED_BERRIES,
    TILE_ICEBERG,
    TILE_SNOWMAN,
    TILE_IGLOO,
    TILE_EMPTY
)
BIOME_NAME = "tundra"
def generate_tundra(width, height):
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()
            if r < 0.15: row.append(TILE_SNOW)          # snowy ground
            elif r < 0.30: row.append(TILE_SNOWY_TREE)  # snowy tree
            elif r < 0.35: row.append(TILE_ICE_CRYSTAL) # ice crystal
            elif r < 0.40: row.append(TILE_SNOWFLAKE)   # collectible snowflake
            else: row.append(TILE_EMPTY)
        tiles.append(row)
    return tiles

