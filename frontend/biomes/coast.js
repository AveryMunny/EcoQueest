// biomes/coast.js
export function emojiForCoast(tile) {
  const map = {
    // terrain
    sand: "🏖️",
    ocean: "🟦",   // ← totally blue, clean, simple water tile

    // animals / sea life
    seal: "🦭",
    beluga: "🐋",

    // fallback
    empty: "",
  };

  return map[tile] || null;
}
