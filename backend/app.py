from flask import Flask, jsonify, request, send_from_directory
from game_logic import (
    GameState,
    create_initial_state,
    move_player,
    collect_resource,
    reset_state,
    plant_tree,
    build_solar_panel,
    build_wind_turbine,
    build_house
)


import os

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend"),
    static_url_path="",
)

# single global game state (fine for local single-player)
GAME_STATE: GameState = create_initial_state()


def get_state_dict():
    return GAME_STATE.to_dict()


@app.route("/")
def index():
    # serve frontend
    return app.send_static_file("index.html")


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



if __name__ == "__main__":
    # run: python app.py
    app.run(debug=True)
