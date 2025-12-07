# systems/farming.py
import time

from game_state import GameState
from tile_types import (
    TILE_FARM,
    TILE_WHEAT_1,
    TILE_WHEAT_2,
    TILE_WHEAT_3,
    TILE_CARROT_1,
    TILE_CARROT_2,
    TILE_CARROT_3,
)

START_TIME = time.time()

def plant_wheat(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_FARM:
        return
    state.tiles[y][x] = TILE_WHEAT_1
    state.crop_growth[(x, y)] = time.time()


def plant_carrot(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_FARM:
        return
    state.tiles[y][x] = TILE_CARROT_1
    state.crop_growth[(x, y)] = time.time()


def grow_crops(state: GameState):
    elapsed = time.time() - START_TIME
    for (x, y), start in list(state.crop_growth.items()):
        age = (elapsed - start) / 60.0
        tile = state.tiles[y][x]

        if tile == TILE_WHEAT_1 and age >= 3:
            state.tiles[y][x] = TILE_WHEAT_2
        elif tile == TILE_WHEAT_2 and age >= 6:
            state.tiles[y][x] = TILE_WHEAT_3
        elif tile == TILE_CARROT_1 and age >= 2:
            state.tiles[y][x] = TILE_CARROT_2
        elif tile == TILE_CARROT_2 and age >= 5:
            state.tiles[y][x] = TILE_CARROT_3


def harvest_crop(state: GameState):
    x, y = state.player_x, state.player_y
    tile = state.tiles[y][x]

    if tile == TILE_WHEAT_3:
        state.food += 3
        state.tiles[y][x] = TILE_FARM
        del state.crop_growth[(x, y)]

    elif tile == TILE_CARROT_3:
        state.food += 2
        state.tiles[y][x] = TILE_FARM
        del state.crop_growth[(x, y)]
