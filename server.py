import os
from flask import Flask, jsonify
import json
import time

app = Flask(__name__)

# Logların saklanacağı dizini oluşturuyoruz
log_folder = "client_logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Log dosyasının yolu
log_file_path = os.path.join(log_folder, "log.txt")

# Örnek log ekleme fonksiyonu
def append_log(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{current_time}: {message}\n")

# Sunucu başlatıldığında bir başlangıç logu ekliyoruz
append_log("Server started successfully.")

# Logları almak için API endpoint
@app.route("/get_logs", methods=["GET"])
def get_logs():
    try:
        # Log dosyasını okuma
        with open(log_file_path, "r") as log_file:
            logs = log_file.readlines()
        return jsonify(logs)
    except Exception as e:
        # Eğer hata olursa error mesajı döneriz
        return jsonify({"error": str(e)}), 500

# Sunucuya log eklemek için bir endpoint
@app.route("/add_log", methods=["POST"])
def add_log():
    try:
        # Log verisi almak
        new_log = json.loads(request.data.decode('utf-8'))
        message = new_log.get('message', 'No message')
        append_log(message)
        return jsonify({"status": "success", "message": "Log added."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Sunucu çalıştırma
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)  # Flask server'ı başlatıyoruz
