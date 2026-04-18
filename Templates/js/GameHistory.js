// let socket;

// let historyList = [];

// document.addEventListener("DOMContentLoaded", () => {
//     init();
// });

// function init() {
//     socket = io();

//     setupListeners();
//     requestHistory();
// }

// function setupListeners() {
//     const searchInput = document.getElementById("history-search");

//     searchInput.addEventListener("input", renderHistoryList);

//     socket.on("connect", () => {
//         requestHistory();
//     });

//     socket.on("game_history", (data) => {
//         if (!data.success) {
//             console.error(data.error || "Failed to load game history");
//             return;
//         }

//         historyList = Array.isArray(data.history) ? data.history : [];
//         renderHistoryList();
//     });

//     socket.on("error", (data) => {
//         console.error(data.error || "Socket error");
//     });
// }

// function requestHistory() {
//     socket.emit("get_history");
// }

// function renderHistoryList() {
//     const container = document.getElementById("game-history");
//     const query = document.getElementById("history-search").value.trim().toLowerCase();

//     container.innerHTML = "";

//     const filteredHistory = historyList.filter((game) => matchesSearch(game, query));

//     filteredHistory.forEach((game) => {
//         const row = createHistoryRow(game);
//         container.appendChild(row);
//     });
// }

// function matchesSearch(game, query) {
//     if (!query) {
//         return true;
//     }

//     const gameId = String(game.game_id || "").toLowerCase();
//     const role = String(game.role || "").toLowerCase();
//     const ruleset = String(game.ruleset || "").toLowerCase();
//     const result = String(game.result || "").toLowerCase();

//     return (
//         gameId.includes(query) ||
//         role.includes(query) ||
//         ruleset.includes(query) ||
//         result.includes(query)
//     );
// }

// function createHistoryRow(game) {
//     const row = document.createElement("div");
//     row.className = "history-row";

//     const gameIdEl = createLabel(game.game_id ?? "Game ID", "game-box");
//     const roleEl = createLabel(game.role ?? "ROLE", "game-role");
//     const rulesetEl = createLabel(game.ruleset ?? "Ruleset", "game-ruleset");
//     const resultEl = createLabel(formatResult(game.result), "game-result");

//     row.appendChild(gameIdEl);
//     row.appendChild(roleEl);
//     row.appendChild(rulesetEl);
//     row.appendChild(resultEl);

//     return row;
// }

// function createLabel(text, className) {
//     const el = document.createElement("div");
//     el.className = `box button ${className}`;
//     el.textContent = text;
//     return el;
// }

// function formatResult(result) {
//     if (!result) {
//         return "RESULT";
//     }

//     return String(result);
// }