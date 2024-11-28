async function fetchAllStatuses() {
    try {
        const response = await fetch("/get_all_statuses", { method: "POST" });
        const data = await response.json();
        console.log("All statuses:", data);

        // Update mic status
        const micButton = document.getElementById("toggleButton");
        if (data.mic_status === "muted") {
            micButton.textContent = "Muted";
            micButton.classList.add("muted");
        } else if (data.mic_status === "unmuted") {
            micButton.textContent = "Mute";
            micButton.classList.remove("muted");
        } else {
            console.error("Unexpected mic status:", data.mic_status);
        }

        // Update mic monitor status
        const micMonitorButton = document.getElementById("micMonitorButton");
        if (data.mic_monitor_status === "active") {
            micMonitorButton.classList.add("active");
        } else if (data.mic_monitor_status === "inactive") {
            micMonitorButton.classList.remove("active");
        } else {
            console.error("Unexpected mic monitor status:", data.mic_monitor_status);
        }

        // Update guitar monitor status
        const guitarMonitorButton = document.getElementById("guitarMonitorButton");
        if (data.guitar_monitor_status === "muted") {
            guitarMonitorButton.classList.add("active");
        } else {
            guitarMonitorButton.classList.remove("active");
        }

    } catch (error) {
        console.error("Error fetching all statuses:", error);
    }
}

window.onload = fetchAllStatuses;
setInterval(fetchAllStatuses, 1000);

async function toggleMicrophone() {
    try {
        const response = await fetch("/toggle_microphone", { method: "POST" });
        const data = await response.json();
        const button = document.getElementById("toggleButton");

        if (data.status === "muted") {
            button.textContent = "Unmute";
        } else {
            button.textContent = "Mute";
        }
    } catch (error) {
        console.error("Error toggling microphone:", error);
    }
}

async function unmuteMicrophone() {
    try {
        const response = await fetch("/unmute_microphone", { method: "POST" });
        const data = await response.json();
    } catch (error) {
        console.error("Error unmuting microphone:", error);
    }
}

async function muteMicrophone() {
    try {
        const response = await fetch("/mute_microphone", { method: "POST" });
        const data = await response.json();
    } catch (error) {
        console.error("Error muting microphone:", error);
    }
}

async function toggleMicMonitor() {
    try {
        const response = await fetch("/mic_monitor", { method: "POST" });
        const data = await response.json();
        const micMonitorButton = document.getElementById("micMonitorButton");

        if (data.status === "active") {
            micMonitorButton.classList.add("active");
        } else {
            micMonitorButton.classList.remove("active");
        }
    } catch (error) {
        console.error("Error toggling microphone monitor:", error);
    }
}

async function toggleGuitarMonitor() {
    try {
        const response = await fetch("/guitar_monitor", { method: "POST" });
        const data = await response.json();
        const guitarMonitorButton = document.getElementById("guitarMonitorButton");
        if (data.status == "muted") {
            guitarMonitorButton.classList.add("active");
        } else {
            guitarMonitorButton.classList.remove("active");
        }
    } catch (error) {
        console.error("Error toggling guitar monitor:", error);
    }
}

