# systems/crafting.py
from game_state import GameState
from systems.inventory import has_items, remove_item, add_item

# Define all recipes in one place
# Format: recipe_name -> {"requires": {...}, "produces": {...}}
RECIPES = {
    "rope": {
        "requires": {"wood": 1, "fiber": 1},
        "produces": {"rope": 1},
    },
    "plank": {
        "requires": {"wood": 2},
        "produces": {"plank": 1},
    },
    "fabric": {
        "requires": {"fiber": 2},
        "produces": {"fabric": 1},
    },
    "net": {
        "requires": {"rope": 2},
        "produces": {"net": 1},
    },
}


def can_craft(state: GameState, recipe_name: str) -> bool:
    """Check if player has all required ingredients for a recipe."""
    if recipe_name not in RECIPES:
        return False
    
    recipe = RECIPES[recipe_name]
    required = recipe["requires"]
    
    # Check if we have all required items
    return has_items(state, **required)


def craft(state: GameState, recipe_name: str) -> bool:
    """
    Attempt to craft an item.
    Returns True if successful, False if not enough resources.
    """
    if recipe_name not in RECIPES:
        state.dialog_message = f"Unknown recipe: {recipe_name}"
        return False
    
    recipe = RECIPES[recipe_name]
    required = recipe["requires"]
    produces = recipe["produces"]
    
    # Check if we have enough ingredients
    if not can_craft(state, recipe_name):
        missing = []
        for item, amount in required.items():
            current = state.inventory.get(item, 0)
            if current < amount:
                missing.append(f"{amount - current} more {item}")
        state.dialog_message = f"Cannot craft {recipe_name}. Need: {', '.join(missing)}"
        return False
    
    # Remove ingredients
    for item, amount in required.items():
        remove_item(state, item, amount)
    
    # Add products
    for item, amount in produces.items():
        add_item(state, item, amount)
    
    state.dialog_message = f"Crafted {recipe_name}!"
    return True


def get_available_recipes(state: GameState):
    """Return a mapping of all recipes and their requires/produces for the frontend.

    Previously this returned only craftable recipes; frontend expects a recipe
    dictionary to render the menu. Expose the full registry so the UI can
    present recipes even when the player lacks resources.
    """
    out = {}
    for name, data in RECIPES.items():
        out[name] = {"requires": data.get("requires", {}), "produces": data.get("produces", {})}
    return out
