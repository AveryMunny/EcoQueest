export function emojiForTundra(tile) {
  const map = {
    // terrain
    snow: "❄️",
    snowflake: "✨",
    ice: "🧊",
    snowy_tree: "🌲❄️",
    ice_crystal: "🔷",
    frosted_berries: "🫐❄️",
    iceberg: "🧊🗻",

    // animals
    penguin: "🐧",
    arctic_fox: "🦊❄️",
    polar_hare: "🐇❄️",
    walrus: "🦭",
    seal: "🐬❄️",
    beluga: "🐋❄️",

    // structures
    snowman: "⛄",
    igloo: "🏠❄️",

    empty: ""
  };

  return map[tile] || null;
}
