# systems/inventory.py

def add_item(state, item, amount=1):
    state.inventory[item] = state.inventory.get(item, 0) + amount


def remove_item(state, item, amount=1):
    if state.inventory.get(item, 0) >= amount:
        state.inventory[item] -= amount
        return True
    return False


def has_items(state, **requirements):
    """
    Example: has_items(state, wood=5, stone=2)
    """
    inv = state.inventory

    for item, needed in requirements.items():
        if inv.get(item, 0) < needed:
            return False

    return True
def get_item_count(state, item):
    return state.inventory.get(item, 0) 