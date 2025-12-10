# game_state.py
from dataclasses import dataclass

@dataclass
class GameState:
    world_x: int = 0
    world_y: int = 0

    width: int = 30
    height: int = 30

    player_x: int = 0
    player_y: int = 0

    player_health: int = 100

    # mirrors *current biome's* health
    ecosystem_health: int = 100
    biome_health: dict = None   # {"forest": 100, ...}

    energy: int = 0
    wood: int = 0
    coal: int = 0

    # swamp extras
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
    
    inventory: dict = None  # {"item_name": quantity, ...}
    
    player_path: str = None  # "eco", "industry", or "neutral"
    awaiting_path_choice: bool = False
    dialog_message: str = ""
    
    # Quest system
    active_quests: dict = None  # {"quest_name": {"status": "active/completed", "progress": {...}}}
    
    # Path-based modifiers
    eco_bonuses: bool = False
    industry_bonuses: bool = False

    # persistent data per biome
    biome_states: dict = None   # {"forest": {...}, "tundra": {...}, ...}
    pets: list = None

    def to_dict(self):
        """State -> JSON-safe dict for frontend."""
        return {
            "width": self.width,
            "height": self.height,
            "player_x": self.player_x,
            "player_y": self.player_y,
            "player_health": self.player_health,
            "ecosystem_health": self.ecosystem_health,
            "energy": self.energy,
            
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
            "inventory": self.inventory,
            "turn": self.turn,
            "dialog_message": self.dialog_message,
            "awaiting_path_choice": self.awaiting_path_choice,
            "player_path": self.player_path,
            "eco_bonuses": self.eco_bonuses,
            "industry_bonuses": self.industry_bonuses,
            "biome_health": self.biome_health,
            "biome_states": self.biome_states,
            "pets": self.pets,
            "active_quests": self.active_quests,

        }
