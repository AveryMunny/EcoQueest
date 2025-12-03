export function emojiForSwamp(tile) {
  const map = {
    mud: "🟫",
    swamp_grass: "🌿",
    reeds: "🎋",
    swamp_water: "💧",

    // animals
    frog: "🐸",
    crocodile: "🐊",
    snake: "🐍",
    stork: "🕊️",

    // structures
    // (none specific to swamp for now)

    //resource
    peat: "🪵",
    mushroom: "🍄",
    fiber : "🧵",
  };

  return map[tile] || null;
}
