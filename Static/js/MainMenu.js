document.addEventListener("DOMContentLoaded", () => {
    await ensureGuestSession();
    setupCreateLobbyLinks();
    setupLobbyInvites();
});

async function postJson(urls, payload = {}) {
    for (const url of urls) {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await response.json().catch(() => ({}));
        if (response.ok) return data;
        if (response.status !== 404) throw new Error(data.error || data.message || "Request failed");
    }
    throw new Error("Request failed");
}

async function ensureGuestSession() {
    try {
        await postJson(["/auth/guest"]);
    } catch (error) {
        console.error(error.message || "Could not create guest session");
    }
}

function collectDefaultRules() {
    return {};
}

function setupCreateLobbyLinks() {
    document.querySelectorAll("a[href='/GameLobby']").forEach((link) => {
        link.addEventListener("click", async (event) => {
            event.preventDefault();
            try {
                await ensureGuestSession();
                await postJson(["/game/create_game", "/create_game"], { ruleset: collectDefaultRules(), seed: null });
            } catch (error) {
                // If the page route creates the lobby itself, still allow navigation.
                console.warn(error.message || "Create game request failed");
            }
            window.location.href = "/GameLobby";
        });
    });
}

function setupLobbyInvites() {
    if (typeof io !== "function") return;
    const socket = io();
    socket.on("lobby_invite_received", (data) => {
        const from = data?.from_username || "A friend";
        if (confirm(`${from} invited you to a lobby. Join?`)) {
            socket.emit("accept_lobby_invite", { game_id: data.game_id });
        }
    });
    socket.on("lobby_joined", () => { window.location.href = "/GameLobby"; });
}
