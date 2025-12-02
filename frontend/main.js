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


function toggleHelpMenu() {
  const menu = document.getElementById("helpMenu");
  menu.classList.toggle("hidden");
}


function render() {
  if (!state) return;

  // HUD
  document.getElementById("eco").textContent = state.ecosystem_health;
  document.getElementById("energy").textContent = state.energy;
  document.getElementById("food").textContent = state.food;
  document.getElementById("wood").textContent = state.wood;
  document.getElementById("coal").textContent = state.coal;

  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  grid.style.gridTemplateColumns = `repeat(${state.width}, 32px)`;

  for (let y = 0; y < state.height; y++) {
    for (let x = 0; x < state.width; x++) {
      const cell = document.createElement("div");
      const tileType = state.tiles[y][x];

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
      else cell.textContent = "";


      // player position
      if (x === state.player_x && y === state.player_y) {
        cell.classList.add("player");
        cell.textContent = "🧍";
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
