# systems/wildlife.py
import random

from game_state import GameState
from tile_types import (
    TILE_EMPTY,
    TILE_RABBIT, TILE_DEER, TILE_BIRD,
    TILE_LIZARD, TILE_SNAKE, TILE_SCORPION,
    TILE_ARCTIC_FOX, TILE_POLAR_HARE, TILE_SEAL, TILE_WALRUS,
    TILE_FROG, TILE_CROCODILE, TILE_STORK, TILE_TURTLE,
    TILE_GOAT, TILE_HAWK,
    TILE_CRAB,
)

from systems.world import get_current_biome_health


def spawn_wildlife(state: GameState):
    if get_current_biome_health(state) < 70:
        return

    # FIX: comment previously said "3% -> 6%", which didn't match the
    # actual numbers below (5% baseline, doubled to 10% for Eco-Guardians,
    # halved to 2.5% for Industrialists). Comment now matches the code.
    # Eco-Guardians spawn more wildlife (5% -> 10%)
    # Industrialists spawn less wildlife (5% -> 2.5%)
    if state.eco_bonuses:
        spawn_chance = 0.1
    elif state.industry_bonuses:
        spawn_chance = 0.025
    else:
        spawn_chance = 0.05
    
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
        animals = [TILE_FROG, TILE_CROCODILE, TILE_SNAKE, TILE_STORK, TILE_TURTLE]
    elif biome == "mountain":
        animals = [TILE_GOAT, TILE_HAWK]
    elif biome == "coastal":
        # Seals and crabs wander the shore dynamically.
        # (Static crabs are also placed by the biome generator, but
        # wildlife spawning adds living ones that move around.)
        animals = [TILE_SEAL, TILE_CRAB]
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
                TILE_FROG, TILE_CROCODILE, TILE_TURTLE, TILE_STORK,
                TILE_GOAT, TILE_HAWK,
                TILE_CRAB,  # coastal
            ]:
                state.tiles[y][x] = TILE_EMPTY