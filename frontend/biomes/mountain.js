export function emojiForMountain(tile) {
  const map = {
    // terrain 
    rock: "🪨",
    stone: "⬛",
    snow_rock: "❄️🪨",
    cave: "🕳️",

    //resoures 
    ore: "⛏️",
    crystal: "💎",

    // possible additions, but idk how I can get this in 
    mineral: "💠",
    gold: "🥇",
    silver: "🥈",
    iron: "⛓️",
    mountain_grass: "🌿",

    // animals 
    goat: "🐐",
    hawk: "🦅",

    // structures
    mountain_hut: "🏕️",
    lookout_tower: "🗼",

    empty: "",
  };

  return map[tile] || null;
}
