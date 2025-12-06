export function emojiForMountain(tile) {
  const map = {
    // === TERRAIN ===
    rock: "🪨",
    stone: "⬛",
    snow_rock: "❄️🪨",
    cave: "🕳️",

    // === RESOURCES ===
    ore: "⛏️",
    crystal: "💎",

    // optional future crafting resources:
    mineral: "💠",
    gold: "🥇",
    silver: "🥈",
    iron: "⛓️",
    mountain_grass: "🌿",

    // === ANIMALS ===
    goat: "🐐",
    hawk: "🦅",

    // === OPTIONAL STRUCTURES ===
    mountain_hut: "🏕️",
    lookout_tower: "🗼",

    empty: "",
  };

  return map[tile] || null;
}
