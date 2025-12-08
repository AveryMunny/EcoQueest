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

from systems.inventory import has_items, remove_item
from systems.world import get_current_biome_health, set_current_biome_health



# -------------------------------
# Plant Tree (cost: 1 wood)
# -------------------------------
def plant_tree(state: GameState):
    if state.in_house:
        return

    x, y = state.player_x, state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return

    # NEW inventory-based check
    if not has_items(state, wood=1):
        return

    remove_item(state, "wood", 1)
    state.tiles[y][x] = TILE_SAPLING

    health = get_current_biome_health(state) + 3
    set_current_biome_health(state, health)



# -------------------------------
# Build Farm (cost: 2 wood, 1 wood for Industrialists)
# -------------------------------
def build_farm(state: GameState):
    x, y = state.player_x, state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return

    wood_cost = 1 if state.industry_bonuses else 2
    if not has_items(state, wood=wood_cost):
        return

    remove_item(state, "wood", wood_cost)
    state.tiles[y][x] = TILE_FARM
    
    # Industrialists consume ecosystem health
    if state.industry_bonuses:
        health = get_current_biome_health(state) - 2
        set_current_biome_health(state, health)



# -------------------------------
# Build Solar Panel (cost: 2 wood, 1 wood for Industrialists)
# -------------------------------
def build_solar_panel(state: GameState):
    x, y = state.player_x, state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return

    wood_cost = 1 if state.industry_bonuses else 2
    if not has_items(state, wood=wood_cost):
        return

    remove_item(state, "wood", wood_cost)
    state.tiles[y][x] = TILE_SOLAR
    
    # Industrialists consume ecosystem health
    if state.industry_bonuses:
        health = get_current_biome_health(state) - 2
        set_current_biome_health(state, health)



# -------------------------------
# Build Wind Turbine (cost: 3 wood, 2 wood for Industrialists)
# -------------------------------
def build_wind_turbine(state: GameState):
    x, y = state.player_x, state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return

    wood_cost = 2 if state.industry_bonuses else 3
    if not has_items(state, wood=wood_cost):
        return

    remove_item(state, "wood", wood_cost)
    state.tiles[y][x] = TILE_WIND
    
    # Industrialists consume ecosystem health
    if state.industry_bonuses:
        health = get_current_biome_health(state) - 2
        set_current_biome_health(state, health)



# -------------------------------
# Build House (cost: 5 wood, 3 wood for Industrialists)
# -------------------------------
def build_house(state: GameState):
    x, y = state.player_x, state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return

    wood_cost = 3 if state.industry_bonuses else 5
    if not has_items(state, wood=wood_cost):
        return

    remove_item(state, "wood", wood_cost)
    state.tiles[y][x] = TILE_HOUSE

    state.last_house_x = x
    state.last_house_y = y

    if state.house_tiles is None:
        # Build interior layout
        state.house_tiles = [
            [TILE_EMPTY for _ in range(state.house_width)]
            for _ in range(state.house_height)
        ]
    
    # Industrialists consume ecosystem health
    if state.industry_bonuses:
        health = get_current_biome_health(state) - 3
        set_current_biome_health(state, health)



# -------------------------------
# House Entry / Exit
# -------------------------------
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
                0 <= nx < state.width and
                0 <= ny < state.height and
                state.tiles[ny][nx] == TILE_EMPTY
            ):
                state.player_x = nx
                state.player_y = ny
                return

    state.player_x = state.last_house_x
    state.player_y = state.last_house_y
