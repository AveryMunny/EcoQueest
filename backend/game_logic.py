import random
from dataclasses import dataclass
import time
START_TIME = time.time()    

# ----- TILE TYPES -----
TILE_EMPTY = "empty"
TILE_TREE = "tree"
TILE_COAL = "coal"
TILE_BERRIES = "berries"
TILE_SAPLING = "sapling"
TILE_SOLAR = "solar"
TILE_WIND = "wind"
TILE_HOUSE = "house"
TILE_RABBIT = "rabbit"
TILE_DEER = "deer"
TILE_BIRD = "bird"
TILE_FARM = "farm"
TILE_WHEAT_1 = "wheat1"  # just planted
TILE_WHEAT_2 = "wheat2"  # growing
TILE_WHEAT_3 = "wheat3"  # ready to harvest

TILE_CARROT_1 = "carrot1" # just planted
TILE_CARROT_2 = "carrot2" # growing
TILE_CARROT_3 = "carrot3"  # ready to harvest


RESOURCE_TYPES = [TILE_TREE, TILE_COAL, TILE_BERRIES]


# Game State Data Class
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
    tiles: list
    crop_growth: dict = None


    # Extras
    turn: int = 0
    in_house: bool = False
    house_tiles: list = None
    house_width: int = 10
    house_height: int = 10
    last_house_x: int = 0
    last_house_y: int = 0
    time_of_day: str = "day" # or "Night"
    current_day: int = 0

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
            "in_house": self.in_house,
            "house_tiles": self.house_tiles,
            "house_width": self.house_width,
            "house_height": self.house_height,
            "time_of_day": self.time_of_day,
            "current_day": self.current_day,

        }


# initialize game state 
def create_initial_state(width: int = 30, height: int = 30) -> GameState:
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            if random.random() < 0.25:
                row.append(random.choice(RESOURCE_TYPES))
            else:
                row.append(TILE_EMPTY)
        tiles.append(row)

    return GameState(
        width=width,
        height=height,
        player_x=width // 2,
        player_y=height // 2,
        ecosystem_health=100,
        energy=0,
        food=0,
        wood=0,
        coal=0,
        tiles=tiles,
        crop_growth={},

    )


# ----- PASSIVE ENERGY -----
def apply_passive_energy(state: GameState):
    # Solar panels give +1 per turn
    for row in state.tiles:
        for tile in row:
            if tile == TILE_SOLAR:
                state.energy += 1

    # Wind turbines give +2 every 3 turns
    if state.turn % 3 == 0:
        for row in state.tiles:
            for tile in row:
                if tile == TILE_WIND:
                    state.energy += 2


# ----- MOVEMENT -----
def move_player(state: GameState, direction: str):
    if state.in_house:
        # Move inside house grid
        dx, dy = 0, 0
        if direction == "up": dy = -1
        elif direction == "down": dy = 1
        elif direction == "left": dx = -1
        elif direction == "right": dx = 1
        else: return

        new_x = state.player_x + dx
        new_y = state.player_y + dy

        if 0 <= new_x < state.house_width and 0 <= new_y < state.house_height:
            state.player_x = new_x
            state.player_y = new_y

        state.turn += 1
        return

    # Move in overworld
    dx, dy = 0, 0
    if direction == "up": dy = -1
    elif direction == "down": dy = 1
    elif direction == "left": dx = -1
    elif direction == "right": dx = 1
    else: return

    new_x = state.player_x + dx
    new_y = state.player_y + dy

    if 0 <= new_x < state.width and 0 <= new_y < state.height:
        state.player_x = new_x
        state.player_y = new_y

    state.turn += 1
    apply_passive_energy(state)
    spawn_wildlife(state)
    despawn_wildlife(state)
    try_enter_house(state)
    grow_crops(state)


def collect_resource(state: GameState):
    if state.in_house:
        return  # No resource collecting indoors yet

    x = state.player_x
    y = state.player_y
    tile_type = state.tiles[y][x]

    if tile_type == TILE_TREE:
        state.wood += 1
        state.ecosystem_health -= 3
    elif tile_type == TILE_COAL:
        state.coal += 1
        state.energy += 3
        state.ecosystem_health -= 8
    elif tile_type == TILE_BERRIES:
        state.food += 1
        state.ecosystem_health += 1
    else:
        return

    state.tiles[y][x] = TILE_EMPTY
    state.ecosystem_health = max(0, min(100, state.ecosystem_health))
    state.turn += 1
    apply_passive_energy(state)
    spawn_wildlife(state)
    despawn_wildlife(state)
    grow_crops(state)
    try_enter_house(state)
    
    
def plant_wheat(state: GameState):
    x, y = state.player_x, state.player_y

    # must be planted on a farm tile
    if state.tiles[y][x] != TILE_FARM:
        return
    
    state.tiles[y][x] = TILE_WHEAT_1
    state.crop_growth[(x, y)] = time.time()


def plant_carrot(state: GameState):
    x, y = state.player_x, state.player_y

    if state.tiles[y][x] != TILE_FARM:
        return

    state.tiles[y][x] = TILE_CARROT_1
    state.crop_growth[(x, y)] = time.time()


