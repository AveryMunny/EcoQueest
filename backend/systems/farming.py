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

# One full day-night cycle (matches app.py defaults: 5 min day + 5 min night)
DAY_LENGTH = 5 * 60
NIGHT_LENGTH = 5 * 60
FULL_CYCLE_SECONDS = DAY_LENGTH + NIGHT_LENGTH

def plant_wheat(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_FARM:
        return
    state.tiles[y][x] = TILE_WHEAT_1
    if state.crop_growth is None:
        state.crop_growth = {}
    state.crop_growth[f"{x},{y}"] = time.time()


def plant_carrot(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_FARM:
        return
    state.tiles[y][x] = TILE_CARROT_1
    if state.crop_growth is None:
        state.crop_growth = {}
    state.crop_growth[f"{x},{y}"] = time.time()


def grow_crops(state: GameState):
    now = time.time()
    # Eco-Guardians grow crops 20% faster (multiply age)
    growth_multiplier = 1.2 if state.eco_bonuses else 1.0
    half_cycle = FULL_CYCLE_SECONDS * 0.5

    # Support both tuple keys and string keys ("x,y") in crop_growth
    for key, start in list((state.crop_growth or {}).items()):
        try:
            if isinstance(key, str):
                x_str, y_str = key.split(",")
                x, y = int(x_str), int(y_str)
            else:
                x, y = key
        except Exception:
            # malformed key; skip
            continue

        age_seconds = (now - start) * growth_multiplier

        # guard coordinates
        if not (0 <= x < state.width and 0 <= y < state.height):
            continue

        tile = state.tiles[y][x]

        # One full day-night cycle to mature: stage 1 -> 2 at half-cycle, 2 -> 3 at full cycle
        if tile == TILE_WHEAT_1 and age_seconds >= half_cycle:
            state.tiles[y][x] = TILE_WHEAT_2
        elif tile == TILE_WHEAT_2 and age_seconds >= FULL_CYCLE_SECONDS:
            state.tiles[y][x] = TILE_WHEAT_3
        elif tile == TILE_CARROT_1 and age_seconds >= half_cycle:
            state.tiles[y][x] = TILE_CARROT_2
        elif tile == TILE_CARROT_2 and age_seconds >= FULL_CYCLE_SECONDS:
            state.tiles[y][x] = TILE_CARROT_3


def harvest_crop(state: GameState):
    x, y = state.player_x, state.player_y
    tile = state.tiles[y][x]

    if tile == TILE_WHEAT_3:
        if state.inventory is None:
            state.inventory = {}
        state.inventory["wheat"] = state.inventory.get("wheat", 0) + 3
        state.tiles[y][x] = TILE_FARM
        # remove crop growth entry for this tile (support string or tuple key)
        if state.crop_growth is not None:
            state.crop_growth.pop(f"{x},{y}", None)
            state.crop_growth.pop((x, y), None)

    elif tile == TILE_CARROT_3:
        if state.inventory is None:
            state.inventory = {}
        state.inventory["carrot"] = state.inventory.get("carrot", 0) + 2
        state.tiles[y][x] = TILE_FARM
        if state.crop_growth is not None:
            state.crop_growth.pop(f"{x},{y}", None)
            state.crop_growth.pop((x, y), None)
