import { emojiForForest } from "./biomes/forest.js";
import { emojiForDesert } from "./biomes/desert.js";
import { emojiForTundra } from "./biomes/tundra.js";
import { emojiForSwamp } from "./biomes/swamp.js";
import { emojiForMountain } from "./biomes/mountain.js";
import { emojiForCoast } from "./biomes/coast.js";

let state = null;

/* ---------------- FETCH HELPERS ---------------- */
async function fetchState() {
  const res = await fetch("/api/state");
  state = await res.json();
  render();
}

async function sendMove(direction) {
  const res = await fetch("/api/move", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ direction }),
  });

  state = await res.json();
  state.dialog_message = "";
  render();
  positionHelpMenu();
}

export async function choosePath(path) {
    const res = await fetch("/api/choose_path", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path })
    });

    const newState = await res.json();
    state = newState;
    render();

    // Hide dialog after choosing
    state.dialog_message = "";
    state.awaiting_path_choice = false;

    removeNPC();
    render();
}

window.choosePath = choosePath; 
function removeNPC() {
    const tiles = state.tiles;
    for (let y = 0; y < tiles.length; y++) {
        for (let x = 0; x < tiles[y].length; x++) {
            if (tiles[y][x] === "npc_forest_guide") {
                tiles[y][x] = "empty";
                return;
            }
        }
    }
}


async function sendAction(url) {
  const res = await fetch(`/api/${url}`, { method: "POST" });
  state = await res.json();
  render();
}

/* ---------------- HELP MENU ---------------- */
function toggleHelpMenu() {
  const menu = document.getElementById("helpMenu");
  menu.classList.toggle("hidden");
  
  // Reposition immediately when shown
  if (!menu.classList.contains("hidden")) {
    setTimeout(positionHelpMenu, 50);
  }
}


function positionHelpMenu() {
  const menu = document.getElementById("helpMenu");
  if (!menu || menu.classList.contains("hidden")) return;

  const grid = document.getElementById("grid");
  if (!grid) return;

  const gridRect = grid.getBoundingClientRect();

  // Tile size (cell + gap)
  const tileSize = 34;
  const spacing = 20;

  // Vertical center on player (in viewport coordinates)
  const playerCenterY = gridRect.top + state.player_y * tileSize + tileSize / 2;

  const menuHeight = menu.offsetHeight;
  const menuWidth = menu.offsetWidth;

  // Center menu vertically on player, but clamp to viewport
  let newTop = Math.round(playerCenterY - menuHeight / 2);
  newTop = Math.max(12, Math.min(newTop, window.innerHeight - menuHeight - 12));

  // Preferred left is to place the menu just right of the grid
  let preferredLeft = Math.ceil(gridRect.right + spacing);
  const maxLeft = window.innerWidth - menuWidth - 12; // keep 12px margin

  // If there's not enough space to the right, clamp to viewport right edge
  let newLeft = Math.min(preferredLeft, maxLeft);
  if (newLeft < 12) newLeft = Math.max(12, maxLeft);

  menu.style.top = `${newTop}px`;
  menu.style.left = `${newLeft}px`;
}


/* ---------------- EMOJI LOOKUP ---------------- */
function getBiomeEmoji(tile) {
  if (state.current_biome === "forest") return emojiForForest(tile);
  if (state.current_biome === "desert") return emojiForDesert(tile);
  if (state.current_biome === "tundra") return emojiForTundra(tile);
  if (state.current_biome === "swamp") return emojiForSwamp(tile);
  if (state.current_biome === "mountain") return emojiForMountain(tile);
  if (state.current_biome === "coastal") return emojiForCoast(tile);
  return null;
}

function getGlobalEmoji(tile) {
  const map = {
    solar: "☀️",
    wind: "🌀",
    house: "🏡",
    farm: "🚜",
    rabbit: "🐇",
    deer: "🦌",
    bird: "🐦",
    wheat1: "🌱",
    wheat2: "🌾",
    wheat3: "🌾✨",
    carrot1: "🌱",
    carrot2: "🥕",
    carrot3: "🥕✨",
  };
  return map[tile] || null;
}

