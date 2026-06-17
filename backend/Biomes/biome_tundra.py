import random

BIOME_NAME = "tundra"

from tile_types import (
    TILE_SNOW,
    TILE_ICE,
    TILE_SNOWY_TREE,
    TILE_ICE_CRYSTAL,
    TILE_SNOWFLAKE,
    TILE_FROSTED_BERRIES,
    TILE_IGLOO,
    TILE_SNOWMAN,
    TILE_ICEBERG,
    TILE_EMPTY
)

def generate_tundra(width, height):
    tiles = []

    for y in range(height):
        row = []
        elevation = y / height

        for x in range(width):
            r = random.random()

            # -----------------------------
            # LARGE OPEN SPACE (SNOW)
            # -----------------------------
            if r < 0.55:
                row.append(TILE_EMPTY)

            # -----------------------------
            # ICE PATCHES
            # -----------------------------
            elif r < 0.65:
                if elevation > 0.5:
                    row.append(TILE_ICE)
                else:
                    row.append(TILE_SNOW)

            # -----------------------------
            # SNOWY TREES (collectible)
            # -----------------------------
            elif r < 0.72:
                row.append(TILE_SNOWY_TREE)

            # -----------------------------
            # FROSTED BERRIES (collectible)
            # -----------------------------
            elif r < 0.78:
                row.append(TILE_FROSTED_BERRIES)

            # -----------------------------
            # SNOWFLAKE (collectible)
            # -----------------------------
            elif r < 0.83:
                row.append(TILE_SNOWFLAKE)

            # -----------------------------
            # RARE ICE CRYSTAL
            # -----------------------------
            elif r < 0.86:
                row.append(TILE_ICE_CRYSTAL)

            # -----------------------------
            # ULTRA RARE IGLOO
            # -----------------------------
            elif r < 0.87:
                row.append(TILE_IGLOO)

            # -----------------------------
            # ULTRA RARE ICEBERG (high elevation only)
            # FIX: TILE_ICEBERG had a collection handler in collection.py
            # but was never actually placed on the map anywhere. Give it a
            # small chance to appear in the "deeper" half of the tundra.
            # -----------------------------
            elif r < 0.875 and elevation > 0.5:
                row.append(TILE_ICEBERG)

            # -----------------------------
            # ULTRA RARE SNOWMAN
            # -----------------------------
            elif r < 0.88:
                row.append(TILE_SNOWMAN)

            # -----------------------------
            # EMPTY TILE
            # -----------------------------
            else:
                row.append(TILE_EMPTY)

        tiles.append(row)

    return tiles