# systems/buildings.py
from game_state import GameState
from tile_types import (
    TILE_EMPTY,
    TILE_SAPLING,
    TILE_FARM,
    TILE_SOLAR,
    TILE_WIND,
    TILE_HOUSE,
)

from systems.world import get_current_biome_health, set_current_biome_health


def plant_tree(state: GameState):
    if state.in_house:
        return

    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_EMPTY:
        return
    if state.wood < 1:
        return

    state.wood -= 1
    state.tiles[y][x] = TILE_SAPLING

    health = get_current_biome_health(state) + 3
    set_current_biome_health(state, health)


def build_farm(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_EMPTY or state.wood < 2:
        return
    state.wood -= 2
    state.tiles[y][x] = TILE_FARM


def build_solar_panel(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_EMPTY or state.wood < 2:
        return
    state.wood -= 2
    state.tiles[y][x] = TILE_SOLAR


def build_wind_turbine(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_EMPTY or state.wood < 3:
        return
    state.wood -= 3
    state.tiles[y][x] = TILE_WIND


def build_house(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_EMPTY or state.wood < 5:
        return

    state.wood -= 5
    state.tiles[y][x] = TILE_HOUSE

    state.last_house_x = x
    state.last_house_y = y

    if state.house_tiles is None:
        state.house_tiles = [
            [TILE_EMPTY for _ in range(state.house_width)]
            for _ in range(state.house_height)
        ]


def try_enter_house(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] == TILE_HOUSE:
        state.in_house = True
        state.player_x = state.house_width // 2
        state.player_y = state.house_height // 2


def exit_house(state: GameState):
    if not state.in_house:
        return

    state.in_house = False

    for dy in [-1, 1, 0]:
        for dx in [-1, 1, 0]:
            nx = state.last_house_x + dx
            ny = state.last_house_y + dy
            if (
                0 <= nx < state.width
                and 0 <= ny < state.height
                and state.tiles[ny][nx] == TILE_EMPTY
            ):
                state.player_x = nx
                state.player_y = ny
                return

    state.player_x = state.last_house_x
    state.player_y = state.last_house_y
