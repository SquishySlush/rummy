let socket;

let players = [];
let friends = [];
let gameId = null;

document.addEventListener("DOMContentLoaded", () => {
    init();
});

function init() {
    socket = io();

    setupSocketListeners();
    setupUIListeners();

    socket.emit("join_game");
    requestLobbyPlayers();
}

function setupSocketListeners() {
    socket.on("connect", () => {
        socket.emit("join_game");
        requestLobbyPlayers();
    });

    socket.on("lobby_players", (data) => {
        if (!data.success) {
            return;
        }

        players = Array.isArray(data.players) ? data.players : [];
        gameId = data.game_id ?? null;

        renderPlayers();
        renderInviteFriends();
    });

    socket.on("social_list", (data) => {
        if (!data.success) {
            console.error("Failed to load socials");
            return;
        }

        friends = Array.isArray(data.friends) ? data.friends : [];
        renderInviteFriends();
    });

    socket.on("message", (data) => {
        console.log(data.message || "Socket message");
        requestLobbyPlayers();
    });

    socket.on("error", (data) => {
        console.error(data.error || "Socket error");
    });
}

function setupUIListeners() {
    const inviteButton = document.getElementById("invite-button");
    const readyButton = document.getElementById("ready-button");
    const startButton = document.getElementById("start-button");
    const exportButton = document.getElementById("export-button");
    const importButton = document.getElementById("import-button");
    const inviteCloseButton = document.getElementById("invite-close");
    const saveButton = document.getElementById("save-button");

    if (inviteButton) {
        inviteButton.addEventListener("click", openInviteModal);
    }

    if (readyButton) {
        readyButton.addEventListener("click", onReady);
    }

    if (startButton) {
        startButton.addEventListener("click", onStart);
    }

    if (exportButton) {
        exportButton.addEventListener("click", exportRules);
    }

    if (importButton) {
        importButton.addEventListener("click", importRules);
    }

    if (inviteCloseButton) {
        inviteCloseButton.addEventListener("click", closeInviteModal);
    }

    if (saveButton) {
        saveButton.style.display = "none";
    }
}

function requestLobbyPlayers() {
    socket.emit("get_lobby_players");
}

function renderPlayers() {
    const container = document.getElementById("players-list");
    if (!container) {
        return;
    }

    container.innerHTML = "";

    players.forEach((player, index) => {
        const row = document.createElement("div");
        row.className = "friend-row";

        const name = createLabel(
            index === 0 ? `${player.username} (HOST)` : player.username,
            "player-box"
        );

        const status = createLabel(
            player.ready ? "Ready" : "Not Ready",
            "friend-status"
        );

        if (player.ready) {
            name.classList.add("ready");
            status.classList.add("ready");
        }

        row.appendChild(name);
        row.appendChild(status);

        container.appendChild(row);
    });

    updateReadyButton();
    updateStartButton();
}

function updateReadyButton() {
    const readyButton = document.getElementById("ready-button");
    if (!readyButton) {
        return;
    }

    const currentPlayer = getCurrentPlayer();

    if (!currentPlayer) {
        readyButton.disabled = true;
        return;
    }

    if (currentPlayer.ready) {
        readyButton.disabled = true;
        readyButton.textContent = "READY";
    } else {
        readyButton.disabled = false;
        readyButton.textContent = "READY!";
    }
}

function updateStartButton() {
    const startButton = document.getElementById("start-button");
    if (!startButton) {
        return;
    }

    const isHost = currentUserIsHost();
    const allReady = players.length > 0 && players.every((player) => player.ready);

    startButton.disabled = !(isHost && allReady);
}

function getCurrentUserId() {
    return window.CURRENT_USER_ID ?? null;
}

function getCurrentPlayer() {
    const currentUserId = getCurrentUserId();

    if (currentUserId === null) {
        return null;
    }

    return players.find((player) => player.user_id === currentUserId) || null;
}

function currentUserIsHost() {
    const currentUserId = getCurrentUserId();

    if (currentUserId === null || players.length === 0) {
        return false;
    }

    return players[0].user_id === currentUserId;
}

function onReady() {
    if (!gameId) {
        console.error("Missing game id");
        return;
    }

    socket.emit("ready", { game_id: gameId });

    const currentPlayer = getCurrentPlayer();
    if (currentPlayer) {
        currentPlayer.ready = true;
        renderPlayers();
    }

    setTimeout(() => {
        requestLobbyPlayers();
    }, 150);
}

