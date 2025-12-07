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
        health -= 3
        changed = True

    elif tile == TILE_COAL:
        add_item(state, "coal", 1)
        state.energy += 3
        health -= 8
        changed = True

    elif tile == TILE_BERRIES:
        add_item(state, "food", 1)
        health += 1
        changed = True

    elif tile == TILE_SNOWY_TREE:
        add_item(state, "wood", 1)
        health -= 3
        changed = True

    elif tile == TILE_FROSTED_BERRIES:
        add_item(state, "food", 1)
        health += 1
        changed = True

    elif tile == TILE_CACTUS:
        add_item(state, "food", 1)
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
        health -= 1
        changed = True

    elif tile == TILE_ICE_CRYSTAL:
        add_item(state, "energy", 2)
        changed = True

    elif tile == TILE_ICEBERG:
        add_item(state, "energy", 3)
        changed = True

    elif tile in (TILE_ROCK, TILE_STONE):
        # for now, just allow generic collection; later tie to pickaxe
        add_item(state, "wood", 1)
        changed = True

    elif tile == TILE_ORE:
        # placeholder for future mining
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
