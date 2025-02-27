// Simulate log updates
function addLog(message) {
    const logContainer = document.getElementById("logs");
    const logEntry = document.createElement("p");
    const currentDate = new Date().toLocaleString();
    logEntry.textContent = `${currentDate}: ${message}`;
    logContainer.appendChild(logEntry);
}

// Simulate adding a log when server pushes
function simulateLog() {
    setInterval(() => {
        addLog("Yeni bir log kaydedildi.");
    }, 5000);  // Every 5 seconds, simulate a log update
}

window.onload = simulateLog;
