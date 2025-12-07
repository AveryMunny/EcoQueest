# systems/npc.py
from tile_types import TILE_NPC_FOREST_GUIDE
from systems.inventory import add_item

def interact_with_npc(state):
    x, y = state.player_x, state.player_y

    # Player must stand ON or NEXT TO NPC to interact
    nearby = [
        (x, y),
        (x+1, y), (x-1, y),
        (x, y+1), (x, y-1)
    ]

    npc_found = False
    for nx, ny in nearby:
        if 0 <= nx < state.width and 0 <= ny < state.height:
            if state.tiles[ny][nx] == TILE_NPC_FOREST_GUIDE:
                npc_found = True
                break

    if not npc_found:
        state.dialog_message = "No one is nearby to talk to."
        return

    # If player has not chosen a path yet:
    if state.player_path is None:
        state.dialog_message = (
            "🧑‍🌾 Forest Guide:\n"
            "\"Welcome, traveler. The world is changing.\n"
            "What path will you walk?\"\n\n"
            "Press 1 — 🌱 Eco-Guardian\n"
            "Press 2 — 💼 Industrial Entrepreneur\n"
            "Press 3 — ⚪ Wanderer (Neutral)\""
        )
        state.awaiting_path_choice = True
        return

    # If already chosen
    if state.player_path == "eco":
        state.dialog_message = (
            "🧑‍🌾 Forest Guide:\n"
            "\"Protect the land, and it will protect you.\""
        )
    elif state.player_path == "industry":
        state.dialog_message = (
            "🧑‍🌾 Forest Guide:\n"
            "\"Prosperity is yours, if you're willing to shape the land.\""
        )
    else:
        state.dialog_message = (
            "🧑‍🌾 Forest Guide:\n"
            "\"Walk your own path, traveler.\""
        )
