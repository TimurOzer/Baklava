import socket
import json
import os
from blockchain import Blockchain  # Blockchain sınıfınızı buraya dahil etmelisiniz
from flask import Flask, jsonify, request
from flask_cors import CORS  # CORS kütüphanesini dahil et
import time
from threading import Thread
from wallet import Wallet, create_wallet  # Wallet sınıfını ve fonksiyonunu içe aktar

app = Flask(__name__)
CORS(app)  # CORS'u aktif et

app.config['DEBUG'] = True  # Debug modunu aktif et

# Log dosyalarının bulunduğu klasör
log_folder = "client_logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Blockchain'i başlatıyoruz
blockchain = Blockchain()

# Sunucu durumunu kontrol etmek için API endpoint
@app.route('/status', methods=['GET'])
def get_status():
    try:
        # Sunucunun çalışıp çalışmadığını kontrol et
        # Bir soket bağlantısı denemesi yapalım
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(2)  # 2 saniye timeout
        result = test_socket.connect_ex(('127.0.0.1', 5001))  # Sunucu portunu kontrol et
        test_socket.close()

        if result == 0:
            return jsonify({"status": "Online"}), 200
        else:
            return jsonify({"status": "Offline"}), 500
    except Exception as e:
        return jsonify({"status": "Offline", "error": str(e)}), 500

# Logları yapılandırılmış JSON formatında kaydetme fonksiyonu
def save_log_to_file(log_data):
    """
    Logları JSON formatında kaydeder ve doğru formatta olup olmadığını kontrol eder.
    """
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
    log_filename = f"{log_folder}/log_{timestamp}.json"  # .json uzantısını koru

    try:
        # JSON'un geçerli olup olmadığını kontrol et
        json_string = json.dumps(log_data, indent=4)  # JSON string olarak oluştur
        json.loads(json_string)  # JSON geçerli mi kontrol et

        with open(log_filename, 'w') as log_file:
            log_file.write(json_string)  # JSON formatında kaydet

        print(f"✅ Log saved to: {log_filename}")  # Başarı mesajı
    except json.JSONDecodeError as e:
        print(f"🚨 JSON format hatası: {e}")
    except Exception as e:
        print(f"🚨 Log kaydetme hatası: {e}")

# Logları almak için API endpoint
@app.route('/get_logs', methods=['GET'])
def get_logs():
    try:
        logs = get_logs_from_file()  # Log dosyasını okuma işlemi
        if not logs:
            raise ValueError("No logs found in the file.")  # Eğer log yoksa hata fırlatalım
        return jsonify(logs)
    except Exception as e:
        error_message = f"Error while fetching logs: {str(e)}"
        print(error_message)  # Hata mesajını konsola yazdıralım
        return jsonify({"error": error_message}), 500  # 500 status kodu ile hata mesajını döndürelim

# Yeni cüzdan oluşturma endpoint'i
@app.route('/create_wallet', methods=['GET'])
def create_new_wallet():
    try:
        wallet = create_wallet()
        return jsonify({
            "address": wallet.address,
            "private_key": wallet.private_key,
            "message": "Yeni cüzdan oluşturuldu."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Cüzdan bilgilerini görüntüleme endpoint'i
@app.route('/wallet_info', methods=['GET'])
def get_wallet_info():
    try:
        wallet_data = Wallet.load_from_file()
        if wallet_data:
            return jsonify(wallet_data), 200
        else:
            return jsonify({"error": "Cüzdan bulunamadı. Önce bir cüzdan oluşturun."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# JSON formatındaki log dosyalarını okuma fonksiyonu
def get_logs_from_file():
    """
    JSON formatındaki log dosyalarını okur ve listeler.
    """
    try:
        logs = []
        log_files = os.listdir(log_folder)  # Klasördeki tüm dosyaları al
        if not log_files:
            return []  # Eğer dosya yoksa boş liste döndür

        for log_file in log_files:
            if log_file.endswith(".json"):
                log_file_path = os.path.join(log_folder, log_file)
                with open(log_file_path, 'r') as file:
                    log_data = json.load(file)  # JSON dosyasını oku
                    logs.append(log_data)  # Log içeriklerini listeye ekle

        return logs

    except FileNotFoundError:
        raise FileNotFoundError("Log file not found.")
    except Exception as e:
        raise Exception(f"Error reading log file: {str(e)}")

# Coin transferi için API endpoint
@app.route('/transfer', methods=['POST'])
def transfer():
    try:
        data = request.get_json()
        sender = data.get("sender")
        recipient = data.get("recipient")
        amount = data.get("amount")

        # Bakiye kontrolü
        if blockchain.get_balance(sender) < amount:
            return jsonify({"error": "Yetersiz bakiye"}), 400

        # Yeni işlem oluştur
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }

        # Bloğa ekle
        blockchain.add_block([transaction])

        # Log kaydını yapılandırılmış JSON formatında yapalım
        log_data = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "previous_hash": blockchain.get_latest_block().previous_hash,
            "hash": blockchain.get_latest_block().hash,
            "transactions": [transaction]  # Transactions'ı dizi olarak kaydedin
        }

        save_log_to_file(log_data)  # Logu JSON formatında kaydedin

        return jsonify({"message": "Transfer başarılı"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Bakiye sorgulama için API endpoint
@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    try:
        balance = blockchain.get_balance(address)
        return jsonify({"address": address, "balance": balance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Sunucuyu başlatma fonksiyonu
def start_server(host='127.0.0.1', port=5001):
    # Sunucu soketini oluştur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # Sunucuyu belirtilen host ve port üzerinde dinlemeye başlat
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        # İstemci bağlantısını kabul et
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")

        try:
            # Şifreyi alalım
            password = client_socket.recv(1024).decode('utf-8')
            print(f"Password received: {password}")

            # Şifreyi kontrol edelim
            if password == "Baklava123":
                print("Password correct, proceeding...")
                response = "Password accepted"
                client_socket.send(response.encode('utf-8'))

                # Blockchain verisi alalım
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Received data: {data}")

                # JSON verisini işleyerek bir blok ekleyelim
                block_data = json.loads(data)
                blockchain.add_block([block_data])  # Blockchain'e ekliyoruz
                print(f"Updated blockchain: {blockchain.chain}")

                # Log kaydını yapılandırılmış JSON formatında yapalım
                log_data = {
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                    "previous_hash": blockchain.get_latest_block().previous_hash,
                    "hash": blockchain.get_latest_block().hash,
                    "transactions": [block_data]  # Transactions'ı dizi olarak kaydedin
                }

                save_log_to_file(log_data)  # Logu JSON formatında kaydedin

                # Yanıt gönderelim
                client_socket.send("Block data received and added to blockchain".encode('utf-8'))
            else:
                print("Incorrect password.")
                response = "Incorrect password"
                client_socket.send(response.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Bağlantıyı kapatalım
            client_socket.close()

if __name__ == "__main__":
    # Sunucu ve Flask API'yi çalıştır
    server_thread = Thread(target=start_server, args=('127.0.0.1', 5001))
    server_thread.start()

    # Flask API'yi çalıştır
    app.run(debug=True, host='0.0.0.0', port=5002)  # API portu farklı olmalı