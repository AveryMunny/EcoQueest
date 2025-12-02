import random
from dataclasses import dataclass, asdict

TILE_EMPTY = "empty"
TILE_TREE = "tree"
TILE_COAL = "coal"
TILE_BERRIES = "berries"    
TILE_SAPLING = "sapling" # for planting trees
TILE_SOLAR = "solar" # for renewable energy
TILE_WIND = "wind" # for renewable energy
TILE_HOUSE = "house" # try to add a house lolllll

RESOURCE_TYPES = [TILE_TREE, TILE_COAL, TILE_BERRIES]


@dataclass
class GameState:
    width: int
    height: int
    player_x: int
    player_y: int
    ecosystem_health: int
    energy: int
    food: int
    wood: int
    coal: int
    tiles: list  # 2D list of tile types (strings)
    turn: int = 0


    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "player_x": self.player_x,
            "player_y": self.player_y,
            "ecosystem_health": self.ecosystem_health,
            "energy": self.energy,
            "food": self.food,
            "wood": self.wood,
            "coal": self.coal,
            "tiles": self.tiles,
        }


def create_initial_state(width: int = 30, height: int = 30) -> GameState:
    # random tiles
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            if random.random() < 0.25:  # ~25% of tiles have resources
                row.append(random.choice(RESOURCE_TYPES))
            else:
                row.append(TILE_EMPTY)
        tiles.append(row)

    # player starts in center
    player_x = width // 2
    player_y = height // 2

    return GameState(
        width=width,
        height=height,
        player_x=player_x,
        player_y=player_y,
        ecosystem_health=100,
        energy=0,
        food=0,
        wood=0,
        coal=0,
        tiles=tiles,
    )


def move_player(state: GameState, direction: str):
    dx, dy = 0, 0
    if direction == "up":
        dy = -1
    elif direction == "down":
        dy = 1
    elif direction == "left":
        dx = -1
    elif direction == "right":
        dx = 1
    else:
        return  # invalid direction

    new_x = state.player_x + dx
    new_y = state.player_y + dy

    # stay in bounds
    if 0 <= new_x < state.width and 0 <= new_y < state.height:
        state.player_x = new_x
        state.player_y = new_y
    
    state.turn += 1
    apply_passive_energy(state)



def collect_resource(state: GameState):
    x = state.player_x
    y = state.player_y
    tile_type = state.tiles[y][x]

    if tile_type == TILE_EMPTY:
        return  # nothing to do

    # sustainability logic
    if tile_type == TILE_TREE:
        state.wood += 1
        state.ecosystem_health -= 3  # cutting trees hurts environment
    elif tile_type == TILE_COAL:
        state.coal += 1
        state.energy += 3
        state.ecosystem_health -= 8  # coal is bad!
    elif tile_type == TILE_BERRIES:
        state.food += 1
        state.ecosystem_health += 1  # sustainable-ish if not overused

    # clear tile
    state.tiles[y][x] = TILE_EMPTY

    # clamp ecosystem health
    state.ecosystem_health = max(0, min(100, state.ecosystem_health))
    
    state.turn += 1
    apply_passive_energy(state)

def build_house(state: GameState):
    x = state.player_x
    y = state.player_y

    # must be empty tile
    if state.tiles[y][x] != TILE_EMPTY:
        return

    # cost: 5 wood
    if state.wood < 5:
        return

    state.wood -= 5
    state.tiles[y][x] = TILE_HOUSE

def reset_state() -> GameState:
    return create_initial_state()

def apply_passive_energy(state: GameState):
    # Solar panels give +1 each turn
    for row in state.tiles:
        for tile in row:
            if tile == TILE_SOLAR:
                state.energy += 1

    # Wind turbines give +2 energy every 3 turns
    if state.turn % 3 == 0:
        for row in state.tiles:
            for tile in row:
                if tile == TILE_WIND:
                    state.energy += 2

def plant_tree(state: GameState):
    x = state.player_x
    y = state.player_y

    # tile must be empty
    if state.tiles[y][x] != TILE_EMPTY:
        return

    # must have at least 1 wood
    if state.wood < 1:
        return

    state.wood -= 1
    state.tiles[y][x] = TILE_SAPLING
    state.ecosystem_health = min(100, state.ecosystem_health + 3)

def build_solar_panel(state: GameState):
    x = state.player_x
    y = state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return

    if state.wood < 2:
        return

    state.wood -= 2
    state.tiles[y][x] = TILE_SOLAR

def build_wind_turbine(state: GameState):
    x = state.player_x
    y = state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return

    if state.wood < 3:
        return

    state.wood -= 3
    state.tiles[y][x] = TILE_WIND

