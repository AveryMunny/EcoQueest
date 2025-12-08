# systems/energy.py
from game_state import GameState
from tile_types import TILE_SOLAR, TILE_WIND

def apply_passive_energy(state: GameState):
    # solar every turn (Industrialists get +1)
    solar_bonus = 1 if state.industry_bonuses else 0
    for row in state.tiles:
        for tile in row:
            if tile == TILE_SOLAR:
                state.energy += 1 + solar_bonus

    # wind every 3 turns (Industrialists get +1)
    wind_bonus = 1 if state.industry_bonuses else 0
    if state.turn % 3 == 0:
        for row in state.tiles:
            for tile in row:
                if tile == TILE_WIND:
                    state.energy += 2 + wind_bonus
