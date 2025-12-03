import random
from tile_types import TILE_SANDSTONE, TILE_CACTUS, TILE_OASIS, TILE_LIZARD, TILE_SNAKE, TILE_SCORPION, TILE_EMPTY
BIOME_NAME = "desert"

def generate_desert(width, height):
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()
            if r < 0.15: row.append(TILE_SANDSTONE)   # like “rock”
            elif r < 0.25: row.append(TILE_CACTUS)   # collectible cactus
            elif r < 0.27: row.append(TILE_OASIS)    # small water spot
            else: row.append(TILE_EMPTY)
        tiles.append(row)
    return tiles

