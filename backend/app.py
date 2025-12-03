from flask import Flask, jsonify, request, send_from_directory
import time
START_TIME = time.time()
DAY_LENGTH = 5 * 60   # 5 minutes
NIGHT_LENGTH = 5 * 60  # 5 minutes

from game_logic import (
    GameState,
    create_initial_state,
    move_player,
    collect_resource,
    reset_state,
    plant_tree,
    build_solar_panel,
    build_wind_turbine,
    build_house,
    build_farm,
    try_enter_house, 
    exit_house,
    plant_wheat, 
    plant_carrot, 
    harvest_crop,
    grow_crops,
)


import os

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend"),
    static_url_path="",
)

# single global game state (fine for local single-player)
GAME_STATE: GameState = create_initial_state()

def update_day_night_cycle(state):
    elapsed = time.time() - START_TIME
    cycle_length = DAY_LENGTH + NIGHT_LENGTH

    # Determine which cycle we are in
    cycle_pos = elapsed % cycle_length

    # Day
    if cycle_pos < DAY_LENGTH:
        state.time_of_day = "day"
    else:
        state.time_of_day = "night"

    # Count how many full day/night cycles have passed
    state.current_day = int(elapsed // cycle_length)
    
@app.before_request
def before_request():
    update_day_night_cycle(GAME_STATE)  

def get_state_dict():
    update_day_night_cycle(GAME_STATE)
    grow_crops(GAME_STATE)
    return GAME_STATE.to_dict()


@app.route("/")
def index():
    # serve frontend
    return app.send_static_file("index.html")


@app.route("/api/exit_house", methods=["POST"])
def api_exit_house():
    exit_house(GAME_STATE)
    return jsonify(get_state_dict())

@app.route("/api/state", methods=["GET"])
def api_state():
    return jsonify(get_state_dict())



@app.route("/api/move", methods=["POST"])
def api_move():
    data = request.get_json(force=True)
    direction = data.get("direction")
    move_player(GAME_STATE, direction)
    return jsonify(get_state_dict())


@app.route("/api/collect", methods=["POST"])
def api_collect():
    collect_resource(GAME_STATE)
    return jsonify(get_state_dict())


@app.route("/api/reset", methods=["POST"])
def api_reset():
    global GAME_STATE
    GAME_STATE = reset_state()
    return jsonify(get_state_dict())

@app.route("/api/plant", methods=["POST"])
def api_plant():
    plant_tree(GAME_STATE)
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/solar", methods=["POST"])
def api_solar():
    build_solar_panel(GAME_STATE)
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/wind", methods=["POST"])
def api_wind():
    build_wind_turbine(GAME_STATE)
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/house", methods=["POST"])
def api_house():
    build_house(GAME_STATE)
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/plant_wheat", methods=["POST"])
def api_plant_wheat():
    plant_wheat(GAME_STATE)
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/plant_carrot", methods=["POST"])
def api_plant_carrot():
    plant_carrot(GAME_STATE)
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/harvest", methods=["POST"])
def api_harvest():
    harvest_crop(GAME_STATE)
    return jsonify(GAME_STATE.to_dict())

@app.route("/api/farm", methods=["POST"])
def api_farm():
    build_farm(GAME_STATE)
    return jsonify(GAME_STATE.to_dict())


if __name__ == "__main__":
    # run: python app.py
    app.run(debug=True)
