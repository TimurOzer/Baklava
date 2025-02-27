import socket
import json
import os
import subprocess
from blockchain import Blockchain

# Dosya yolu ve klasör
log_dir = "server_logs"
log_file = os.path.join(log_dir, "log.txt")

def create_log_folder():
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Log folder created at: {log_dir}")
    else:
        print(f"Log folder already exists at: {log_dir}")

def log_to_file(message):
    with open(log_file, "a") as file:
        file.write(message + "\n")

def git_push():
    try:
        # Git'e ekle, commit yap ve push işlemini yap
        subprocess.run(["git", "add", "."])  # Dosyaları ekle
        subprocess.run(["git", "commit", "-m", "Updated log file"])  # Commit yap
        subprocess.run(["git", "push", "origin", "main"])  # Push yap
        print("Log file pushed to GitHub successfully!")
    except Exception as e:
        print(f"Error while pushing to GitHub: {e}")

def start_server(host='127.0.0.1', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    blockchain = Blockchain()  # Blockchain'i başlatıyoruz

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")

        try:
            # Şifre doğrulaması yapılacak
            password = client_socket.recv(1024).decode('utf-8')
            if password == "Baklava123":
                print("Password correct, proceeding...")
                response = "Password accepted"
                client_socket.send(response.encode('utf-8'))

                # Blockchain verisi alalım
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Received data: {data}")

                # JSON verisini işleyerek bir blok ekleyelim
                block_data = json.loads(data)
                blockchain.add_block(block_data)  # Blockchain'e ekliyoruz
                print(f"Updated blockchain: {blockchain.chain}")

                # Log dosyasına yaz
                log_to_file(f"Received data: {data}")
                log_to_file(f"Updated blockchain: {blockchain.chain}")

                # GitHub'a dosyayı pushla
                git_push()

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
    create_log_folder()  # Log klasörünü oluştur
    start_server()

