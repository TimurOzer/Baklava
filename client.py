import socket
import json
import os

# Dosya yolu ve klasör
log_dir = "client_logs"
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

def send_block_to_network(host='127.0.0.1', port=5000, block_data=None):
    if block_data is None:
        block_data = {"index": 1, "previous_hash": "0000", "transactions": "Alice->Bob 10 BTC", "timestamp": 123456789}

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # Şifreyi kullanıcıdan al
    password = input("Enter password: ")

    # Şifreyi sunucuya gönder
    client_socket.send(password.encode('utf-8'))
    
    # Sunucudan yanıt al
    response = client_socket.recv(1024).decode('utf-8')
    if response == "Password accepted":
        print(f"Server response: {response}")
        
        # Şifre doğruysa, blok verisini gönder
        data = json.dumps(block_data)
        client_socket.send(data.encode('utf-8'))
        print(f"Sent block data: {data}")
        
        # Log dosyasına yaz
        log_to_file(f"Sent block data: {data}")
        
        # Sunucudan gelen yanıtı al
        server_response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {server_response}")
        
        # Log dosyasına yaz
        log_to_file(f"Server response: {server_response}")
    else:
        print("Incorrect password.")
        log_to_file("Incorrect password attempt.")

    client_socket.close()

if __name__ == "__main__":
    create_log_folder()  # Log klasörünü oluştur
    send_block_to_network()
