import random
from tile_types import (
    TILE_EMPTY,
    TILE_SAND,
    TILE_SWAMP_WATER,
    TILE_SEAL,
    TILE_BELUGA,
)

BIOME_NAME = "coastal"

def generate_coastal(width, height):
    tiles = []

    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()
            pct = x / max(1, width - 1)

            # --- FAR RIGHT (deep water) ---
            if pct > 0.7:
                if r < 0.50:  # much less water density
                    row.append(TILE_SWAMP_WATER)
                elif r < 0.55:
                    row.append(TILE_SEAL)
                elif r < 0.60:
                    row.append(TILE_BELUGA)
                else:
                    row.append(TILE_EMPTY)  # add empty water gaps

            # --- MID ZONE (shallow water + sand) ---
            elif pct > 0.4:
                if r < 0.30:  # sand
                    row.append(TILE_SAND)
                elif r < 0.45:  # shallow water patches
                    row.append(TILE_SWAMP_WATER)
                else:
                    row.append(TILE_EMPTY)  # open beach dunes

            # --- SHORELINE / BEACH ---
            else:
                if r < 0.55:
                    row.append(TILE_SAND)
                else:
                    row.append(TILE_EMPTY)  # lots more walkable land

            # End tile
        tiles.append(row)

    return tiles
