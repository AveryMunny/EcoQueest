import random
from dataclasses import dataclass
import time
from tile_types import *

START_TIME = time.time()

# BIOME GENERATORS
from biomes.biome_forest import generate_forest
from biomes.biome_tundra import generate_tundra
from biomes.biome_desert import generate_desert
from biomes.biome_swamp import generate_swamp
from biomes.biome_mountains import generate_mountain

BIOME_GENERATORS = {
    "forest": generate_forest,
    "tundra": generate_tundra,
    "desert": generate_desert,
    "swamp": generate_swamp,
    "mountain": generate_mountain,
}

# WORLD GRID MAP
WORLD_MAP = {
    (0, 0): "forest",
    (0, -1): "tundra",
    (0, -2): "mountain",
    (0, 1): "swamp",
    (1, 0): "desert",
    (-1, 0): "forest",
}


# -------------------------------
# PER-BIOME HEALTH HELPERS
# -------------------------------
def get_current_biome_health(state):
    return state.biome_health.get(state.current_biome, 100)


def set_current_biome_health(state, value):
    clamped = max(0, min(100, value))
    state.biome_health[state.current_biome] = clamped
    state.ecosystem_health = clamped  # HUD uses this


# -------------------------------
# GAME STATE CLASS
# -------------------------------
@dataclass
class GameState:
    world_x: int = 0
    world_y: int = 0

    width: int = 30
    height: int = 30

    player_x: int = 0
    player_y: int = 0

    ecosystem_health: int = 100  # mirrors current biome
    biome_health: dict = None  # {"forest":100,...}

    energy: int = 0
    food: int = 0
    wood: int = 0
    coal: int = 0
    mushroom: int = 0
    fiber: int = 0
    peat: int = 0

    tiles: list = None
    crop_growth: dict = None

    turn: int = 0
    in_house: bool = False

    house_tiles: list = None
    house_width: int = 10
    house_height: int = 10
    last_house_x: int = 0
    last_house_y: int = 0

    time_of_day: str = "day"
    current_day: int = 0
    current_biome: str = "forest"

    biome_states: dict = None  # persistent biome data

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
            "mushroom": self.mushroom,
            "fiber": self.fiber,
            "peat": self.peat,
            "tiles": self.tiles,
            "in_house": self.in_house,
            "house_tiles": self.house_tiles,
            "house_width": self.house_width,
            "house_height": self.house_height,
            "time_of_day": self.time_of_day,
            "current_day": self.current_day,
            "current_biome": self.current_biome,
            "world_x": self.world_x,
            "world_y": self.world_y,
        }


# -------------------------------
# INITIAL STATE
# -------------------------------
def create_initial_state(width=30, height=30) -> GameState:
    # Random starting tiles
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            if random.random() < 0.25:
                row.append(random.choice([TILE_TREE, TILE_COAL, TILE_BERRIES]))
            else:
                row.append(TILE_EMPTY)
        tiles.append(row)

    state = GameState(
        width=width,
        height=height,
        player_x=width // 2,
        player_y=height // 2,
        tiles=tiles,
        crop_growth={},
        biome_health={
            "forest": 100,
            "tundra": 100,
            "mountain": 100,
            "swamp": 100,
            "desert": 100,
        },
        biome_states={},
    )

    # Mirror current biome's health
    state.ecosystem_health = get_current_biome_health(state)
    return state


# -------------------------------
# BIOME STATE MANAGEMENT
# -------------------------------
def get_or_create_biome_state(state: GameState, biome_name: str):
    if biome_name in state.biome_states:
        return state.biome_states[biome_name]

    # Create new
    biome_state = {
        "tiles": BIOME_GENERATORS[biome_name](state.width, state.height),
        "crop_growth": {},
        "last_house_x": None,
        "last_house_y": None,
        "house_tiles": None,
    }

    state.biome_states[biome_name] = biome_state
    return biome_state


def switch_biome(state: GameState, biome_name: str):
    # ---------------- SAVE CURRENT BIOME ----------------
    current = state.current_biome

    # Sync HUD-facing ecosystem_health
    state.ecosystem_health = get_current_biome_health(state)

    if current not in state.biome_states:
        state.biome_states[current] = {}

    state.biome_states[current]["tiles"] = state.tiles
    state.biome_states[current]["crop_growth"] = state.crop_growth
    state.biome_states[current]["last_house_x"] = state.last_house_x
    state.biome_states[current]["last_house_y"] = state.last_house_y
    state.biome_states[current]["house_tiles"] = state.house_tiles

    # ---------------- LOAD NEW BIOME ----------------
    new_biome_state = get_or_create_biome_state(state, biome_name)

    state.tiles = new_biome_state["tiles"]
    state.crop_growth = new_biome_state["crop_growth"]
    state.last_house_x = new_biome_state["last_house_x"]
    state.last_house_y = new_biome_state["last_house_y"]
    state.house_tiles = new_biome_state["house_tiles"]

    state.current_biome = biome_name

    # Reset player to center
    state.player_x = state.width // 2
    state.player_y = state.height // 2

    # Update HUD-facing health
    state.ecosystem_health = get_current_biome_health(state)


