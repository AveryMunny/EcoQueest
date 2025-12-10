# systems/npc.py
from tile_types import TILE_NPC_FOREST_GUIDE, TILE_NPC_DESERT_MERCHANT, TILE_EMPTY
from systems.inventory import add_item, has_items, remove_item
from game_state import GameState

def interact_with_npc(state):
    x, y = state.player_x, state.player_y

    # Player must stand ON or NEXT TO NPC to interact
    nearby = [
        (x, y),
        (x+1, y), (x-1, y),
        (x, y+1), (x, y-1)
    ]

    npc_type = None
    for nx, ny in nearby:
        if 0 <= nx < state.width and 0 <= ny < state.height:
            tile = state.tiles[ny][nx]
            if tile == TILE_NPC_FOREST_GUIDE:
                npc_type = "forest_guide"
                break
            elif tile == TILE_NPC_DESERT_MERCHANT:
                npc_type = "desert_merchant"
                break

    if not npc_type:
        state.dialog_message = "No one is nearby to talk to."
        return
    
    # Handle specific NPC
    if npc_type == "forest_guide":
        interact_forest_guide(state)
    elif npc_type == "desert_merchant":
        interact_desert_merchant(state)


def interact_forest_guide(state):
    # Waiting for path choice?
    if state.awaiting_path_choice:
        state.dialog_message = "Choose a path using 1, 2, or 3."
        return

    # No path chosen yet: prompt the player
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

    # Already chosen a path
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


def interact_desert_merchant(state):
    if state.active_quests is None:
        state.active_quests = {}
    
    quest_name = "desert_trader"
    
    # Check if quest is already completed
    if quest_name in state.active_quests and state.active_quests[quest_name]["status"] == "completed":
        state.dialog_message = (
            "🧑‍💼 Desert Merchant:\n"
            "\"Thank you again for the cactus fiber!\n"
            "May your travels be prosperous.\""
        )
        return
    
    # Check if quest is active and player has items
    if quest_name in state.active_quests and state.active_quests[quest_name]["status"] == "active":
        # Check if player has 5 fiber
        if has_items(state, fiber=5):
            # Complete quest - give reward
            remove_item(state, "fiber", 5)
            add_item(state, "quartz", 3)
            add_item(state, "energy", 10)
            state.active_quests[quest_name]["status"] = "completed"
            state.dialog_message = (
                "🧑‍💼 Desert Merchant:\n"
                "\"Excellent! This fiber is perfect!\n"
                "Here's your reward: 3 Quartz and 10 Energy.\"\n\n"
                "✅ Quest Complete!"
            )
        else:
            current = state.inventory.get("fiber", 0)
            state.dialog_message = (
                f"🧑‍💼 Desert Merchant:\n"
                f"\"Bring me 5 cactus fiber, and I'll reward you well.\n"
                f"You have {current}/5 fiber.\""
            )
        return
    
    # First interaction - give quest
    state.active_quests[quest_name] = {
        "status": "active",
        "description": "Bring 5 cactus fiber to the Desert Merchant"
    }
    state.dialog_message = (
        "🧑‍💼 Desert Merchant:\n"
        "\"Greetings, traveler! I trade in rare goods.\n"
        "If you bring me 5 cactus fiber,\n"
        "I'll give you valuable quartz and energy.\"\n\n"
        "📜 New Quest: Desert Trader\n"
        "Collect 5 fiber from cacti."
    )


def choose_path(state, path):
    state.player_path = path
    state.awaiting_path_choice = False
    
    # Set bonuses based on path
    if path == "eco":
        state.eco_bonuses = True
        state.industry_bonuses = False
        state.inventory["mushroom"] += 3
    elif path == "industry":
        state.eco_bonuses = False
        state.industry_bonuses = True
        state.inventory["coal"] += 3
    else:
        state.eco_bonuses = False
        state.industry_bonuses = False
        state.inventory["fiber"] += 3
    
    # Clear dialog message immediately
    state.dialog_message = ""

    # remove the NPC from the map
    for y in range(state.height):
        for x in range(state.width):
            if state.tiles[y][x] == TILE_NPC_FOREST_GUIDE:
                state.tiles[y][x] = TILE_EMPTY