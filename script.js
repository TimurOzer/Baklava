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
            const transactionDiv = document.createElement("div");
            transactionDiv.className = "transaction";
            transactionDiv.innerHTML = `
                <p>Gönderen: ${transaction.sender}</p>
                <p>Alıcı: ${transaction.recipient}</p>
                <p>Miktar: ${transaction.amount}</p>
            `;
            logCard.appendChild(transactionDiv);
        });
    } else {
        const noTransactions = document.createElement("p");
        noTransactions.textContent = "İşlem bulunamadı.";
        logCard.appendChild(noTransactions);
    }

    // Log kartını log container'a ekle
    logContainer.appendChild(logCard);
}