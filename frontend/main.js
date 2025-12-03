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
  render();
  positionHelpMenu();
}

async function sendExitHouse() {
  const res = await fetch("/api/exit_house", { method: "POST" });
  state = await res.json();
  render();
}

async function sendCollect() {
  const res = await fetch("/api/collect", { method: "POST" });
  state = await res.json();
  render();
}

async function sendReset() {
  const res = await fetch("/api/reset", { method: "POST" });
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
  state = await res.json();
  render();
}

async function sendPlantCarrot() {
  const res = await fetch("/api/plant_carrot", { method: "POST" });
  state = await res.json();
  render();
}

async function sendHarvest() {
  const res = await fetch("/api/harvest", { method: "POST" });
  state = await res.json();
  render();
}

async function sendFarm() {
  const res = await fetch("/api/farm", { method: "POST" });
  state = await res.json();
  render();
}


/* ---------------- HELP MENU POSITIONING ---------------- */

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
  const tileSize = 34; // tile + gap

  const playerCenterY =
    gridRect.top + state.player_y * tileSize + tileSize / 2;

  const menuHeight = menu.offsetHeight;

  let newTop = playerCenterY - menuHeight / 2;

  newTop = Math.max(20, Math.min(window.innerHeight - menuHeight - 20, newTop));

  menu.style.top = `${newTop}px`;
}


/* ---------------- RENDERING ---------------- */

function render() {
  if (!state) return;

  let gridData, width, height;

  /* ----- day/night ----- */
  if (state.time_of_day === "day") {
    document.body.classList.add("daytime");
    document.body.classList.remove("nighttime");
    document.documentElement.style.setProperty(
      "--tile-border",
      "1px solid rgba(0,0,0,0.25)"
    );
  } else {
    document.body.classList.add("nighttime");
    document.body.classList.remove("daytime");
    document.documentElement.style.setProperty(
      "--tile-border",
      "1px solid rgba(255,255,255,0.12)"
    );
  }

  /* ----- in house vs overworld ----- */
  if (state.in_house) {
    gridData = state.house_tiles;
    width = state.house_width;
    height = state.house_height;
  } else {
    gridData = state.tiles;
    width = state.width;
    height = state.height;
  }

  /* ----- biome body class ----- */
  document.body.classList.remove("forest", "tundra", "desert", "swamp");
  document.body.classList.add(state.current_biome);

  /* ----- HUD ----- */
  document.getElementById("eco").textContent = state.ecosystem_health;
  document.getElementById("energy").textContent = state.energy;
  document.getElementById("food").textContent = state.food;
  document.getElementById("wood").textContent = state.wood;
  document.getElementById("coal").textContent = state.coal;

  /* ----- draw grid ----- */
  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  grid.style.gridTemplateColumns = `repeat(${width}, 32px)`;

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const cell = document.createElement("div");
      const tileType = gridData[y][x];

      cell.classList.add("cell", tileType);

      /* ----- tile emoji logic ----- */
      let emoji = null;

      // forest biome
      if (state.current_biome === "forest") {
        if (tileType === "tree") emoji = "🌳";
        else if (tileType === "berries") emoji = "🍓";
        else if (tileType === "sapling") emoji = "🌱";
        else if (tileType === "coal") emoji = "⛏️";
      }

      // desert
      if (state.current_biome === "desert") {
        if (tileType === "sand") emoji = "🏜️";
      }

      // tundra
      if (state.current_biome === "tundra") {
        if (tileType === "snow") emoji = "❄️";
        else if (tileType === "ice") emoji = "🧊";
      }

      // swamp
      if (state.current_biome === "swamp") {
        if (tileType === "mud") emoji = "🪵";
      }

      // global (crops, farm, house, etc.)
      if (!emoji) {
        if (tileType === "solar") emoji = "☀️";
        else if (tileType === "wind") emoji = "🌀";
        else if (tileType === "house") emoji = "🏡";
        else if (tileType === "farm") emoji = "🚜";
        else if (tileType === "rabbit") emoji = "🐇";
        else if (tileType === "deer") emoji = "🦌";
        else if (tileType === "bird") emoji = "🐦";
        else if (tileType === "wheat1") emoji = "🌱";
        else if (tileType === "wheat2") emoji = "🌾";
        else if (tileType === "wheat3") emoji = "🌾✨";
        else if (tileType === "carrot1") emoji = "🌱";
        else if (tileType === "carrot2") emoji = "🥕";
        else if (tileType === "carrot3") emoji = "🥕✨";
      }

      cell.textContent = emoji || "";

      /* ----- player ----- */
      if (x === state.player_x && y === state.player_y) {
        cell.classList.add("player");
        cell.textContent = "🧍";
      }

      /* ----- inside house override ----- */
      if (state.in_house) {
        cell.classList.add("house-floor");
      }

      grid.appendChild(cell);
    }
  }
}


/* ---------------- INPUT ---------------- */

function setupInput() {
  document.addEventListener("keydown", (e) => {
    if (!state) return;

    if (e.key === "ArrowUp" || e.key === "w") sendMove("up");
    else if (e.key === "ArrowDown" || e.key === "s") sendMove("down");
    else if (e.key === "ArrowLeft" || e.key === "a") sendMove("left");
    else if (e.key === "ArrowRight" || e.key === "d") sendMove("right");
    else if (e.key === "p") sendPlant();
    else if (e.key === "1") sendSolar();
    else if (e.key === "2") sendWind();
    else if (e.key === "h") toggleHelpMenu();
    else if (e.key === "3") sendHouse();
    else if (e.key === "e") sendExitHouse();
    else if (e.key === "5") sendPlantWheat();
    else if (e.key === "6") sendPlantCarrot();
    else if (e.key === "x") sendHarvest();
    else if (e.key === "4") sendFarm();
    else if (e.key === " ") {
      e.preventDefault();
      sendCollect();
    }
  });

  document.getElementById("resetBtn").addEventListener("click", sendReset);
}


/* ---------------- INIT ---------------- */

window.addEventListener("load", () => {
  setupInput();
  fetchState();
});

