import socket
import json
from blockchain import Blockchain

# Şifreyi belirliyoruz
PASSWORD = "Baklava123"

def start_server(host='127.0.0.1', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    blockchain = Blockchain()  # Blockchain'i başlatıyoruz

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")

        # Şifre isteme
        client_socket.send("Enter password: ".encode('utf-8'))
        password = client_socket.recv(1024).decode('utf-8')

        # Şifreyi kontrol et
        if password == PASSWORD:
            print("Password correct, proceeding...")
            response = "Password accepted. You can now send block data."
            client_socket.send(response.encode('utf-8'))

            # Blockchain verisi al
            data = client_socket.recv(1024).decode('utf-8')
            block_data = json.loads(data)  # Veriyi JSON formatında alıyoruz
            print(f"Received block data: {block_data}")

            # Blockchain'e ekliyoruz
            blockchain.add_block(block_data)
            print(f"Updated blockchain: {blockchain.chain}")

            response = "Block added to blockchain"
            client_socket.send(response.encode('utf-8'))
        else:
            print("Incorrect password!")
            response = "Incorrect password. Connection closing."
            client_socket.send(response.encode('utf-8'))

        client_socket.close()

if __name__ == "__main__":
    start_server()
