import random
from tile_types import (
    TILE_RABBIT, TILE_DEER, TILE_BIRD,
    TILE_LIZARD, TILE_SNAKE, TILE_SCORPION,
    TILE_ARCTIC_FOX, TILE_POLAR_HARE, TILE_SEAL, TILE_WALRUS,
    TILE_FROG, TILE_CROCODILE, TILE_TURTLE, TILE_STORK,
    TILE_GOAT, TILE_HAWK,

    TILE_EMPTY, TILE_HOUSE, TILE_WIND, TILE_SOLAR, TILE_FARM
)

ANIMAL_TILES = {
    TILE_RABBIT, TILE_DEER, TILE_BIRD,
    TILE_LIZARD, TILE_SNAKE, TILE_SCORPION,
    TILE_ARCTIC_FOX, TILE_POLAR_HARE, TILE_SEAL, TILE_WALRUS,
    TILE_FROG, TILE_CROCODILE, TILE_TURTLE, TILE_STORK,
    TILE_GOAT, TILE_HAWK
}

BLOCKING_TILES = {TILE_HOUSE, TILE_WIND, TILE_SOLAR, TILE_FARM}

def move_animals(state):
    """Make animals randomly wander 1 tile per turn."""
    tiles = state.tiles
    width, height = state.width, state.height

    # Collect all animal positions
    animals = []
    for y in range(height):
        for x in range(width):
            if tiles[y][x] in ANIMAL_TILES:
                animals.append((x, y, tiles[y][x]))

    # Try to move each animal
    for x, y, animal in animals:

        # 25% chance an animal moves
        if random.random() > 0.25:
            continue

        # Choose random direction
        dx, dy = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        nx, ny = x + dx, y + dy

        # Check boundaries
        if not (0 <= nx < width and 0 <= ny < height):
            continue

        # Check collision
        target = tiles[ny][nx]
        if target != TILE_EMPTY:
            continue

        # Move the animal
        tiles[ny][nx] = animal
        tiles[y][x] = TILE_EMPTY
