let socket;
let historyItems = [];

window.addEventListener("DOMContentLoaded", () => {
    socket = io();
    searchInput()?.addEventListener("input", renderHistory);
    socket.on("connect", () => socket.emit("get_history"));
    socket.on("game_history", (data) => {
        if (!data?.success) return showHistoryMessage(data?.error || "Could not load game history");
        historyItems = Array.isArray(data.history) ? data.history : [];
        renderHistory();
    });
    socket.on("error", (data) => showHistoryMessage(data?.error || "Socket error"));
});

function searchInput() {
    return document.getElementById("history-search") || document.getElementById("friend-search");
}

function renderHistory() {
    const container = document.getElementById("game-history");
    if (!container) return;
    const query = (searchInput()?.value || "").trim().toLowerCase();
    const items = historyItems.filter((game) => matches(game, query));

    container.innerHTML = "";
    if (!items.length) return showHistoryMessage("No game history found");
    items.forEach((game) => container.appendChild(historyRow(game)));
}

function matches(game, query) {
    if (!query) return true;
    return [game.game_id, game.role, game.ruleset, game.result, game.winner, game.created_at]
        .some((value) => String(value ?? "").toLowerCase().includes(query));
}

function historyRow(game) {
    const row = document.createElement("div");
    row.className = "history-row";
    row.appendChild(cell(`Game ${game.game_id ?? ""}`, "game-box"));
    row.appendChild(cell(game.role || "Player", "game-role"));
    row.appendChild(cell(formatRuleset(game.ruleset), "game-ruleset"));
    row.appendChild(cell(game.result || game.outcome || "Finished", "game-result"));
    return row;
}

function formatRuleset(ruleset) {
    if (!ruleset) return "Ruleset";
    if (typeof ruleset === "string") return ruleset;
    return ruleset.name || "Custom Rules";
}

function cell(text, className) {
    const element = document.createElement("div");
    element.className = `box button ${className}`;
    element.textContent = text;
    return element;
}

function showHistoryMessage(message) {
    const container = document.getElementById("game-history");
    if (!container) return;
    container.innerHTML = "";
    container.appendChild(cell(message, "game-box"));
}
