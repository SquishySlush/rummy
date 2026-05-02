document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("signup-button");
    button?.addEventListener("click", signUp);
    document.addEventListener("keydown", (e) => { if (e.key === "Enter") signUp(); });
});

function getSignUpFields() {
    const username = document.querySelector("#username-field, input[name='username']")?.value.trim();
    const email = document.querySelector("#email-field, input[name='email'], input[type='email']")?.value.trim();
    const passwordInputs = [...document.querySelectorAll("input[type='password'], input[name='password']")];
    const password = passwordInputs.at(-1)?.value;
    return { username, email, password };
}

async function postJson(urls, payload) {
    for (const url of urls) {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await response.json().catch(() => ({}));
        if (response.ok) return data;
        if (response.status !== 404) throw new Error(data.error || data.message || "Sign up failed");
    }
    throw new Error("Sign up failed");
}

async function signUp() {
    const { username, email, password } = getSignUpFields();
    if (!username || !email || !password) {
        alert("Fill in all fields");
        return;
    }

    try {
        await postJson(["/auth/sign_up", "/sign_up"], { username, email, password });
        window.location.href = "/";
    } catch (error) {
        alert(error.message || "Sign up failed");
    }
}
