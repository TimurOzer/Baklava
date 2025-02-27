import socket
import json
import os
import time
from blockchain import Blockchain
import git

# Log kaydetme ve GitHub'a yükleme fonksiyonu
def log_to_github(log_data):
    # Log klasörünü kontrol et
    log_folder = 'client_logs'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Güncel tarih ile log kaydetme
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_folder, f"log_{current_time}.txt")
    
    with open(log_file, 'w') as file:
        file.write(log_data)

    # Git işlemleri
    repo = git.Repo(log_folder)
    repo.index.add([log_file])
    repo.index.commit(f"Log updated at {current_time}")
    repo.remote().push()  # Push to the remote repository

def start_server(host='127.0.0.1', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    blockchain = Blockchain()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")

        try:
            # Şifre doğrulaması
            password = client_socket.recv(1024).decode('utf-8')
            if password == "Baklava123":
                print("Password correct, proceeding...")
                response = "Password accepted"
                client_socket.send(response.encode('utf-8'))

                # Blockchain verisi alalım
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Received data: {data}")

                # JSON verisini işleyerek blok ekleyelim
                block_data = json.loads(data)
                blockchain.add_block(block_data)
                print(f"Updated blockchain: {blockchain.chain}")

                # Log verisini oluştur
                log_data = f"Block data received and added to blockchain:\n{block_data}\nUpdated blockchain:\n{blockchain.chain}"
                
                # GitHub'a gönder
                log_to_github(log_data)

                # Yanıt gönderelim
                client_socket.send("Block data received and added to blockchain".encode('utf-8'))
            else:
                print("Incorrect password.")
                response = "Incorrect password"
                client_socket.send(response.encode('utf-8'))
        
        except Exception as e:
            print(f"Error: {e}")

        finally:
            client_socket.close()

if __name__ == "__main__":
    start_server()
