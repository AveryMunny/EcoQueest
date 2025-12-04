export function emojiForMountain(tile) {
  const map = {
    // terrain
    mountain_rock: "🪨🗻",
    cliff: "🧱🗻",
    mountain_grass: "🌿🗻",
    snow_capped_peak: "🏔️", 
    cave: "🕳️",
    mineral: "💎",
    gold: "🥇",
    silver: "🥈",
    iron: "⛓️",
    // animals
    mountain_goat: "🐐",
    hawk: "🦅",
    // structures
    mountain_hut: "🏕️",
    lookout_tower: "🗼",
    empty: ""
    };
    return map[tile] || null;
}