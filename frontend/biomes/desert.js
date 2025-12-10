// biomes/desert.js
export function emojiForDesert(tile) {
   const map = {
    // terrain
    sand: "🏜️",
    sandstone: "🪨",
    cactus: "🌵",
    oasis: "🏝️",
    rock: "🪨",
    quartz: "🔶",

    // NPCs
    npc_desert_merchant: "🧑‍💼",

    // animals
    lizard: "🦎",
    snake: "🐍",
    scorpion: "🦂",
    camel: "🐪",
    vulture: "🦅",
    empty: ""
}
  return map[tile] || null;
}

