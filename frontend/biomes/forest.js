export function emojiForForest(tile) {
  const map = {
    tree: "🌳",
    coal: "⛏️",
    berries: "🍓",
    sapling: "🌱",

    // farm + crops
    farm: "🚜",
    wheat1: "🌱",
    wheat2: "🌾",
    wheat3: "🌾✨",
    carrot1: "🌱",
    carrot2: "🥕",
    carrot3: "🥕✨",

    // wildlife
    rabbit: "🐇",
    deer: "🦌",
    bird: "🐦",

    // buildings + structures
    house: "🏡",
    solar: "☀️",
    wind: "🌀",

    //npcs
    npc_forest_guide: "🧑‍🌾",
    npc_desert_guide: "🧑‍🌵",

    empty: ""
  };

  return map[tile] || null;
}
