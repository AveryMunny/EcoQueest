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


def drain_energy(state: GameState, amount: int = 1):
    """Drain energy and damage health if energy is depleted."""
    state.energy -= amount
    
    # If energy goes below 0, start damaging health
    if state.energy < 0:
        health_damage = abs(state.energy)  # Convert negative energy to health damage
        state.player_health = max(0, state.player_health - health_damage)
        state.energy = 0  # Keep energy at 0, not negative
        
        if state.player_health <= 0:
            state.dialog_message = "💀 You've collapsed from exhaustion! Eat food to recover."


def passive_energy_drain(state: GameState):
    """Drain energy every few turns from just existing."""
    # Drain 1 energy every 3 turns
    if state.turn % 3 == 0:
        drain_energy(state, 1)
