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

            # 75% plain snow (calm, open tundra)
            if r < 0.75:
                row.append(TILE_SNOW)

            # 10% ice patches
            elif r < 0.85:
                row.append(TILE_ICE)

            # 5% snowflakes (decorative)
            elif r < 0.90:
                row.append(TILE_SNOWFLAKE)

            # 3% snowy trees
            elif r < 0.93:
                row.append(TILE_SNOWY_TREE)

            # 2% ice crystals
            elif r < 0.95:
                row.append(TILE_ICE_CRYSTAL)

            # 2% frosted berries
            elif r < 0.97:
                row.append(TILE_FROSTED_BERRIES)

            # 1% rare iceberg
            elif r < 0.98:
                row.append(TILE_ICEBERG)

            else:
                row.append(TILE_EMPTY)

        tiles.append(row)

    return tiles