# -------------------------------
# DAY/NIGHT & PASSIVE ENERGY
# -------------------------------
def apply_passive_energy(state: GameState):
    for row in state.tiles:
        for tile in row:
            if tile == TILE_SOLAR:
                state.energy += 1

    if state.turn % 3 == 0:
        for row in state.tiles:
            for tile in row:
                if tile == TILE_WIND:
                    state.energy += 2


# -------------------------------
# MOVEMENT SYSTEM
# -------------------------------
def move_player(state: GameState, direction: str):
    # House movement
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

    # Overworld movement
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

    # Inside biome
    if 0 <= nx < state.width and 0 <= ny < state.height:
        state.player_x = nx
        state.player_y = ny
    else:
        # Try biome transition
        new_world_pos = (state.world_x + dx, state.world_y + dy)
        if new_world_pos in WORLD_MAP:
            state.world_x, state.world_y = new_world_pos
            switch_biome(state, WORLD_MAP[new_world_pos])
        else:
            return

    state.turn += 1
    apply_passive_energy(state)
    spawn_wildlife(state)
    despawn_wildlife(state)
    try_enter_house(state)
    grow_crops(state)


# -------------------------------
# RESOURCE COLLECTION
# -------------------------------
def collect_resource(state: GameState):
    if state.in_house:
        return

    x, y = state.player_x, state.player_y
    tile = state.tiles[y][x]

    health = get_current_biome_health(state)

    if tile == TILE_TREE:
        state.wood += 1
        health -= 3
    elif tile == TILE_COAL:
        state.coal += 1
        state.energy += 3
        health -= 8
    elif tile == TILE_BERRIES:
        state.food += 1
        health += 1
    elif tile == TILE_SNOWY_TREE:
        state.wood += 1
        health -= 3
    elif tile == TILE_FROSTED_BERRIES:
        state.food += 1
        health += 1
    elif tile == TILE_CACTUS:
        state.food += 1
        health += 1
    elif tile == TILE_REEDS:
        state.wood += 1
        health += 1
    elif tile == TILE_MUSHROOM:
        state.food += 1
        health += 1
    elif tile == TILE_PEAT:
        state.energy += 1
        health -= 1
    elif tile == TILE_SANDSTONE:
        state.wood += 1
    elif tile == TILE_QUARTZ:
        state.energy += 2
    elif tile == TILE_ICE_CRYSTAL:
        state.energy += 2
    elif tile == TILE_ICEBERG:
        state.energy += 3
    else:
        return

    # save new health
    set_current_biome_health(state, health)

    state.tiles[y][x] = TILE_EMPTY

    state.turn += 1
    apply_passive_energy(state)
    spawn_wildlife(state)
    despawn_wildlife(state)
    grow_crops(state)
    try_enter_house(state)


# -------------------------------
# FARMING
# -------------------------------
def plant_wheat(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] == TILE_FARM:
        state.tiles[y][x] = TILE_WHEAT_1
        state.crop_growth[(x, y)] = time.time()


def plant_carrot(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] == TILE_FARM:
        state.tiles[y][x] = TILE_CARROT_1
        state.crop_growth[(x, y)] = time.time()


def grow_crops(state: GameState):
    elapsed = time.time() - START_TIME
    for (x, y), start in list(state.crop_growth.items()):
        age = (elapsed - start) / 60.0
        tile = state.tiles[y][x]

        if tile == TILE_WHEAT_1 and age >= 3:
            state.tiles[y][x] = TILE_WHEAT_2
        elif tile == TILE_WHEAT_2 and age >= 6:
            state.tiles[y][x] = TILE_WHEAT_3
        elif tile == TILE_CARROT_1 and age >= 2:
            state.tiles[y][x] = TILE_CARROT_2
        elif tile == TILE_CARROT_2 and age >= 5:
            state.tiles[y][x] = TILE_CARROT_3


