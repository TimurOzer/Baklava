function addLog(logData) {
    const logContainer = document.getElementById("logs");

    // Log kartını oluştur
    const logCard = document.createElement("div");
    logCard.className = "log-card";

    // Timestamp
    const timestamp = document.createElement("h4");
    timestamp.textContent = `Zaman: ${logData.timestamp}`;
    logCard.appendChild(timestamp);

    // Previous Hash
    const previousHash = document.createElement("p");
    previousHash.textContent = `Önceki Hash: ${logData.previous_hash}`;
    logCard.appendChild(previousHash);

    // Current Hash
    const currentHash = document.createElement("p");
    currentHash.textContent = `Mevcut Hash: ${logData.hash}`;
    logCard.appendChild(currentHash);

    // Transactions
    const transactionsHeader = document.createElement("p");
    transactionsHeader.textContent = "İşlemler:";
    logCard.appendChild(transactionsHeader);

    if (logData.transactions && logData.transactions.length > 0) {
        logData.transactions.forEach(transaction => {
            if (transaction && transaction.sender && transaction.recipient && transaction.amount) {
                const transactionDiv = document.createElement("div");
                transactionDiv.className = "transaction";
                transactionDiv.innerHTML = `
                    <p>Gönderen: ${transaction.sender}</p>
                    <p>Alıcı: ${transaction.recipient}</p>
                    <p>Miktar: ${transaction.amount}</p>
                `;
                logCard.appendChild(transactionDiv);
            }
        });
    } else {
        const noTransactions = document.createElement("p");
        noTransactions.textContent = "İşlem bulunamadı.";
        logCard.appendChild(noTransactions);
    }

    // Log kartını log container'a ekle
    logContainer.appendChild(logCard);
}

// Sunucudan logları çekip eklemek için
function fetchLogs() {
    fetch('http://127.0.0.1:5002/get_logs')
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                data.forEach(log => {
                    addLog(log);  // Her logu ekle
                });
            } else {
                console.log("Log bulunamadı.");
            }
        })
        .catch(error => console.error("Log verileri alınamadı:", error));
}

window.onload = fetchLogs;  // Sayfa yüklendiğinde logları çekmeye başla