document.addEventListener("DOMContentLoaded", () => {
    await EnsureUserSession();
});

async function EnsureUserSession() {
    try {
        const response = await fetch("/auth/guest", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        if (!response.ok) {
            console.error("Guest Initialisation Failed", data);
            return;
        }

        console.log("Session Ready:", data);
    } catch (error) {
        console.error("Failed To Create Guest Session:", error);
    }
}