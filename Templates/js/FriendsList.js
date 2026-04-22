let socket;

let socials = {
    friends: [],
    pending: [],
    others: []
};

document.addEventListener("DOMContentLoaded", () => {
    init();
});

function init() {
    socket = io();

    setupListeners();
    requestSocials();
}

function setupListeners() {
    const searchInput = document.getElementById("friend-search");

    searchInput.addEventListener("input", renderSocialList);

    socket.on("connect", () => {
        requestSocials();
    });

    socket.on("social_list", (data) => {
        if (!data.success) return;

        socials.friends = data.friends || [];
        socials.pending = data.pending || [];
        socials.others = data.others || [];

        renderSocialList();
    });

    socket.on("friend_request_received", requestSocials);
    socket.on("friend_request_accepted", requestSocials);
    socket.on("friend_request_rejected", requestSocials);

    socket.on("error", (data) => {
        console.error(data.error || "Socket error");
    });
}

function requestSocials() {
    socket.emit("get_socials");
}

function renderSocialList() {
    const container = document.getElementById("friends-list");
    const query = document.getElementById("friend-search").value.toLowerCase();

    container.innerHTML = "";

    const matches = (u) =>
        u.username && u.username.toLowerCase().includes(query);

    renderFriends(container, socials.friends.filter(matches));
    renderPending(container, socials.pending.filter(matches));
    renderOthers(container, socials.others.filter(matches));
}

function renderFriends(container, friends) {
    friends.forEach((f) => {
        const row = createRow(
            f.username,
            createLabel("Offline", "friend-status"),
            createEmpty()
        );

        container.appendChild(row);
    });
}

function renderPending(container, pending) {
    pending.forEach((p) => {
        let statusEl;
        let actionEl;

        if (p.direction === "incoming") {
            statusEl = createButton("ACCEPT", "friend-status", () => {
                socket.emit("accept_request", { friend_id: p.user_id });
            });

            actionEl = createButton("DECLINE", "friend-action", () => {
                socket.emit("reject_request", { friend_id: p.user_id });
            });
        } else {
            statusEl = createLabel("Pending", "friend-status");
            actionEl = createEmpty();
        }

        const row = createRow(p.username, statusEl, actionEl);
        container.appendChild(row);
    });
}

function renderOthers(container, others) {
    others.forEach((u) => {
        const actionEl = createButton("SEND REQUEST", "friend-action", () => {
            socket.emit("friend_request", { friend_id: u.user_id });
        });

        const row = createRow(
            u.username,
            createLabel("Offline", "friend-status"),
            actionEl
        );

        container.appendChild(row);
    });
}

function createRow(username, statusEl, actionEl) {
    const row = document.createElement("div");
    row.className = "friend-row";

    const player = createLabel(username, "player-box");

    row.appendChild(player);
    row.appendChild(statusEl);
    row.appendChild(actionEl);

    return row;
}

function createLabel(text, className) {
    const el = document.createElement("div");
    el.className = `box ${className}`;
    el.textContent = text;
    return el;
}

function createButton(text, className, onClick) {
    const btn = document.createElement("button");
    btn.className = `box button ${className}`;
    btn.textContent = text;
    btn.onclick = onClick;
    return btn;
}

function createEmpty() {
    const el = document.createElement("div");
    el.className = "friend-action";
    return el;
}