def grow_crops(state: GameState):
    # Crops grow based on real time, not turns
    elapsed = time.time() - START_TIME

    for (x, y), grow_start in list(state.crop_growth.items()):
        age_minutes = (elapsed - grow_start) / 60.0  # convert seconds → minutes
        
        tile = state.tiles[y][x]

        # --- Wheat ---
        if tile == TILE_WHEAT_1 and age_minutes >= 3:
            state.tiles[y][x] = TILE_WHEAT_2
        elif tile == TILE_WHEAT_2 and age_minutes >= 6:
            state.tiles[y][x] = TILE_WHEAT_3

        # --- Carrots ---
        elif tile == TILE_CARROT_1 and age_minutes >= 2:
            state.tiles[y][x] = TILE_CARROT_2
        elif tile == TILE_CARROT_2 and age_minutes >= 5:
            state.tiles[y][x] = TILE_CARROT_3

    
def harvest_crop(state: GameState):
    x, y = state.player_x, state.player_y
    tile = state.tiles[y][x]

    # Wheat harvest
    if tile == TILE_WHEAT_3:
        state.food += 3
        state.tiles[y][x] = TILE_FARM
        del state.crop_growth[(x, y)]
        return

    # Carrot harvest
    if tile == TILE_CARROT_3:
        state.food += 2
        state.tiles[y][x] = TILE_FARM
        del state.crop_growth[(x, y)]
        return


# ----- PLANT TREE -----
def plant_tree(state: GameState):
    if state.in_house:
        return

    x = state.player_x
    y = state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return
    if state.wood < 1:
        return

    state.wood -= 1
    state.tiles[y][x] = TILE_SAPLING
    state.ecosystem_health = min(100, state.ecosystem_health + 3)

def build_farm(state: GameState):
    if state.in_house:
        return

    x = state.player_x
    y = state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return

    if state.wood < 2:
        return

    state.wood -= 2
    state.tiles[y][x] = TILE_FARM


# ----- BUILD SOLAR PANEL -----
def build_solar_panel(state: GameState):
    if state.in_house:
        return

    x = state.player_x
    y = state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return
    if state.wood < 2:
        return

    state.wood -= 2
    state.tiles[y][x] = TILE_SOLAR


# ----- BUILD WIND TURBINE -----
def build_wind_turbine(state: GameState):
    if state.in_house:
        return

    x = state.player_x
    y = state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return
    if state.wood < 3:
        return

    state.wood -= 3
    state.tiles[y][x] = TILE_WIND


# ----- BUILD HOUSE -----
def build_house(state: GameState):
    if state.in_house:
        return

    x = state.player_x
    y = state.player_y

    if state.tiles[y][x] != TILE_EMPTY:
        return
    if state.wood < 5:
        return

    state.wood -= 5
    state.tiles[y][x] = TILE_HOUSE

    state.last_house_x = x
    state.last_house_y = y

    if state.house_tiles is None:
        state.house_tiles = []
        for j in range(state.house_height):
            row = []
            for i in range(state.house_width):
                row.append(TILE_EMPTY)
            state.house_tiles.append(row)


# ----- ENTER HOUSE -----
def try_enter_house(state: GameState):
    x = state.player_x
    y = state.player_y

    if state.tiles[y][x] == TILE_HOUSE:
        state.in_house = True
        state.player_x = state.house_width // 2
        state.player_y = state.house_height // 2


# ----- EXIT HOUSE -----
def exit_house(state: GameState):
    if not state.in_house:
        return

    state.in_house = False

    # Try putting player next to house outside
    for dy in [-1, 1, 0]:
        for dx in [-1, 1, 0]:
            nx = state.last_house_x + dx
            ny = state.last_house_y + dy
            if (
                0 <= nx < state.width and
                0 <= ny < state.height and
                state.tiles[ny][nx] == TILE_EMPTY
            ):
                state.player_x = nx
                state.player_y = ny
                return

    # fallback
    state.player_x = state.last_house_x
    state.player_y = state.last_house_y
    

def spawn_wildlife(state: GameState):
    # Only spawn animals if ecosystem is healthy
    if state.ecosystem_health < 70:
        return

    # Small chance each turn
    if random.random() < 0.03:  # 3% chance per turn
        # pick random location
        x = random.randint(0, state.width - 1)
        y = random.randint(0, state.height - 1)

        if state.tiles[y][x] == TILE_EMPTY:
            state.tiles[y][x] = random.choice([TILE_RABBIT, TILE_DEER, TILE_BIRD])

def despawn_wildlife(state: GameState):
    # If ecosystem is suffering, animals leave
    if state.ecosystem_health > 40:
        return

    for y in range(state.height):
        for x in range(state.width):
            if state.tiles[y][x] in [TILE_RABBIT, TILE_DEER, TILE_BIRD]:
                state.tiles[y][x] = TILE_EMPTY



# ----- RESET -----
def reset_state() -> GameState:
    return create_initial_state()
