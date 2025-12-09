// biomes/coast.js
export function emojiForCoast(tile) {
  const map = {
    // terrain
    sand: "🏖️",
    ocean: "🌊",

    // collectibles
    shell: "🐚",

    // animals / sea life
    crab: "🦀",
    seal: "🦭",
    beluga: "🐋",

    // fallback
    empty: "",
  };

  return map[tile] || null;
}
