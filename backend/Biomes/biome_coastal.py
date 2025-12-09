import random
from tile_types import (
    TILE_SAND,
    TILE_OCEAN,
    TILE_SEAL,
    TILE_CRAB,
    TILE_SHELL,
    TILE_EMPTY,
)
BIOME_NAME = "coastal"

def generate_coastal(width, height):
    tiles = []

    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()

            # Beach gradient: left (x=0) is sand/beach, right (x=width-1) is ocean
            pct = x / max(1, width - 1)

            if pct < 0.3:
                # Left side: mostly sand with some shells
                if r < 0.35:
                    row.append(TILE_SAND)
                elif r < 0.15:
                    row.append(TILE_SHELL)
                else:
                    row.append(TILE_EMPTY)
            elif pct < 0.6:
                # Middle transition: mix of sand and ocean
                if r < 0.1:
                    row.append(TILE_SAND)
                elif r < 0.05:
                    row.append(TILE_OCEAN)
                elif r < 0.05:
                    row.append(TILE_CRAB)
                else:
                    row.append(TILE_EMPTY)
            else:
                # Right side: mostly ocean with some crabs
                if r < 0.35:
                    row.append(TILE_OCEAN)
                elif r < 0.25:
                    row.append(TILE_CRAB)
                else:
                    row.append(TILE_EMPTY)

        tiles.append(row)

    return tiles