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

            # Create a beach-to-sea gradient: left side sand, right side water
            pct = x / max(1, width - 1)

            # If far right, more water
            if pct > 0.7:
                # Mostly shallow sea/water with occasional marine life
                if r < 0.80:
                    row.append(TILE_SWAMP_WATER)
                elif r < 0.90:
                    row.append(TILE_SEAL)
                else:
                    row.append(TILE_BELUGA)
            elif pct > 0.4:
                # Transition zone: mix of sand and water
                if r < 0.6:
                    row.append(TILE_SAND)
                elif r < 0.9:
                    row.append(TILE_SWAMP_WATER)
                else:
                    row.append(TILE_SEAL)
            else:
                # Near shore: mostly sand
                if r < 0.8:
                    row.append(TILE_SAND)
                else:
                    row.append(TILE_EMPTY)

        tiles.append(row)

    return tiles