def harvest_crop(state: GameState):
    x, y = state.player_x, state.player_y
    tile = state.tiles[y][x]

    if tile == TILE_WHEAT_3:
        state.food += 3
        state.tiles[y][x] = TILE_FARM
        del state.crop_growth[(x, y)]

    elif tile == TILE_CARROT_3:
        state.food += 2
        state.tiles[y][x] = TILE_FARM
        del state.crop_growth[(x, y)]


# -------------------------------
# BUILDING
# -------------------------------
def plant_tree(state: GameState):
    x, y = state.player_x, state.player_y
    if state.in_house:
        return
    if state.tiles[y][x] != TILE_EMPTY:
        return
    if state.wood < 1:
        return

    state.wood -= 1
    state.tiles[y][x] = TILE_SAPLING

    health = get_current_biome_health(state) + 3
    set_current_biome_health(state, health)


def build_farm(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_EMPTY:
        return
    if state.wood < 2:
        return

    state.wood -= 2
    state.tiles[y][x] = TILE_FARM


def build_solar_panel(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_EMPTY:
        return
    if state.wood < 2:
        return

    state.wood -= 2
    state.tiles[y][x] = TILE_SOLAR


def build_wind_turbine(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_EMPTY:
        return
    if state.wood < 3:
        return

    state.wood -= 3
    state.tiles[y][x] = TILE_WIND


def build_house(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] != TILE_EMPTY:
        return
    if state.wood < 5:
        return

    state.wood -= 5
    state.tiles[y][x] = TILE_HOUSE

    state.last_house_x = x
    state.last_house_y = y

    if state.house_tiles is None:
        state.house_tiles = [
            [TILE_EMPTY for _ in range(state.house_width)]
            for _ in range(state.house_height)
        ]


# -------------------------------
# HOUSE ENTRY
# -------------------------------
def try_enter_house(state: GameState):
    x, y = state.player_x, state.player_y
    if state.tiles[y][x] == TILE_HOUSE:
        state.in_house = True
        state.player_x = state.house_width // 2
        state.player_y = state.house_height // 2


def exit_house(state: GameState):
    if not state.in_house:
        return

    state.in_house = False

    for dy in [-1, 1, 0]:
        for dx in [-1, 1, 0]:
            nx = state.last_house_x + dx
            ny = state.last_house_y + dy
            if (
                0 <= nx < state.width
                and 0 <= ny < state.height
                and state.tiles[ny][nx] == TILE_EMPTY
            ):
                state.player_x = nx
                state.player_y = ny
                return

    state.player_x = state.last_house_x
    state.player_y = state.last_house_y


# -------------------------------
# WILDLIFE SYSTEM
# -------------------------------
def spawn_wildlife(state):
    # Spawn depends ONLY on current biome's health
    if get_current_biome_health(state) < 70:
        return

    if random.random() > 0.03:
        return

    x = random.randint(0, state.width - 1)
    y = random.randint(0, state.height - 1)

    if state.tiles[y][x] != TILE_EMPTY:
        return

    biome = state.current_biome

    if biome == "forest":
        animals = [TILE_RABBIT, TILE_DEER, TILE_BIRD]
    elif biome == "desert":
        animals = [TILE_LIZARD, TILE_SNAKE, TILE_SCORPION]
    elif biome == "tundra":
        animals = [TILE_ARCTIC_FOX, TILE_POLAR_HARE, TILE_SEAL, TILE_WALRUS]
    elif biome == "swamp":
        animals = [TILE_FROG, TILE_CROCODILE, TILE_SNAKE, TILE_STORK]
    elif biome == "mountain":
        animals = [TILE_GOAT, TILE_HAWK]
    else:
        return

    state.tiles[y][x] = random.choice(animals)


def despawn_wildlife(state):
    # Wildlife only despawns if *current* biome health is low
    if get_current_biome_health(state) > 40:
        return

    for y in range(state.height):
        for x in range(state.width):
            tile = state.tiles[y][x]
            if tile in [
                TILE_RABBIT,
                TILE_DEER,
                TILE_BIRD,
                TILE_LIZARD,
                TILE_SNAKE,
                TILE_SCORPION,
                TILE_ARCTIC_FOX,
                TILE_POLAR_HARE,
                TILE_SEAL,
                TILE_WALRUS,
                TILE_FROG,
                TILE_CROCODILE,
                TILE_STORK,
                TILE_GOAT,
                TILE_HAWK,
            ]:
                state.tiles[y][x] = TILE_EMPTY


# -------------------------------
# RESET
# -------------------------------
def reset_state():
    return create_initial_state()
