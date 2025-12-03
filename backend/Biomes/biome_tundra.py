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

            # --- Terrain ---
            if r < 0.45:                     # 45% snow
                row.append(TILE_SNOW)

            elif r < 0.60:                   # 15% ice sheets
                row.append(TILE_ICE)

            elif r < 0.70:                   # 10% snowflakes (decorative)
                row.append(TILE_SNOWFLAKE)

            elif r < 0.77:                   # 7% snowy trees
                row.append(TILE_SNOWY_TREE)

            elif r < 0.83:                   # 6% ice crystals (collectable)
                row.append(TILE_ICE_CRYSTAL)

            elif r < 0.87:                   # 4% frosted berries (food)
                row.append(TILE_FROSTED_BERRIES)

            elif r < 0.89:                   # rare icebergs
                row.append(TILE_ICEBERG)

            # --- Wildlife ---
            elif r < 0.915:
                row.append(TILE_PENGUIN)
            elif r < 0.93:
                row.append(TILE_ARCTIC_FOX)
            elif r < 0.945:
                row.append(TILE_POLAR_HARE)
            elif r < 0.955:
                row.append(TILE_WALRUS)
            elif r < 0.965:
                row.append(TILE_SEAL)
            elif r < 0.975:
                row.append(TILE_BELUGA)

            # --- Rare structures ---
            elif r < 0.982:
                row.append(TILE_SNOWMAN)
            elif r < 0.99:
                row.append(TILE_IGLOO)

            else:
                row.append(TILE_EMPTY)

        tiles.append(row)

    return tiles
