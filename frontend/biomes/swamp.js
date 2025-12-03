export function emojiForSwamp(tile) {
  const map = {
    mud: "🟫",
    swamp_grass: "🌿",
    reeds: "🎋",
    swamp_water: "💧",

    frog: "🐸",
    crocodile: "🐊",
    snake: "🐍",
    stork: "🕊️"
  };

  return map[tile] || null;
}
