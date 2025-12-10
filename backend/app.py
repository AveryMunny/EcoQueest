from flask import Flask, jsonify, request
import os
import time

# ------------------------------------------------------------
# DAY/NIGHT CYCLE SETTINGS
# ------------------------------------------------------------
START_TIME = time.time()
DAY_LENGTH = 5 * 60      # 5 minutes
NIGHT_LENGTH = 5 * 60    # 5 minutes

# ------------------------------------------------------------
# IMPORT GAME SYSTEMS (NEW MODULAR STRUCTURE)
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# CREATE FLASK APP (serving frontend folder)
# ------------------------------------------------------------
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend"),
    static_url_path=""
)

# ------------------------------------------------------------
# GLOBAL GAME STATE – SINGLE PLAYER
# ------------------------------------------------------------
GAME_STATE: GameState = create_initial_state()

# ------------------------------------------------------------
# TIME OF DAY SYSTEM
# ------------------------------------------------------------
def update_day_night_cycle(state):
    elapsed = time.time() - START_TIME
    cycle_length = DAY_LENGTH + NIGHT_LENGTH

    cycle_pos = elapsed % cycle_length

    if cycle_pos < DAY_LENGTH:
        state.time_of_day = "day"
    else:
        state.time_of_day = "night"

    state.current_day = int(elapsed // cycle_length)


@app.before_request
def before_request():
    update_day_night_cycle(GAME_STATE)


def get_state_dict():
    update_day_night_cycle(GAME_STATE)
    grow_crops(GAME_STATE)  # always keep crops updating
    return GAME_STATE.to_dict()

# ------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/state")
def api_state():
    return jsonify(get_state_dict())


@app.route("/api/move", methods=["POST"])
def api_move():
    direction = request.json.get("direction")
    move_player(GAME_STATE, direction)
    return jsonify(get_state_dict())

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

@app.route("/api/choose_path_eco", methods=["POST"])
def path_eco():
    from systems.npc import choose_path
    choose_path(GAME_STATE, "eco")
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/choose_path_industry", methods=["POST"])
def path_industry():
    from systems.npc import choose_path
    choose_path(GAME_STATE, "industry")
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/choose_path_neutral", methods=["POST"])
def path_neutral():
    from systems.npc import choose_path
    choose_path(GAME_STATE, "neutral")
    return jsonify(GAME_STATE.to_dict())    


@app.route("/api/collect", methods=["POST"])
def api_collect():
    GAME_STATE.dialog_message = ""
    collect_resource(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/reset", methods=["POST"])
def api_reset():
    global GAME_STATE
    GAME_STATE = reset_state()
    return jsonify(get_state_dict())

# -----------------------------
# BUILDING & FARMING ENDPOINTS
# -----------------------------

@app.route("/api/plant", methods=["POST"])
def api_plant():
    GAME_STATE.dialog_message = ""
    plant_tree(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/solar", methods=["POST"])
def api_solar():
    GAME_STATE.dialog_message = ""
    build_solar_panel(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/wind", methods=["POST"])
def api_wind():
    GAME_STATE.dialog_message = ""
    build_wind_turbine(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/house", methods=["POST"])
def api_house():
    GAME_STATE.dialog_message = ""
    build_house(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/farm", methods=["POST"])
def api_farm():
    GAME_STATE.dialog_message = ""
    build_farm(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/exit_house", methods=["POST"])
def api_exit_house():
    GAME_STATE.dialog_message = ""
    exit_house(GAME_STATE)
    return jsonify(get_state_dict())

# -----------------------------
# CROPS
# -----------------------------

@app.route("/api/plant_wheat", methods=["POST"])
def api_plant_wheat():
    GAME_STATE.dialog_message = ""
    plant_wheat(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/plant_carrot", methods=["POST"])
def api_plant_carrot():
    GAME_STATE.dialog_message = ""
    plant_carrot(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/harvest", methods=["POST"])
def api_harvest():
    GAME_STATE.dialog_message = ""
    harvest_crop(GAME_STATE)
    return jsonify(get_state_dict())

@app.route("/api/choose_path", methods=["POST"])
def api_choose_path():
    data = request.get_json(force=True)
    path = data.get("path")
    choose_path(GAME_STATE, path)
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/craft", methods=["POST"])
def api_craft():
    GAME_STATE.dialog_message = ""
    data = request.get_json(force=True)
    recipe_name = data.get("recipe_name")
    craft(GAME_STATE, recipe_name)
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/recipes", methods=["GET"])
def api_recipes():
    available = get_available_recipes(GAME_STATE)
    return jsonify({"recipes": available})



# ------------------------------------------------------------
# RUN SERVER
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
