from flask import Flask, jsonify, request
import os
import time

# ------------------------------------------------------------
# DAY/NIGHT CYCLE SETTINGS
# ------------------------------------------------------------
START_TIME = time.time()
DAY_LENGTH = 5 * 60      # 5 minutes
NIGHT_LENGTH = 5 * 60    # 5 minutes

# import game structure 
from game_state import GameState
from systems.world import create_initial_state, reset_state
from systems.movement import move_player
from systems.collection import collect_resource
from systems.buildings import (
    plant_tree, build_solar_panel, build_wind_turbine,
    build_house, build_farm, exit_house
)
from systems.farming import (
    plant_wheat, plant_carrot, harvest_crop, grow_crops
)
from systems.npc import interact_with_npc, choose_path
from systems.crafting import craft, get_available_recipes
from systems.buildings import place_furniture, clear_furniture, try_enter_house

# create Flask app and configure static folder to serve frontend
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend"),
    static_url_path=""
)

# initialize game state
GAME_STATE: GameState = create_initial_state()

# the time of day cycle creation - will be called before each request to ensure the state is up to date
def update_day_night_cycle(state):
    elapsed = time.time() - START_TIME
    cycle_length = DAY_LENGTH + NIGHT_LENGTH

    cycle_pos = elapsed % cycle_length

    if cycle_pos < DAY_LENGTH:
        state.time_of_day = "day"
    else:
        state.time_of_day = "night"

    state.current_day = int(elapsed // cycle_length)

# ensure day/night cycle is updated before handling any request
@app.before_request
def before_request():
    update_day_night_cycle(GAME_STATE)

# helper function to get current state as dict (with day/night cycle updated)
def get_state_dict():
    update_day_night_cycle(GAME_STATE)
    grow_crops(GAME_STATE)  # always keep crops updating
    return GAME_STATE.to_dict()

# routes for frontend to interact with game state
@app.route("/")
def index():
    return app.send_static_file("index.html") # serve the main frontend page

@app.route("/api/state") 
def api_state():
    return jsonify(get_state_dict()) # return the current game state as JSON, ensuring day/night cycle is updated first


@app.route("/api/move", methods=["POST"])
def api_move():
    direction = request.json.get("direction")
    move_player(GAME_STATE, direction)
    return jsonify(get_state_dict()) # return the updated game state after moving the player

@app.route("/api/interact", methods=["POST"])
def api_interact():
    # First try to interact with/tame nearby animals. If no animal nearby, fall back to NPC dialog.
    from systems.animals import attempt_tame
    result = attempt_tame(GAME_STATE)
    if result is None:
        # no animal nearby — try NPCs
        from systems.npc import interact_with_npc
        interact_with_npc(GAME_STATE)
    # if result is True or False, attempt_tame already set dialog_message
    return jsonify(GAME_STATE.to_dict())


@app.route("/api/enter_house", methods=["POST"])
def api_enter_house():
    GAME_STATE.dialog_message = ""
    try_enter_house(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after trying to enter the house

@app.route("/api/choose_path_eco", methods=["POST"])
def path_eco():
    from systems.npc import choose_path
    choose_path(GAME_STATE, "eco")
    return jsonify(GAME_STATE.to_dict()) # return the updated game state after choosing the eco path

@app.route("/api/choose_path_industry", methods=["POST"])
def path_industry():
    from systems.npc import choose_path
    choose_path(GAME_STATE, "industry")
    return jsonify(GAME_STATE.to_dict()) # return the updated game state after choosing the industry path

@app.route("/api/choose_path_neutral", methods=["POST"])
def path_neutral():
    from systems.npc import choose_path
    choose_path(GAME_STATE, "neutral")
    return jsonify(GAME_STATE.to_dict()) # return the updated game state after choosing the neutral path


@app.route("/api/collect", methods=["POST"])
def api_collect():
    GAME_STATE.dialog_message = ""
    collect_resource(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after collecting resources (or failing to collect)


@app.route("/api/reset", methods=["POST"])
def api_reset():
    global GAME_STATE
    GAME_STATE = reset_state()
    return jsonify(get_state_dict()) # return the reset game state as JSON after resetting the game

# building actions (plant tree, build solar panel, build wind turbine, build house, build farm, exit house)

@app.route("/api/plant", methods=["POST"])
def api_plant():
    GAME_STATE.dialog_message = ""
    plant_tree(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after planting a tree (or failing to plant)


@app.route("/api/solar", methods=["POST"])
def api_solar():
    GAME_STATE.dialog_message = ""
    build_solar_panel(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after building a solar panel (or failing to build)


@app.route("/api/wind", methods=["POST"])
def api_wind():
    GAME_STATE.dialog_message = ""
    build_wind_turbine(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after building a wind turbine (or failing to build)


@app.route("/api/house", methods=["POST"])
def api_house():
    GAME_STATE.dialog_message = ""
    build_house(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after building a house (or failing to build)


@app.route("/api/farm", methods=["POST"])
def api_farm():
    GAME_STATE.dialog_message = ""
    build_farm(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after building a farm (or failing to build)


@app.route("/api/exit_house", methods=["POST"])
def api_exit_house():
    GAME_STATE.dialog_message = ""
    exit_house(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after exiting the house (or failing to exit)

# farming actions (plant wheat, plant carrot, harvest crop)

@app.route("/api/plant_wheat", methods=["POST"])
def api_plant_wheat():
    GAME_STATE.dialog_message = ""
    plant_wheat(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after planting wheat (or failing to plant)


@app.route("/api/plant_carrot", methods=["POST"])
def api_plant_carrot():
    GAME_STATE.dialog_message = ""
    plant_carrot(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after planting carrots (or failing to plant)


@app.route("/api/harvest", methods=["POST"])
def api_harvest():
    GAME_STATE.dialog_message = ""
    harvest_crop(GAME_STATE)
    return jsonify(get_state_dict()) # return the updated game state after harvesting crops (or failing to harvest)

@app.route("/api/choose_path", methods=["POST"])
def api_choose_path():
    data = request.get_json(force=True)
    path = data.get("path")
    choose_path(GAME_STATE, path)
    return jsonify(GAME_STATE.to_dict()) # return the updated game state after choosing a path (eco, industry, or neutral)

@app.route("/api/craft", methods=["POST"])
def api_craft():
    GAME_STATE.dialog_message = ""
    data = request.get_json(force=True)
    recipe_name = data.get("recipe_name")
    craft(GAME_STATE, recipe_name)
    return jsonify(GAME_STATE.to_dict()) # return the updated game state after attempting to craft the specified recipe (or failing to craft)

@app.route("/api/recipes", methods=["GET"])
def api_recipes():
    available = get_available_recipes(GAME_STATE)
    return jsonify({"recipes": available}) # return the list of available recipes based on the current game state (inventory, buildings, etc.)


# house furniture actions (place furniture, clear furniture) - only allowed when player is inside the house

@app.route("/api/house/place", methods=["POST"])
def api_house_place():
    GAME_STATE.dialog_message = ""
    data = request.get_json(force=True)
    x = int(data.get("x", -1))
    y = int(data.get("y", -1))
    item = data.get("item")
    place_furniture(GAME_STATE, x, y, item)
    return jsonify(get_state_dict()) # return the updated game state after attempting to place furniture in the house (or failing to place)


@app.route("/api/house/clear", methods=["POST"])
def api_house_clear():
    GAME_STATE.dialog_message = ""
    data = request.get_json(force=True)
    x = int(data.get("x", -1))
    y = int(data.get("y", -1))
    clear_furniture(GAME_STATE, x, y)
    return jsonify(get_state_dict()) # return the updated game state after attempting to clear furniture from the house (or failing to clear)


# Inventory actions (use / drop)
@app.route("/api/inventory/use", methods=["POST"])
def api_inventory_use():
    data = request.get_json(force=True)
    item = data.get("item")
    amount = int(data.get("amount", 1))
    from systems.inventory import remove_item # need to import to check if player has the item and to remove it when used

    if not item:
        GAME_STATE.dialog_message = "No item specified."
        return jsonify(GAME_STATE.to_dict()) # return current state if no item specified to use

    # Food items restore energy and health
    food_items = {
        "berries": {"energy": 10, "health": 5},
        "frosted_berries": {"energy": 12, "health": 6},
        "wheat": {"energy": 15, "health": 8},
        "carrot": {"energy": 15, "health": 8},
        "fish": {"energy": 20, "health": 12},
        "mushroom": {"energy": 8, "health": 4},
        # crafted utility items
        "meal_pack": {"energy": 40, "health": 20},
        "bedroll": {"energy": 0, "health": 30},
    }

    # Check if the item is a food item that provides energy/health restoration
    # If it is, apply the energy/health gain when used. Otherwise, just remove the item without any stat changes.
    if item in food_items:
        ok = remove_item(GAME_STATE, item, amount)
        if ok:
            restore = food_items[item]
            energy_gain = restore["energy"] * amount
            health_gain = restore["health"] * amount
            
            GAME_STATE.energy = min(100, GAME_STATE.energy + energy_gain)
            GAME_STATE.player_health = min(100, GAME_STATE.player_health + health_gain)
            
            GAME_STATE.dialog_message = f"Ate {amount} x {item}. +{energy_gain} Energy, +{health_gain} Health!"
        else:
            GAME_STATE.dialog_message = f"You don't have {amount} x {item}."
    else:
        ok = remove_item(GAME_STATE, item, amount)
        if ok:
            GAME_STATE.dialog_message = f"Used {amount} x {item}."
        else:
            GAME_STATE.dialog_message = f"You don't have {amount} x {item} to use."

    return jsonify(GAME_STATE.to_dict())


@app.route("/api/inventory/drop", methods=["POST"])
def api_inventory_drop():
    data = request.get_json(force=True)
    item = data.get("item")
    amount = int(data.get("amount", 1))
    from systems.inventory import remove_item

    if not item:
        GAME_STATE.dialog_message = "No item specified to drop."
        return jsonify(GAME_STATE.to_dict())

    ok = remove_item(GAME_STATE, item, amount)
    if ok:
        GAME_STATE.dialog_message = f"Dropped {amount} x {item}."
    else:
        GAME_STATE.dialog_message = f"You don't have {amount} x {item} to drop."

    return jsonify(GAME_STATE.to_dict())


# run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
