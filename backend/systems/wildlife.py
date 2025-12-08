# systems/wildlife.py
import random

from game_state import GameState
from tile_types import (
    TILE_EMPTY,
    TILE_RABBIT, TILE_DEER, TILE_BIRD,
    TILE_LIZARD, TILE_SNAKE, TILE_SCORPION,
    TILE_ARCTIC_FOX, TILE_POLAR_HARE, TILE_SEAL, TILE_WALRUS,
    TILE_FROG, TILE_CROCODILE, TILE_STORK,
    TILE_GOAT, TILE_HAWK,
)

from systems.world import get_current_biome_health


def spawn_wildlife(state: GameState):
    if get_current_biome_health(state) < 70:
        return

    # Eco-Guardians spawn more wildlife (3% -> 5%)
    spawn_chance = 0.05 if state.eco_bonuses else 0.03
    if random.random() > spawn_chance:
        return

    x = random.randint(0, state.width - 1)
    y = random.randint(0, state.height - 1)

    if state.tiles[y][x] != TILE_EMPTY:
        return

    biome = state.current_biome

    if biome == "forest":
        animals = [TILE_RABBIT, TILE_DEER, TILE_BIRD]
    elif biome == "desert":
        animals = [TILE_LIZARD, TILE_SNAKE, TILE_SCORPION]
    elif biome == "tundra":
        animals = [TILE_ARCTIC_FOX, TILE_POLAR_HARE, TILE_SEAL, TILE_WALRUS]
    elif biome == "swamp":
        animals = [TILE_FROG, TILE_CROCODILE, TILE_SNAKE, TILE_STORK]
    elif biome == "mountain":
        animals = [TILE_GOAT, TILE_HAWK]
    else:
        return

    state.tiles[y][x] = random.choice(animals)


def despawn_wildlife(state: GameState):
    if get_current_biome_health(state) > 40:
        return

    for y in range(state.height):
        for x in range(state.width):
            tile = state.tiles[y][x]
            if tile in [
                TILE_RABBIT, TILE_DEER, TILE_BIRD,
                TILE_LIZARD, TILE_SNAKE, TILE_SCORPION,
                TILE_ARCTIC_FOX, TILE_POLAR_HARE, TILE_SEAL, TILE_WALRUS,
                TILE_FROG, TILE_CROCODILE, TILE_STORK,
                TILE_GOAT, TILE_HAWK,
            ]:
                state.tiles[y][x] = TILE_EMPTY
