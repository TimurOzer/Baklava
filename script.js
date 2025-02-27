let logAdded = false;  // Yeni logun zaten eklenip eklenmediğini kontrol etmek için bir bayrak

function addLog(message) {
    const logContainer = document.getElementById("logs");
    const logEntry = document.createElement("p");
    const currentDate = new Date().toLocaleString();
    logEntry.textContent = `${currentDate}: ${message}`;
    logContainer.appendChild(logEntry);
}

// Sunucudan logları çekip eklemek için
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

window.onload = fetchLogs;  // Sayfa yüklendiğinde logları çekmeye başla
