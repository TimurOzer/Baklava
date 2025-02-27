import os
import json
import socket
from datetime import datetime
import git  # GitPython
import shutil
from blockchain import Blockchain

# GitHub repository dizini
REPO_PATH = "C:/Users/timon/Documents/GitHub/Test"  # GitHub repo klasör yolu
LOG_FOLDER = "client_logs"  # Log klasör yolu

def push_to_github(log_file):
    try:
        repo = git.Repo(REPO_PATH)  # Git repo açılır
        repo.git.add(log_file)  # Log dosyasını stage eder
        repo.git.commit('-m', f'Added log file {log_file}')  # Commit yapar
        repo.git.push()  # GitHub'a push eder
        print(f"Log file {log_file} pushed to GitHub.")
    except Exception as e:
        print(f"Error pushing to GitHub: {e}")

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

                # Log dosyasını kaydedelim
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                log_filename = f"log_{timestamp}.txt"
                log_filepath = os.path.join(LOG_FOLDER, log_filename)
                with open(log_filepath, 'w') as log_file:
                    log_file.write(f"Received block data: {block_data}\n")
                    log_file.write(f"Updated blockchain: {blockchain.chain}\n")
                print(f"Log saved to: {log_filepath}")

                # GitHub'a yükleyelim
                push_to_github(log_filepath)

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
