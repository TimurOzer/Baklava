let logAdded = false;  // Yeni log eklenip eklenmediğini kontrol etmek için bayrak

function addLog(message) {
    const logContainer = document.getElementById("logs");
    const logEntry = document.createElement("p");
    const currentDate = new Date().toLocaleString();
    logEntry.textContent = `${currentDate}: ${message}`;
    logContainer.appendChild(logEntry);
    logAdded = true;  // Yeni log eklenmişse bayrağı güncelle
}

// Simulate adding a log when server pushes
function simulateLog() {
    setInterval(() => {
        // Log eklenmemişse, bir log ekle
        if (!logAdded) {
            addLog("Yeni bir log kaydedildi.");
        } else {
            logAdded = false;  // Log eklenmişse bayrağı sıfırla
        }
    }, 5000);  // Her 5 saniyede bir log eklemeye çalış
}

window.onload = simulateLog;
