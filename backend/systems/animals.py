import random
from tile_types import (
    TILE_RABBIT, TILE_DEER, TILE_BIRD,
    TILE_LIZARD, TILE_SNAKE, TILE_SCORPION,
    TILE_ARCTIC_FOX, TILE_POLAR_HARE, TILE_SEAL, TILE_WALRUS,
    TILE_FROG, TILE_CROCODILE, TILE_TURTLE, TILE_STORK,
    TILE_GOAT, TILE_HAWK,

    TILE_EMPTY, TILE_HOUSE, TILE_WIND, TILE_SOLAR, TILE_FARM
)
from systems.inventory import add_item, remove_item

ANIMAL_TILES = {
    TILE_RABBIT, TILE_DEER, TILE_BIRD,
    TILE_LIZARD, TILE_SNAKE, TILE_SCORPION,
    TILE_ARCTIC_FOX, TILE_POLAR_HARE, TILE_SEAL, TILE_WALRUS,
    TILE_FROG, TILE_CROCODILE, TILE_TURTLE, TILE_STORK,
    TILE_GOAT, TILE_HAWK
}

BLOCKING_TILES = {TILE_HOUSE, TILE_WIND, TILE_SOLAR, TILE_FARM}

def move_animals(state):
    """Make animals randomly wander 1 tile per turn."""
    tiles = state.tiles
    width, height = state.width, state.height

    # Collect all animal positions
    animals = []
    for y in range(height):
        for x in range(width):
            if tiles[y][x] in ANIMAL_TILES:
                animals.append((x, y, tiles[y][x]))

    # Try to move each animal
    for x, y, animal in animals:

        # 25% chance an animal moves
        if random.random() > 0.25:
            continue

        # Choose random direction
        dx, dy = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        nx, ny = x + dx, y + dy

        # Check boundaries
        if not (0 <= nx < width and 0 <= ny < height):
            continue

        # Check collision
        target = tiles[ny][nx]
        if target != TILE_EMPTY:
            continue

        # Move the animal
        tiles[ny][nx] = animal
        tiles[y][x] = TILE_EMPTY


def attempt_tame(state):
    """Attempt to tame an adjacent animal. Returns:
       - None if no animal nearby
       - True if an animal was found and successfully tamed
       - False if an animal was found but taming failed
    """
    tiles = state.tiles
    x, y = state.player_x, state.player_y
    width, height = state.width, state.height

    # Positions to check: on or next to player
    nearby = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]

    for nx, ny in nearby:
        if not (0 <= nx < width and 0 <= ny < height):
            continue
        tile = tiles[ny][nx]
        if tile in ANIMAL_TILES:
            # Define tame chances per animal class
            base_chances = {
                TILE_RABBIT: 0.7,
                TILE_DEER: 0.4,
                TILE_BIRD: 0.6,
                TILE_GOAT: 0.6,
                TILE_SEAL: 0.35,
                TILE_WALRUS: 0.2,
                TILE_LIZARD: 0.3,
                TILE_POLAR_HARE: 0.5,
                TILE_ARCTIC_FOX: 0.15,
                TILE_FROG: 0.5,
                TILE_TURTLE: 0.45,
                TILE_CROCODILE: 0.05,
                TILE_SCORPION: 0.1,
                TILE_SNAKE: 0.1,
                TILE_STORK: 0.4,
                TILE_HAWK: 0.1,
            }

            # Items required for taming certain animals (species-specific bait)
            required_items = {
                TILE_DEER: ("carrot", 1),
                TILE_RABBIT: ("carrot", 1),
                TILE_BIRD: ("berries", 1),
                TILE_GOAT: ("wheat", 1),
                TILE_SEAL: ("fish", 1),
                TILE_WALRUS: ("fish", 2),
            }

            req = required_items.get(tile)
            # If a requirement exists, verify player has it
            if req is not None:
                item_name, amount = req
                inv = state.inventory or {}
                has_amount = (inv.get(item_name, 0) >= amount)

                if not has_amount:
                    state.dialog_message = f"You need {amount} {item_name} to attempt taming this animal."
                    return False  # animal remains
                # consume the item from inventory using helper
                remove_item(state, item_name, amount)

            chance = base_chances.get(tile, 0.2)
            import random
            success = random.random() < chance

            # Remove animal from map on attempt (they either flee or come with you)
            tiles[ny][nx] = TILE_EMPTY

            # Add a pet item to inventory if tamed
            pet_key = f"pet_{tile}"
            if state.inventory is None:
                state.inventory = {}
            if success:
                state.inventory[pet_key] = state.inventory.get(pet_key, 0) + 1
            else:
                # ensure no pet added on failure
                state.inventory[pet_key] = state.inventory.get(pet_key, 0) + 0

            # track pets in state.pets
            if success:
                if getattr(state, 'pets', None) is None:
                    state.pets = []
                state.pets.append(tile)
                state.dialog_message = f"You tamed the {tile}! It is now your companion."
                return True
            else:
                state.dialog_message = f"The {tile} resisted taming and ran away."
                return False

    return None
