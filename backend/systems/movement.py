# systems/movement.py
from game_state import GameState
from systems.world import WORLD_MAP, switch_biome
from systems.energy import apply_passive_energy, passive_energy_drain, drain_energy
from systems.wildlife import spawn_wildlife, despawn_wildlife
from systems.buildings import try_enter_house
from systems.farming import grow_crops
from systems.animals import move_animals


def move_player(state: GameState, direction: str):
    # Movement in house
    if state.in_house:
        dx = dy = 0
        if direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        elif direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1

        nx = state.player_x + dx
        ny = state.player_y + dy

        if 0 <= nx < state.house_width and 0 <= ny < state.house_height:
            state.player_x = nx
            state.player_y = ny

        state.turn += 1
        return

    # Overworld
    dx = dy = 0
    if direction == "up":
        dy = -1
    elif direction == "down":
        dy = 1
    elif direction == "left":
        dx = -1
    elif direction == "right":
        dx = 1

    nx = state.player_x + dx
    ny = state.player_y + dy

    if 0 <= nx < state.width and 0 <= ny < state.height:
        state.player_x = nx
        state.player_y = ny
    else:
        new_world_pos = (state.world_x + dx, state.world_y + dy)
        if new_world_pos in WORLD_MAP:
            state.world_x, state.world_y = new_world_pos
            biome_name = WORLD_MAP[new_world_pos]
            switch_biome(state, biome_name)
        else:
            return

    state.turn += 1
    passive_energy_drain(state)  # Drain energy over time
    apply_passive_energy(state)  # Gain energy from solar/wind
    spawn_wildlife(state)
    despawn_wildlife(state)
    try_enter_house(state)
    grow_crops(state)
    move_animals(state)
