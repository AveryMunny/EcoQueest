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

