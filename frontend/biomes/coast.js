// biomes/coast.js
export function emojiForCoast(tile) {
  const map = {
    // terrain
    sand: "🏖️",
    swamp_water: "🌊",

    // animals / sea life
    seal: "🦭",
    beluga: "🐋",

    // fallback
    empty: "",
  };

  return map[tile] || null;
}
