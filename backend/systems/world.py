# systems/world.py
import random
import time

from game_state import GameState
from tile_types import (
    TILE_EMPTY,
    TILE_TREE,
    TILE_COAL,
    TILE_BERRIES,
)

from biomes.biome_forest import generate_forest
from biomes.biome_tundra import generate_tundra
from biomes.biome_desert import generate_desert
from biomes.biome_coastal import generate_coastal
from biomes.biome_swamp import generate_swamp
from biomes.biome_mountains import generate_mountain
from systems.animals import move_animals


START_TIME = time.time()

BIOME_GENERATORS = {
    "forest": generate_forest,
    "tundra": generate_tundra,
    "desert": generate_desert,
    "coastal": generate_coastal,
    "swamp": generate_swamp,
    "mountain": generate_mountain,
}

WORLD_MAP = {
    (0, 0): "forest",
    (0, -1): "tundra",
    (0, -2): "mountain",
    (0, 1): "swamp",
    (1, 0): "desert",
    (2, 0): "coastal",
    (-1, 0): "forest",
}


def get_current_biome_health(state: GameState) -> int:
    if not state.biome_health:
        return state.ecosystem_health
    return state.biome_health.get(state.current_biome, 100)


def set_current_biome_health(state: GameState, value: int):
    clamped = max(0, min(100, value))
    if state.biome_health is None:
        state.biome_health = {}
    state.biome_health[state.current_biome] = clamped
    state.ecosystem_health = clamped


def create_initial_state(width: int = 30, height: int = 30) -> GameState:
    # You can swap this to biome-based start (forest generator) later
    tiles = generate_forest(width, height)

    state = GameState(
        width=width,
        height=height,
        player_x=width // 2,
        player_y=height // 2,
        tiles=tiles,
        crop_growth={},
        biome_health={
            "forest": 100,
            "tundra": 100,
            "mountain": 100,
            "swamp": 100,
            "desert": 100,
            "coastal": 100,
        },
        biome_states={},
        
        inventory={
            "wood": 0,
            "stone": 0,
            "coal": 0,
            "berries": 0,
            "frosted_berries": 0,
            "wheat": 0,
            "carrot": 0,
            "fish": 0,
            "fiber": 0,
            "peat": 0,
            "mushroom": 0,
            "ice_shard": 0,
            "crystal_shard": 0,
            "ore_chunk": 0,

            # tools
            "axe": 0,
            "pickaxe": 0,
            "shovel": 0,
        },

    )
    state.ecosystem_health = get_current_biome_health(state)
    return state


def reset_state() -> GameState:
    return create_initial_state()


def get_or_create_biome_state(state: GameState, biome_name: str):
    if state.biome_states is None:
        state.biome_states = {}

    if biome_name in state.biome_states:
        return state.biome_states[biome_name]

    tiles = BIOME_GENERATORS[biome_name](state.width, state.height)
    biome_state = {
        "tiles": tiles,
        "crop_growth": {},
        "last_house_x": None,
        "last_house_y": None,
        "house_tiles": None,
    }

    state.biome_states[biome_name] = biome_state
    return biome_state


def switch_biome(state: GameState, biome_name: str):
    # Save current biome
    current = state.current_biome

    if state.biome_states is None:
        state.biome_states = {}

    # sync current biome's tiles etc.
    if current not in state.biome_states:
        state.biome_states[current] = {}

    state.biome_states[current]["tiles"] = state.tiles
    state.biome_states[current]["crop_growth"] = state.crop_growth
    state.biome_states[current]["last_house_x"] = state.last_house_x
    state.biome_states[current]["last_house_y"] = state.last_house_y
    state.biome_states[current]["house_tiles"] = state.house_tiles

    # Load new biome
    new_biome_state = get_or_create_biome_state(state, biome_name)

    state.tiles = new_biome_state["tiles"]
    state.crop_growth = new_biome_state["crop_growth"]
    state.last_house_x = new_biome_state["last_house_x"]
    state.last_house_y = new_biome_state["last_house_y"]
    state.house_tiles = new_biome_state["house_tiles"]

    state.current_biome = biome_name
    state.player_x = state.width // 2
    state.player_y = state.height // 2

    # Update HUD health
    state.ecosystem_health = get_current_biome_health(state)