async function onStart(event) {
    if (event) {
        event.preventDefault();
    }

    if (!currentUserIsHost()) {
        console.error("Only the host can start the game");
        return;
    }

    if (!players.length || !players.every((player) => player.ready)) {
        console.error("All players must be ready before starting");
        return;
    }

    const ruleset = collectRules();

    try {
        const response = await fetch("/start_game", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ ruleset })
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            console.error("Failed to start game", data);
            return;
        }

        window.location.href = "/GameState";
    } catch (error) {
        console.error("Failed to start game:", error);
    }
}

function openInviteModal() {
    const modal = document.getElementById("invite-modal");
    if (!modal) {
        return;
    }

    modal.classList.add("active");
    socket.emit("get_socials");
}

function closeInviteModal() {
    const modal = document.getElementById("invite-modal");
    if (!modal) {
        return;
    }

    modal.classList.remove("active");
}

function renderInviteFriends() {
    const container = document.getElementById("invite-friends-list");
    if (!container) {
        return;
    }

    container.innerHTML = "";

    friends.forEach((friend) => {
        const inLobby = players.some((player) => player.user_id === friend.user_id);

        const row = document.createElement("div");
        row.className = "friend-row";

        const name = createLabel(friend.username, "player-box");
        const status = createLabel(inLobby ? "In Lobby" : "Friend", "friend-status");

        if (inLobby) {
            name.classList.add("ready");
            status.classList.add("ready");
        }

        let action;

        if (inLobby) {
            action = createLabel("INVITED", "friend-action");
            action.classList.add("ready");
        } else {
            action = createButton("INVITE", "friend-action", () => {
                socket.emit("invite_to_lobby", { friend_id: friend.user_id });
            });
        }

        row.appendChild(name);
        row.appendChild(status);
        row.appendChild(action);

        container.appendChild(row);
    });
}

function collectRules() {
    const rules = {};
    const controls = document.querySelectorAll("[name]");

    controls.forEach((control) => {
        if (!control.name) {
            return;
        }

        if (control.type === "checkbox") {
            rules[control.name] = control.checked;
            return;
        }

        if (control.name === "wilds") {
            rules[control.name] = parseWilds(control.value);
            return;
        }

        if (control.type === "number") {
            rules[control.name] = control.value === "" ? null : Number(control.value);
            return;
        }

        rules[control.name] = control.value;
    });

    return rules;
}

function applyRules(rules) {
    const controls = document.querySelectorAll("[name]");

    controls.forEach((control) => {
        if (!control.name || !(control.name in rules)) {
            return;
        }

        const value = rules[control.name];

        if (control.type === "checkbox") {
            control.checked = Boolean(value);
            return;
        }

        if (control.name === "wilds") {
            control.value = formatWilds(value);
            return;
        }

        control.value = value ?? "";
    });
}

function parseWilds(value) {
    if (!value || !value.trim()) {
        return [];
    }

    return value
        .split(",")
        .map((entry) => entry.trim())
        .filter((entry) => entry.length > 0)
        .map((entry) => {
            const parts = entry.split(":");
            const rank = parts[0]?.trim() ?? "";
            const numberPart = parts[1] !== undefined ? Number(parts[1].trim()) : 0;

            return [rank, Number.isNaN(numberPart) ? 0 : numberPart];
        });
}

function formatWilds(wilds) {
    if (!Array.isArray(wilds)) {
        return "";
    }

    return wilds
        .map((item) => {
            if (!Array.isArray(item) || item.length < 2) {
                return "";
            }

            return `${item[0]}:${item[1]}`;
        })
        .filter((item) => item.length > 0)
        .join(", ");
}

function exportRules() {
    const rules = collectRules();

    const blob = new Blob([JSON.stringify(rules, null, 2)], {
        type: "application/json"
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "ruleset.json";
    link.click();

    URL.revokeObjectURL(url);
}

function importRules() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "application/json";

    input.addEventListener("change", (event) => {
        const file = event.target.files?.[0];
        if (!file) {
            return;
        }

        const reader = new FileReader();

        reader.onload = () => {
            try {
                const rules = JSON.parse(reader.result);
                applyRules(rules);
            } catch (error) {
                console.error("Invalid JSON file:", error);
            }
        };

        reader.readAsText(file);
    });

    input.click();
}

function createLabel(text, className) {
    const element = document.createElement("div");
    element.className = `box button ${className}`;
    element.textContent = text;
    return element;
}

function createButton(text, className, onClick) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `box button ${className}`;
    button.textContent = text;
    button.addEventListener("click", onClick);
    return button;
}