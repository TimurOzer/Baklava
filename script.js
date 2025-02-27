let logAdded = false;  // Yeni logun zaten eklenip eklenmediğini kontrol etmek için bir bayrak

function addLog(message) {
    const logContainer = document.getElementById("logs");

    // Sadece yeni bir log geldiğinde mesaj ekle
    if (!logAdded) {
        const logEntry = document.createElement("p");
        const currentDate = new Date().toLocaleString();
        logEntry.textContent = `${currentDate}: ${message}`;
        logContainer.appendChild(logEntry);
        logAdded = true;  // Yeni log eklendi, bayrağı güncelle
    }
}

// Simulate adding a log when server pushes
function simulateLog() {
    setInterval(() => {
        if (logAdded) {
            logAdded = false;  // Log zaten eklenmişse, bayrağı sıfırla
            addLog("Yeni bir log kaydedildi.");  // Yeni log mesajı ekle
        }
    }, 5000);  // Her 5 saniyede bir log eklemeye çalış
}

window.onload = simulateLog;
