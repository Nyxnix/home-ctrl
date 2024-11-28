async function fetchStatus() {
    try {
        const response = await fetch("/get_status", { method: "POST" });
        const data = await response.json();
        const button = document.getElementById("toggleButton");
        if (data.status == "muted") {
            button.textContent = "Muted";
            button.classList.add("muted");
        } else {
            button.textContent = "Mute";
            button.classList.remove("muted");
        }
    } catch (error) {
        console.error("Error fetching status:", error);
    }
}

async function fetchStatus() {
    try {
        const response = await fetch("/get_status", { method: "POST" });
        const data = await response.json();
        const button = document.getElementById("toggleButton");
        if (data.status == "muted") {
            button.textContent = "Muted";
            button.classList.add("muted");
        } else {
            button.textContent = "Mute";
            button.classList.remove("muted");
        }
    } catch (error) {
        console.error("Error fetching status:", error);
    }
}

async function toggleMicrophone() {
    try {
        const response = await fetch("/toggle_microphone", { method: "POST" });
        const data = await response.json();
        const button = document.getElementById("toggleButton");
        button.textContent = data.status === "muted" ? "Unmute" : "Mute";
    } catch (error) {
        console.error("Error toggling microphone:", error);
    }
}

setInterval(fetchStatus, 500);

window.onload = fetchStatus;

// Unmute the microphone
async function unmuteMicrophone() {
    try {
        const response = await fetch("/unmute_microphone", { method: "POST" });
        const data = await response.json();
        fetchStatus();
    } catch (error) {
        console.error("Error unmuting microphone:", error);
    }
}

// Mute the microphone
async function muteMicrophone() {
    try {
        const response = await fetch("/mute_microphone", { method: "POST" });
        const data = await response.json();
        fetchStatus();
    } catch (error) {
        console.error("Error muting microphone:", error);
    }
}

// Fetch initial status on page load
window.onload = fetchStatus;