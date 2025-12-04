import random
from tile_types import (
    TILE_EMPTY,
    TILE_ROCK,
    TILE_STONE,
    TILE_CAVE
)

def generate_mountain(width, height):
    tiles = []

    for y in range(height):
        row = []
        for x in range(width):

            r = random.random()

            # Dense rocky terrain
            if r < 0.35:
                row.append(TILE_ROCK)
            elif r < 0.55:
                row.append(TILE_STONE)

            # Rare caves for future crafting or mining
            elif r < 0.58:
                row.append(TILE_CAVE)

            else:
                row.append(TILE_EMPTY)

        tiles.append(row)

    return tiles
