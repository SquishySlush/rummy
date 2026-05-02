document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("login-button");
    button?.addEventListener("click", login);
    document.addEventListener("keydown", (e) => { if (e.key === "Enter") login(); });
});

async function postJson(urls, payload) {
    const list = Array.isArray(urls) ? urls : [urls];
    let lastData = {};
    for (const url of list) {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await response.json().catch(() => ({}));
        if (response.ok) return data;
        lastData = data;
        if (response.status !== 404) throw new Error(data.error || data.message || "Request failed");
    }
    throw new Error(lastData.error || lastData.message || "Request failed");
}

async function login() {
    const username = document.getElementById("username-field")?.value.trim();
    const password = document.getElementById("password-field")?.value;

    if (!username || !password) {
        alert("Fill in all fields");
        return;
    }

    try {
        await postJson(["/auth/login", "/login"], { username, password });
        window.location.href = "/";
    } catch (error) {
        alert(error.message || "Login failed");
    }
}
