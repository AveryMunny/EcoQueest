# systems/energy.py
from game_state import GameState
from tile_types import TILE_SOLAR, TILE_WIND

def apply_passive_energy(state: GameState):
    # solar every turn
    for row in state.tiles:
        for tile in row:
            if tile == TILE_SOLAR:
                state.energy += 1

    # wind every 3 turns
    if state.turn % 3 == 0:
        for row in state.tiles:
            for tile in row:
                if tile == TILE_WIND:
                    state.energy += 2
