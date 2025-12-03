let state = null;

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
  render();

  // updating menu ONLY on movement
  positionHelpMenu();
}


async function sendExitHouse() {
  const res = await fetch("/api/exit_house", { method: "POST" });
  state = await res.json();
  render();
}


async function sendCollect() {
  const res = await fetch("/api/collect", {
    method: "POST",
  });
  state = await res.json();
  render();
}

async function sendReset() {
  const res = await fetch("/api/reset", {
    method: "POST",
  });
  state = await res.json();
  render();
}

async function sendPlant() {
  const res = await fetch("/api/plant", { method: "POST" });
  state = await res.json();
  render();
}

async function sendSolar() {
  const res = await fetch("/api/solar", { method: "POST" });
  state = await res.json();
  render();
}

async function sendWind() {
  const res = await fetch("/api/wind", { method: "POST" });
  state = await res.json();
  render();
}

async function sendHouse() {
  const res = await fetch("/api/house", { method: "POST" });
  state = await res.json();
  render();
}

async function sendPlantWheat() {
  const res = await fetch("/api/plant_wheat", { method: "POST" });
  state = await res.json(); render();
}

async function sendPlantCarrot() {
  const res = await fetch("/api/plant_carrot", { method: "POST" });
  state = await res.json(); render();
}

async function sendHarvest() {
  const res = await fetch("/api/harvest", { method: "POST" });
  state = await res.json(); render();
}

async function sendFarm() {
  const res = await fetch("/api/farm", { method: "POST" });
  state = await res.json();
  render();
}


function toggleHelpMenu() {
  const menu = document.getElementById("helpMenu");
  menu.classList.toggle("hidden");
}

function positionHelpMenu() {
  if (!state) return;

  const menu = document.getElementById("helpMenu");
  const grid = document.getElementById("grid");
  if (!menu || !grid) return;

  const gridRect = grid.getBoundingClientRect();

  const tileSize = 34; // 32px tile + ~2px gap
  const playerCenterY =
    gridRect.top + state.player_y * tileSize + tileSize / 2;

  const menuHeight = menu.offsetHeight || 0;

  // Align menu center with player center
  let newTop = playerCenterY - menuHeight / 2;

  // Keep menu on screen (20px padding top/bottom)
  const minTop = 20;
  const maxTop = window.innerHeight - menuHeight - 20;
  newTop = Math.max(minTop, Math.min(maxTop, newTop));

  menu.style.top = `${newTop}px`;
}






function render() {
  if (!state) return;

  // Determine which grid to drawing
  let gridData = null;
  let width = 0;
  let height = 0;

  if (state.time_of_day === "day") {
    document.body.classList.add("daytime");
    document.body.classList.remove("nighttime");
    } else {
    document.body.classList.add("nighttime");
    document.body.classList.remove("daytime");
    }

    if (state.time_of_day === "day") {
    document.documentElement.style.setProperty("--tile-border", "1px solid rgba(0, 0, 0, 0.25)");
    } else {
    document.documentElement.style.setProperty("--tile-border", "1px solid rgba(255, 255, 255, 0.12)");
    } 



  if (state.in_house) {
    gridData = state.house_tiles;
    width = state.house_width;
    height = state.house_height;
  } else {
    gridData = state.tiles;
    width = state.width;
    height = state.height;
  }

  // HUD
  document.getElementById("eco").textContent = state.ecosystem_health;
  document.getElementById("energy").textContent = state.energy;
  document.getElementById("food").textContent = state.food;
  document.getElementById("wood").textContent = state.wood;
  document.getElementById("coal").textContent = state.coal;

  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  grid.style.gridTemplateColumns = `repeat(${width}, 32px)`;

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const cell = document.createElement("div");
      const tileType = gridData[y][x];

      cell.classList.add("cell");
      cell.classList.add(tileType);

      // emoji for tile type
      if (tileType === "tree") cell.textContent = "🌳";
      else if (tileType === "coal") cell.textContent = "⛏️";
      else if (tileType === "berries") cell.textContent = "🍓";
      else if (tileType === "sapling") cell.textContent = "🌱";
      else if (tileType === "solar") cell.textContent = "☀️";
      else if (tileType === "wind") cell.textContent = "🌀";
      else if (tileType === "house") cell.textContent = "🏡";
      else if (tileType === "rabbit") cell.textContent = "🐇"
      else if (tileType === "deer") cell.textContent = "🦌";
      else if (tileType === "bird") cell.textContent = "🐦";
      else if (tileType === "farm") cell.textContent = "🚜";
      else if (tileType === "wheat1") cell.textContent = "🌱";
      else if (tileType === "wheat2") cell.textContent = "🌾";
      else if (tileType === "wheat3") cell.textContent = "🌾✨";  // ripe
      else if (tileType === "carrot1") cell.textContent = "🌱";
      else if (tileType === "carrot2") cell.textContent = "🥕";
      else if (tileType === "carrot3") cell.textContent = "🥕✨";  // ripe

      else cell.textContent = "";

      // player position
      if (x === state.player_x && y === state.player_y) {
        cell.classList.add("player");
        cell.textContent = "🧍";
      }

      // If inside house, override tile style
      if (state.in_house) { 
        cell.classList.add("house-floor");
      }

      grid.appendChild(cell);
    }
  }
}


function setupInput() {
  document.addEventListener("keydown", (e) => {
    if (!state) return;

    if (e.key === "ArrowUp" || e.key === "w") {
      sendMove("up");
    } else if (e.key === "ArrowDown" || e.key === "s") {
      sendMove("down");
    } else if (e.key === "ArrowLeft" || e.key === "a") {
      sendMove("left");
    } else if (e.key === "ArrowRight" || e.key === "d") {
      sendMove("right");
    } else if (e.key === "p") {
      sendPlant();
    } else if (e.key === "1") {
      sendSolar();
    } else if (e.key === "2") {
      sendWind();
    } else if (e.key === "h") {
      toggleHelpMenu();
    } else if (e.key === "3") {
      sendHouse();
    } else if (e.key === "e") {
      sendExitHouse();
    } else if (e.key === "5") {
      sendPlantWheat();
    } else if (e.key === "6") {
      sendPlantCarrot();
    } else if (e.key === "x") {
      sendHarvest();
    } else if (e.key === "4") {
      sendFarm();
    } else if (e.key === " ") {
      // space to collect resource
      e.preventDefault();
      sendCollect();
    }
  });

  document.getElementById("resetBtn").addEventListener("click", () => {
    sendReset();
  });
}

window.addEventListener("load", () => {
  setupInput();
  fetchState();
});
