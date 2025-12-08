import random
from tile_types import (
    TILE_EMPTY,
    TILE_SAND,
    TILE_OCEAN,
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

            # --- FAR RIGHT: DEEP BLUE OCEAN ---
            if pct > 0.7:
                if r < 0.90:
                    row.append(TILE_OCEAN)  # mostly pure blue
                elif r < 0.95:
                    row.append(TILE_SEAL)
                else:
                    row.append(TILE_BELUGA)

            # --- MID AREA: SHALLOW SEA / BEACH BLEND ---
            elif pct > 0.4:
                if r < 0.50:
                    row.append(TILE_SAND)
                elif r < 0.80:
                    row.append(TILE_OCEAN)
                else:
                    row.append(TILE_EMPTY)  # beach openings

            # --- SHORE: BEACH ---
            else:
                if r < 0.60:
                    row.append(TILE_SAND)
                else:
                    row.append(TILE_EMPTY)

            # End tile
        tiles.append(row)

    return tiles
