# systems/buildings.py

from game_state import GameState
from tile_types import (
    TILE_EMPTY,
    TILE_SAPLING,
    TILE_FARM,
    TILE_SOLAR,
    TILE_WIND,
    TILE_HOUSE,
    TILE_WALL,
    TILE_FLOOR,
    TILE_DOOR,
    TILE_BED,
    TILE_TABLE,
    TILE_CHEST,
    TILE_RUG,
)

from systems.inventory import has_items, remove_item
from systems.world import get_current_biome_health, set_current_biome_health


def create_default_house_layout(width: int, height: int):
    layout = [[TILE_FLOOR for _ in range(width)] for _ in range(height)]

    # Surround with walls
    for x in range(width):
        layout[0][x] = TILE_WALL
        layout[height - 1][x] = TILE_WALL
    for y in range(height):
        layout[y][0] = TILE_WALL
        layout[y][width - 1] = TILE_WALL

    # Door at bottom center
    door_x = width // 2
    layout[height - 1][door_x] = TILE_DOOR
    return layout


def ensure_house_tiles(state: GameState):
    if state.house_tiles is None:
        state.house_tiles = create_default_house_layout(state.house_width, state.house_height)
    else:
        # Normalize any legacy "empty" cells inside to floor so interiors get the light floor style
        for y in range(len(state.house_tiles)):
            for x in range(len(state.house_tiles[y])):
                if state.house_tiles[y][x] == TILE_EMPTY:
                    state.house_tiles[y][x] = TILE_FLOOR



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

    ensure_house_tiles(state)
    
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
        ensure_house_tiles(state)
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


# ---------------------------------
# Interior decoration (place/clear)
# ---------------------------------
ALLOWED_FURNITURE = {"bed": TILE_BED, "table": TILE_TABLE, "chest": TILE_CHEST, "rug": TILE_RUG}


def place_furniture(state: GameState, x: int, y: int, item: str):
    if not state.in_house:
        state.dialog_message = "You must be inside the house to place furniture."
        return False

    ensure_house_tiles(state)
    if not (0 <= x < state.house_width and 0 <= y < state.house_height):
        state.dialog_message = "Invalid spot."
        return False

    target = state.house_tiles[y][x]
    if target in (TILE_WALL, TILE_DOOR):
        state.dialog_message = "Can't place on walls or the door."
        return False

    tile = ALLOWED_FURNITURE.get(item)
    if not tile:
        state.dialog_message = f"Unknown furniture: {item}"
        return False

    state.house_tiles[y][x] = tile
    state.dialog_message = f"Placed {item}."
    return True


def clear_furniture(state: GameState, x: int, y: int):
    if not state.in_house:
        state.dialog_message = "You must be inside the house to edit furniture."
        return False

    ensure_house_tiles(state)
    if not (0 <= x < state.house_width and 0 <= y < state.house_height):
        state.dialog_message = "Invalid spot."
        return False

    if state.house_tiles[y][x] in (TILE_WALL, TILE_DOOR):
        state.dialog_message = "Can't remove walls or the door."
        return False

    state.house_tiles[y][x] = TILE_FLOOR
    state.dialog_message = "Cleared."
    return True