function render() {
    if (!state) return;

    /* ---------- BODY / THEME ---------- */
    const body = document.body;
    body.className = "";
    body.classList.add(state.current_biome);
    body.classList.add(state.time_of_day === "day" ? "daytime" : "nighttime");

    /* ---------- GRID ---------- */
    const grid = document.getElementById("grid");
    grid.innerHTML = "";

    const tiles = state.in_house ? state.house_tiles : state.tiles;
    grid.style.gridTemplateColumns = `repeat(${tiles[0].length}, 32px)`;

    for (let y = 0; y < tiles.length; y++) {
        for (let x = 0; x < tiles[y].length; x++) {
            const div = document.createElement("div");
            const tile = tiles[y][x];

            div.classList.add("cell", tile);

            let emoji = getBiomeEmoji(tile) || getGlobalEmoji(tile);

            if (state.player_x === x && state.player_y === y) {
                div.classList.add("player");
                emoji = "🧍";
            }

            div.textContent = emoji || "";
            grid.appendChild(div);
        }
    }

    /* ---------- DIALOG BOX ---------- */
    const dialogBox = document.getElementById("dialogBox");
    const dialogText = document.getElementById("dialogText");
    const dialogChoices = document.getElementById("dialogChoices");

    if (state.dialog_message) {
        dialogBox.classList.remove("hidden");
        dialogText.textContent = state.dialog_message;

        if (state.awaiting_path_choice) {
            dialogChoices.classList.remove("hidden");
        } else {
            dialogChoices.classList.add("hidden");
        }

        updateDialogPosition();
        window.dialogOpen = true;
    } else {
        dialogBox.classList.add("hidden");
        dialogChoices.classList.add("hidden");
        window.dialogOpen = false;
    }

    /* ---------- HUD INFO ---------- */
    document.getElementById("hud-biome").textContent = state.current_biome;
    document.getElementById("hud-time").textContent = state.time_of_day;
    document.getElementById("hud-day").textContent = state.current_day;

    document.getElementById("eco-bar").style.width = state.ecosystem_health + "%";
    document.getElementById("energy-bar").style.width = Math.min(state.energy, 100) + "%";

    document.getElementById("eco").textContent = state.ecosystem_health;
    document.getElementById("energy").textContent = state.energy;

    /* ---------- INVENTORY ---------- */
    const inv = state.inventory || {};
    document.getElementById("carrot").textContent = inv.carrot ?? 0;
    document.getElementById("wheat").textContent = inv.wheat ?? 0;
    document.getElementById("berries").textContent = inv.berries ?? 0;
    document.getElementById("frosted_berries").textContent = inv.frosted_berries ?? 0;
    document.getElementById("fish").textContent = inv.fish ?? 0;
    document.getElementById("wood").textContent = inv.wood ?? 0;
    document.getElementById("coal").textContent = inv.coal ?? 0;
    document.getElementById("mushroom").textContent = inv.mushroom ?? 0;
    document.getElementById("fiber").textContent = inv.fiber ?? 0;
    document.getElementById("peat").textContent = inv.peat ?? 0;
    document.getElementById("stone").textContent = inv.stone ?? 0;
    document.getElementById("ore_chunk").textContent = inv.ore_chunk ?? 0;
    document.getElementById("ice_shard").textContent = inv.ice_shard ?? 0;
    document.getElementById("crystal_shard").textContent = inv.crystal_shard ?? 0;
}


/* ---------------- INPUT ---------------- */
function setupInput() {
  document.addEventListener("keydown", (e) => {
    const key = e.key;

    if (["w", "ArrowUp"].includes(key)) sendMove("up");
    else if (["s", "ArrowDown"].includes(key)) sendMove("down");
    else if (["a", "ArrowLeft"].includes(key)) sendMove("left");
    else if (["d", "ArrowRight"].includes(key)) sendMove("right");
    else if (key === "p") sendAction("plant");
    else if (key === "1") {
      if (state.awaiting_path_choice) sendAction("choose_path_eco");
      else sendAction("solar");
    }
    else if (key === "2") {
      if (state.awaiting_path_choice) sendAction("choose_path_industry");
      else sendAction("wind");
    }
    else if (key === "3") {
      if (state.awaiting_path_choice) sendAction("choose_path_neutral");
      else sendAction("house");
    }
    else if (key === "4") sendAction("farm");
    else if (key === "5") sendAction("plant_wheat");
    else if (key === "6") sendAction("plant_carrot");
    else if (key === "x") sendAction("harvest");
    else if (key === "e") sendAction("exit_house");
    else if (key === "h") toggleHelpMenu();
    else if (key.toLowerCase() === "f") sendAction("interact");
        
    else if (key === " ") {
      e.preventDefault();
      sendAction("collect");
    }
  });

  document.getElementById("resetBtn").addEventListener("click", () => {
    sendAction("reset");
  });
}

/* ---------------- INIT ---------------- */
window.addEventListener("load", () => {
  setupInput();
  fetchState();
});
window.addEventListener("resize", () => {
  positionHelpMenu();
});
window.addEventListener("scroll", () => {
  positionHelpMenu();
});
window.addEventListener("orientationchange", () => {
  positionHelpMenu();
});
window.addEventListener("click", () => {
  positionHelpMenu();
});
window.addEventListener("touchstart", () => {
  positionHelpMenu();
});
window.addEventListener("touchmove", () => {
  positionHelpMenu();
});
window.addEventListener("touchend", () => {
  positionHelpMenu();
});

function toggleInventory() {
  const menu = document.getElementById("inventoryMenu");
  menu.classList.toggle("hidden");
  renderInventory();
}

// KEYBOARD SHORTCUT
window.addEventListener("keydown", (e) => {
  if (e.key.toLowerCase() === "i") {
    toggleInventory();
  }
});
function renderInventory() {
  const list = document.getElementById("inventoryList");
  list.innerHTML = "";

  if (!state || !state.inventory) return;

  for (const [item, amount] of Object.entries(state.inventory)) {
    if (amount > 0) {
      const div = document.createElement("div");
      div.textContent = `${item}: ${amount}`;
      list.appendChild(div);
    }
  }
}

function updateDialogPosition() {
  const box = document.getElementById("dialogBox");
  if (!state.dialog_message || box.classList.contains("hidden")) return;

  const grid = document.getElementById("grid");
  const gridRect = grid.getBoundingClientRect();

  const tileSize = 34;

  // NPC or player tile reference (bubble follows NPC)
  let targetX = state.player_x;
  let targetY = state.player_y - 1; // bubble appears above player

  const x = gridRect.left + targetX * tileSize + tileSize / 2;
  const y = gridRect.top + targetY * tileSize;

  box.style.left = `${x}px`;
  box.style.top = `${y}px`;
}


export {};