# systems/collection.py
import random
from game_state import GameState
from tile_types import (
    TILE_EMPTY,
    TILE_TREE, TILE_COAL, TILE_BERRIES,
    TILE_SNOWY_TREE, TILE_FROSTED_BERRIES,
    TILE_CACTUS, TILE_SANDSTONE, TILE_QUARTZ, TILE_OASIS,
    TILE_REEDS, TILE_MUSHROOM, TILE_PEAT,
    TILE_ICE_CRYSTAL, TILE_ICEBERG, TILE_SNOWFLAKE,
    TILE_ROCK, TILE_STONE, TILE_ORE, TILE_SNOW_ROCK, TILE_CRYSTAL,
    TILE_OCEAN, TILE_SWAMP_WATER, TILE_SHELL, TILE_CRAB,
)
from systems.world import get_current_biome_health, set_current_biome_health
from systems.energy import apply_passive_energy, passive_energy_drain, drain_energy
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
    # Most resources disappear once harvested. A few (open water) are
    # effectively infinite, so they stay on the map after fishing.
    remove_tile = True

    if tile == TILE_TREE:
        add_item(state, "wood", 1)
        # 25% chance to drop a sapling
        if random.random() < 0.25:
            add_item(state, "sapling", 1)
        # Eco-Guardians cause less ecosystem decay
        health_loss = 2 if state.eco_bonuses else 3
        health -= health_loss
        changed = True

    elif tile == TILE_COAL:
        add_item(state, "coal", 1)
        state.energy = min(100, state.energy + 3)
        # Eco-Guardians cause less ecosystem decay
        health_loss = 6 if state.eco_bonuses else 8
        health -= health_loss
        changed = True

    elif tile == TILE_BERRIES:
        # Eco-Guardians get +1 extra berries
        berry_gain = 2 if state.eco_bonuses else 1
        add_item(state, "berries", berry_gain)
        health += 1
        changed = True

    elif tile == TILE_SNOWY_TREE:
        add_item(state, "wood", 1)
        # 25% chance to drop a sapling
        if random.random() < 0.25:
            add_item(state, "sapling", 1)
        # Eco-Guardians cause less ecosystem decay
        health_loss = 2 if state.eco_bonuses else 3
        health -= health_loss
        changed = True

    elif tile == TILE_FROSTED_BERRIES:
        # Eco-Guardians get +1 extra frosted berries
        berry_gain = 2 if state.eco_bonuses else 1
        add_item(state, "frosted_berries", berry_gain)
        health += 1
        changed = True

    elif tile == TILE_CACTUS:
        # Cactus yields fiber
        add_item(state, "fiber", 1)
        health += 1
        changed = True

    elif tile == TILE_SANDSTONE:
        add_item(state, "wood", 1)
        changed = True

    elif tile == TILE_OASIS:
        # A drink at the oasis: restores energy and a little health,
        # and is gentle on the ecosystem.
        state.energy = min(100, state.energy + 5)
        health += 2
        changed = True

    elif tile == TILE_QUARTZ:
        # FIX: used to call add_item(state, "energy", 1), which only ever
        # created a useless "energy" inventory entry instead of giving the
        # player real quartz (the desert quest already rewards "quartz",
        # so this now matches that item name).
        add_item(state, "quartz", 1)
        changed = True

    elif tile == TILE_REEDS:
        # FIX: tile_types.py documents fiber as coming from reeds, but this
        # was granting "wood" instead. Reeds now give fiber as intended.
        add_item(state, "fiber", 1)
        health += 1
        changed = True

    elif tile == TILE_MUSHROOM:
        add_item(state, "mushroom", 1)
        health += 1
        changed = True

    elif tile == TILE_PEAT:
        # FIX: used to call add_item(state, "energy", 1) (a no-op inventory
        # item) instead of the already-initialized "peat" item.
        add_item(state, "peat", 1)
        # FIX: this used to be `1 if state.eco_bonuses else 1`, which always
        # evaluated to 1 no matter what -- Eco-Guardians got no benefit at
        # all despite the comment. They now take no ecosystem damage here.
        health_loss = 0 if state.eco_bonuses else 1
        health -= health_loss
        changed = True

    elif tile == TILE_ICE_CRYSTAL:
        # FIX: used to call add_item(state, "energy", 2). Now feeds the
        # "ice_shard" inventory slot that was initialized but never filled.
        add_item(state, "ice_shard", 2)
        changed = True

    elif tile == TILE_SNOWFLAKE:
        # FIX: tundra generated snowflakes and labeled them "collectible",
        # but nothing here ever handled them. Small ice_shard reward.
        add_item(state, "ice_shard", 1)
        health += 1
        changed = True

    elif tile == TILE_ICEBERG:
        # FIX: used to call add_item(state, "energy", 3). Icebergs are now
        # also actually generated in the tundra biome (see biome_tundra.py)
        # so this code path is reachable.
        add_item(state, "ice_shard", 3)
        changed = True

    elif tile in (TILE_ROCK, TILE_STONE, TILE_SNOW_ROCK):
        # FIX: TILE_SNOW_ROCK (the high-elevation mountain variant of stone)
        # was missing from this check entirely, so it was never collectible.
        # Industrialists get double stone.
        stone_gain = 2 if state.industry_bonuses else 1
        add_item(state, "stone", stone_gain)
        changed = True

    elif tile == TILE_CRYSTAL:
        # FIX: mountain crystals generated but had no collection handler.
        # Feeds the "crystal_shard" slot that was initialized but unused.
        add_item(state, "crystal_shard", 1)
        changed = True

    elif tile == TILE_ORE:
        # Industrialists get double ore
        ore_gain = 2 if state.industry_bonuses else 1
        add_item(state, "ore_chunk", ore_gain)
        changed = True

    elif tile == TILE_SHELL:
        # FIX: shells generated on coastal beaches but had no handler.
        add_item(state, "shell", 1)
        health += 1
        changed = True

    elif tile == TILE_CRAB:
        # FIX: crabs generated on the coast but had no handler.
        add_item(state, "fish", 1)
        changed = True

    elif tile == TILE_OCEAN or tile == TILE_SWAMP_WATER:
        # Collect fish from water tiles without removing the tile.
        # FIX: the comment already said "without removing the tile", but
        # the shared `changed` flag below always cleared it anyway. Water
        # tiles now actually stay on the map after fishing.
        add_item(state, "fish", 1)
        changed = True
        remove_tile = False

    else:
        return

    if changed:
        if remove_tile:
            state.tiles[y][x] = TILE_EMPTY
        set_current_biome_health(state, health)
        state.turn += 1
        drain_energy(state, 2)  # Harvesting costs 2 energy
        passive_energy_drain(state)
        apply_passive_energy(state)
        spawn_wildlife(state)
        despawn_wildlife(state)
        grow_crops(state)
        try_enter_house(state)