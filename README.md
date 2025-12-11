# EcoQuest 🌱

An ecosystem management and survival game where you explore different biomes, manage resources, craft items, and make choices that shape the world around you.

## 🎮 Features

### World Exploration
- **6 Diverse Biomes**: Forest, Desert, Tundra, Coastal, Swamp, and Mountain
- **Day/Night Cycle**: 5-minute day and night phases that affect gameplay
- **Persistent World**: Each biome remembers your changes when you return

### Survival Mechanics
- **Health & Energy System**: Start with 100 health and 100 energy
- **Energy Drain**: Actions consume energy; running out damages your health
- **Food System**: Collect and eat berries, wheat, carrots, fish, and mushrooms to restore health and energy

### Building & Crafting
- **Structures**: Build houses with customizable interiors, farms, solar panels, and wind turbines
- **Crafting System**: Create tools, fabric, rope, planks, nets, meal packs, and bedrolls
- **Farming**: Plant and harvest wheat and carrots that grow over a full day-night cycle
- **Tree Planting**: Trees occasionally drop saplings for replanting

### NPCs & Quests
- **Forest Guide**: Choose your path (Eco-Guardian, Industrial Entrepreneur, or Wanderer)
- **Desert Merchant**: Complete quests for rewards (e.g., bring 5 fiber for quartz and energy)
- **Path Bonuses**: Your chosen path grants special bonuses throughout the game

### Biome-Specific Resources
- **Forest**: Trees, berries, coal
- **Desert**: Cacti (fiber), sandstone, quartz, oases
- **Tundra**: Snowy trees, frosted berries, ice crystals, icebergs
- **Coastal**: Sand, ocean, shells, crabs, fish
- **Swamp**: Reeds, mushrooms, peat
- **Mountain**: Rocks, stone, ore

### Wildlife & Pets
- **Wildlife Spawning**: Animals appear when ecosystem health ≥ 70
- **Taming System**: Interact with animals to tame them as pets

## 🕹️ Controls

### Movement
- **W / A / S / D** or **Arrow Keys** — Move
- **Space** — Collect resources
- **E** — Exit house
- **F** — Interact with NPCs

### Building
- **P** — Plant Tree (1 wood)
- **1** — Solar Panel (2 wood)
- **2** — Wind Turbine (3 wood)
- **3** — Build House (5 wood)
- **4** — Build Farm Plot (2 wood)

### Farming
- **5** — Plant Wheat
- **6** — Plant Carrot
- **X** — Harvest crops

### Menus
- **H** — Toggle Help Menu
- **I** — Toggle Inventory
- **C** — Toggle Crafting Menu

## 🎯 Gameplay Tips

1. **Manage Your Energy**: Every 3 turns you lose 1 energy. Harvesting costs 2 energy, building costs 1 energy.
2. **Eat Regularly**: When energy hits 0, your health starts dropping. Keep food in your inventory!
3. **Craft Survival Items**: 
   - Meal Pack (plank + fish + carrot) restores 40 energy and 20 health
   - Bedroll (2 fabric + rope + plank) restores 30 health
4. **Complete Quests**: NPCs offer valuable rewards and bonuses
5. **Plant Saplings**: Trees drop saplings 25% of the time—replant to maintain resources
6. **Build Energy Sources**: Solar panels and wind turbines provide passive energy

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Architecture**: Modular systems (movement, crafting, farming, NPCs, etc.)

## 🚀 How to Run

1. Navigate to the `backend` folder
2. Run `python app.py`
3. Open your browser to `http://localhost:5000`

## 📝 Game Mechanics

### Energy System
- Actions drain energy over time
- Solar panels generate +1 energy per turn (+2 for Industrial path)
- Wind turbines generate +2 energy every 3 turns (+3 for Industrial path)
- Food restores energy and health

### Ecosystem Health
- Ranges from 0-100 per biome
- Harvesting resources lowers health (less for Eco-Guardians)
- Planting trees increases health
- Wildlife only spawns at ≥70 health

### Crop Growth
- Crops grow over one full day-night cycle (10 minutes)
- Stage 1→2 at ~5 minutes, Stage 2→3 at ~10 minutes
- Eco-Guardians get 20% faster growth

---

Made with 🌍 by Avery
