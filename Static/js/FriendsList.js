let socket;
let socials = { friends: [], pending: [], others: [] };

window.addEventListener("DOMContentLoaded", () => {
    socket = io();
    bindEvents();
});

function bindEvents() {
    document.getElementById("friend-search")?.addEventListener("input", renderSocials);

    socket.on("connect", requestSocials);
    socket.on("social_list", (data) => {
        if (!data?.success) return showMessage(data?.error || "Could not load socials");
        socials = {
            friends: data.friends || [],
            pending: data.pending || [],
            others: data.others || []
        };
        renderSocials();
    });

    ["friend_request_received", "friend_request_accepted", "friend_request_rejected"].forEach((eventName) => {
        socket.on(eventName, requestSocials);
    });
    socket.on("error", (data) => showMessage(data?.error || "Socket error"));
}

function requestSocials() {
    socket.emit("get_socials");
}

function renderSocials() {
    const list = document.getElementById("friends-list");
    if (!list) return;
    const query = (document.getElementById("friend-search")?.value || "").trim().toLowerCase();
    const matches = (user) => !query || String(user.username || "").toLowerCase().includes(query);

    list.innerHTML = "";
    addSection(list, "Friends", socials.friends.filter(matches), renderFriendRow);
    addSection(list, "Pending", socials.pending.filter(matches), renderPendingRow);
    addSection(list, "Players", socials.others.filter(matches), renderOtherRow);

    if (!list.children.length) showMessage("No players found");
}

function addSection(container, title, items, renderer) {
    if (!items.length) return;
    const heading = document.createElement("div");
    heading.className = "box friend-status";
    heading.textContent = title;
    container.appendChild(heading);
    items.forEach((item) => container.appendChild(renderer(item)));
}

function renderFriendRow(friend) {
    return row(label(friend.username, "player-box"), label("Friend", "friend-status"), emptyAction());
}

function renderPendingRow(person) {
    if (person.direction === "incoming") {
        return row(
            label(person.username, "player-box"),
            button("ACCEPT", "friend-status", () => socket.emit("accept_request", { friend_id: person.user_id })),
            button("DECLINE", "friend-action", () => socket.emit("reject_request", { friend_id: person.user_id }))
        );
    }
    return row(label(person.username, "player-box"), label("Pending", "friend-status"), emptyAction());
}

function renderOtherRow(user) {
    return row(
        label(user.username, "player-box"),
        label("Player", "friend-status"),
        button("ADD", "friend-action", () => socket.emit("friend_request", { friend_id: user.user_id }))
    );
}

function row(...children) {
    const element = document.createElement("div");
    element.className = "friend-row";
    children.forEach((child) => element.appendChild(child));
    return element;
}

function label(text, className) {
    const element = document.createElement("div");
    element.className = `box button ${className}`;
    element.textContent = text || "Unknown";
    return element;
}

function button(text, className, onClick) {
    const element = document.createElement("button");
    element.type = "button";
    element.className = `box button ${className}`;
    element.textContent = text;
    element.addEventListener("click", onClick);
    return element;
}

function emptyAction() {
    const element = document.createElement("div");
    element.className = "friend-action";
    return element;
}

function showMessage(message) {
    const list = document.getElementById("friends-list");
    if (!list) return;
    list.innerHTML = "";
    list.appendChild(label(message, "player-box"));
}
