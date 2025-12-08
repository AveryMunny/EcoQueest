# systems/collection.py
from game_state import GameState
from tile_types import (
    TILE_EMPTY,
    TILE_TREE, TILE_COAL, TILE_BERRIES,
    TILE_SNOWY_TREE, TILE_FROSTED_BERRIES,
    TILE_CACTUS, TILE_SANDSTONE, TILE_QUARTZ,
    TILE_REEDS, TILE_MUSHROOM, TILE_PEAT,
    TILE_ICE_CRYSTAL, TILE_ICEBERG,
    TILE_ROCK, TILE_STONE, TILE_ORE,
)
from systems.world import get_current_biome_health, set_current_biome_health
from systems.energy import apply_passive_energy
from systems.farming import grow_crops
from systems.buildings import try_enter_house
from systems.wildlife import spawn_wildlife, despawn_wildlife
from systems.inventory import add_item


def collect_resource(state: GameState):
    if state.in_house:
        return

    x, y = state.player_x, state.player_y
    tile = state.tiles[y][x]

    health = get_current_biome_health(state)
    changed = False

    if tile == TILE_TREE:
        add_item(state, "wood", 1)
        # Eco-Guardians cause less ecosystem decay
        health_loss = 2 if state.eco_bonuses else 3
        health -= health_loss
        changed = True

    elif tile == TILE_COAL:
        add_item(state, "coal", 1)
        state.energy += 3
        # Eco-Guardians cause less ecosystem decay
        health_loss = 6 if state.eco_bonuses else 8
        health -= health_loss
        changed = True

    elif tile == TILE_BERRIES:
        # Eco-Guardians get +1 extra food
        food_gain = 2 if state.eco_bonuses else 1
        add_item(state, "food", food_gain)
        health += 1
        changed = True

    elif tile == TILE_SNOWY_TREE:
        add_item(state, "wood", 1)
        # Eco-Guardians cause less ecosystem decay
        health_loss = 2 if state.eco_bonuses else 3
        health -= health_loss
        changed = True

    elif tile == TILE_FROSTED_BERRIES:
        # Eco-Guardians get +1 extra food
        food_gain = 2 if state.eco_bonuses else 1
        add_item(state, "food", food_gain)
        health += 1
        changed = True

    elif tile == TILE_CACTUS:
        # Eco-Guardians get +1 extra food
        food_gain = 2 if state.eco_bonuses else 1
        add_item(state, "food", food_gain)
        health += 1
        changed = True

    elif tile == TILE_SANDSTONE:
        add_item(state, "wood", 1)
        changed = True

    elif tile == TILE_QUARTZ:
        add_item(state, "energy", 1)
        changed = True

    elif tile == TILE_REEDS:
        add_item(state, "wood", 1)
        health += 1
        changed = True

    elif tile == TILE_MUSHROOM:
        add_item(state, "food", 1)
        health += 1
        changed = True

    elif tile == TILE_PEAT:
        add_item(state, "energy", 1)
        # Eco-Guardians cause less ecosystem decay
        health_loss = 1 if state.eco_bonuses else 1
        health -= health_loss
        changed = True

    elif tile == TILE_ICE_CRYSTAL:
        add_item(state, "energy", 2)
        changed = True

    elif tile == TILE_ICEBERG:
        add_item(state, "energy", 3)
        changed = True

    elif tile in (TILE_ROCK, TILE_STONE):
        # Industrialists get double stone/ore
        stone_gain = 2 if state.industry_bonuses else 1
        add_item(state, "stone", stone_gain)
        changed = True

    elif tile == TILE_ORE:
        # Industrialists get double ore
        ore_gain = 2 if state.industry_bonuses else 1
        add_item(state, "ore_chunk", ore_gain)
        changed = True

    else:
        return

    if changed:
        state.tiles[y][x] = TILE_EMPTY
        set_current_biome_health(state, health)
        state.turn += 1
        apply_passive_energy(state)
        spawn_wildlife(state)
        despawn_wildlife(state)
        grow_crops(state)
        try_enter_house(state)
