import socket
import json
import os
import time
import git  # GitPython kütüphanesini ekliyoruz

# Log dosyasının bulunduğu klasörü oluşturuyoruz
log_folder = "client_logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
    print(f"Log folder created at: {log_folder}")
else:
    print(f"Log folder already exists at: {log_folder}")

# Log kaydını dosyaya yazdırma fonksiyonu
def log_message(message):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")  # Zaman damgası oluştur
    log_filename = os.path.join(log_folder, f"log_{timestamp}.txt")  # Dosya adını belirle
    with open(log_filename, 'w') as f:
        f.write(message)  # Mesajı dosyaya yaz

    # Log kaydedildikten sonra otomatik olarak GitHub'a push yapalım
    try:
        repo = git.Repo(search_parent_directories=True)  # Git repo'nun kökünü bul
        repo.git.add(log_filename)  # Dosyayı staging area'ya ekle
        repo.index.commit(f"New log added: {timestamp}")  # Commit mesajı oluştur
        origin = repo.remotes.origin  # GitHub'a bağlı origin'i bul
        origin.push()  # Değişiklikleri GitHub'a gönder
        print("Log pushed to GitHub successfully.")
    except Exception as e:
        print(f"GitHub push error: {e}")

# Sunucuya bağlantı yapma ve blok gönderme fonksiyonu
def send_block_to_network():
    host = '127.0.0.1'  # Sunucu IP adresi
    port = 5001  # Sunucu portu

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))  # Sunucuya bağlan
        print("Connected to server.")

        # Şifreyi alalım
        password = input("Please enter the password: ")
        client_socket.send(password.encode('utf-8'))  # Şifreyi sunucuya gönder

        # Sunucudan gelen yanıtı alalım
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

        if response == "Password accepted":
            # Blok verisini alalım ve gönderelim
            block_data = {
                "index": 1,
                "previous_hash": "0000",  # İlk blokta previous_hash '0000'
                "transactions": "Alice->Bob 10 BTC",
                "timestamp": time.time()
            }

            # JSON formatında veriyi sunucuya gönderelim
            client_socket.send(json.dumps(block_data).encode('utf-8'))
            print(f"Sent block data: {block_data}")

            # Sunucudan gelen yanıtı alalım
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")

            # Log kaydını yazdıralım
            log_message(f"Block data sent: {block_data}\nServer response: {response}")
            print("Log saved and pushed to GitHub successfully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()  # Bağlantıyı kapat

if __name__ == "__main__":
    send_block_to_network()
