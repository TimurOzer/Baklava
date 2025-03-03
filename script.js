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

// Sunucu durumunu kontrol etme fonksiyonu
function checkServerStatus() {
    fetch('http://127.0.0.1:5002/status')
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            const statusText = document.getElementById("status-text");
            if (data.status === "Online") {
                statusText.textContent = "Online";
                statusText.style.color = "green";
            } else {
                statusText.textContent = "Offline";
                statusText.style.color = "red";
            }
        })
        .catch(error => {
            const statusText = document.getElementById("status-text");
            statusText.textContent = "Offline";
            statusText.style.color = "red";
            console.error("Error checking server status:", error);
        });
}
// Coin transferi yapma
document.getElementById("transfer-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const sender = document.getElementById("sender").value;
    const recipient = document.getElementById("recipient").value;
    const amount = parseFloat(document.getElementById("amount").value);

    fetch('http://127.0.0.1:5002/transfer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sender, recipient, amount }),
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("transfer-status").textContent = data.message || data.error;
        })
        .catch(error => {
            console.error("Transfer hatası:", error);
        });
});

// Bakiye sorgulama
document.getElementById("balance-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const address = document.getElementById("address").value;

    fetch(`http://127.0.0.1:5002/balance/${address}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("balance-result").textContent = `Bakiye: ${data.balance}`;
        })
        .catch(error => {
            console.error("Bakiye sorgulama hatası:", error);
        });
});

// Yeni cüzdan oluşturma
document.getElementById("create-wallet-btn").addEventListener("click", function () {
    fetch('http://127.0.0.1:5002/create_wallet')
        .then(response => response.json())
        .then(data => {
            document.getElementById("wallet-address").textContent = data.address;
            document.getElementById("wallet-private-key").textContent = data.private_key;
            alert(data.message);
        })
        .catch(error => {
            console.error("Cüzdan oluşturma hatası:", error);
        });
});

// Cüzdan bilgilerini yükleme
function loadWalletInfo() {
    fetch('http://127.0.0.1:5002/wallet_info')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById("wallet-address").textContent = data.address;
                document.getElementById("wallet-private-key").textContent = data.private_key;
            }
        })
        .catch(error => {
            console.error("Cüzdan bilgileri yüklenirken hata:", error);
        });
}

// Sayfa yüklendiğinde cüzdan bilgilerini yükle
window.onload = function () {
    loadWalletInfo();
    checkServerStatus();
    fetchLogs();  // Logları çekmeye başla
};