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
    from systems.npc import interact_with_npc
    interact_with_npc(GAME_STATE)
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
    plant_tree(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/solar", methods=["POST"])
def api_solar():
    build_solar_panel(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/wind", methods=["POST"])
def api_wind():
    build_wind_turbine(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/house", methods=["POST"])
def api_house():
    build_house(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/farm", methods=["POST"])
def api_farm():
    build_farm(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/exit_house", methods=["POST"])
def api_exit_house():
    exit_house(GAME_STATE)
    return jsonify(get_state_dict())

# -----------------------------
# CROPS
# -----------------------------

@app.route("/api/plant_wheat", methods=["POST"])
def api_plant_wheat():
    plant_wheat(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/plant_carrot", methods=["POST"])
def api_plant_carrot():
    plant_carrot(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/harvest", methods=["POST"])
def api_harvest():
    harvest_crop(GAME_STATE)
    return jsonify(get_state_dict())


# ------------------------------------------------------------
# RUN SERVER
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
