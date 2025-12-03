import random
from tile_types import TILE_TREE, TILE_BERRIES, TILE_COAL, TILE_EMPTY

BIOME_NAME = "forest"

# Resource types you used originally
RESOURCE_TYPES = [TILE_TREE, TILE_COAL, TILE_BERRIES]

def generate_forest(width, height):
    tiles = []

    for y in range(height):
        row = []
        for x in range(width):

            # Same logic as your old create_initial_state()
            if random.random() < 0.25:
                row.append(random.choice(RESOURCE_TYPES))
            else:
                row.append(TILE_EMPTY)

        tiles.append(row)

    return tiles
