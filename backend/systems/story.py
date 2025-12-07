def choose_path(state, path):
    state.player_path = path
    state.awaiting_path_choice = False

    if path == "eco":
        state.dialog_message = "🌱 You chose the Eco-Guardian path!"
        # starter bonus
        state.inventory["mushroom"] += 3
    elif path == "industry":
        state.dialog_message = "💼 You chose the Industrial path!"
        state.inventory["coal"] += 3
    else:
        state.dialog_message = "⚪ You walk your own road."
        state.inventory["fiber"] += 3
        
    