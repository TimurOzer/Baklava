let logAdded = false;

function addLog(message) {
    const logContainer = document.getElementById("logs");
    const logEntry = document.createElement("p");
    const currentDate = new Date().toLocaleString();
    logEntry.textContent = `${currentDate}: ${message}`;
    logContainer.appendChild(logEntry);
}

// Gerçek logları sunucudan alıp eklemek için
function fetchLogs() {
    fetch('http://127.0.0.1:5001/get_logs')  // Sunucunun API endpointi
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                data.forEach(logMessage => {
                    addLog(logMessage);  // Gelen her logu ekle
                });
            }
        })
        .catch(error => console.error("Log verileri alınamadı:", error));
}

// Simulate adding a log when server pushes
function simulateLog() {
    setInterval(() => {
        fetchLogs();  // Sunucudan yeni logları al
    }, 5000);  // Her 5 saniyede bir log al ve ekle
}

window.onload = simulateLog;
