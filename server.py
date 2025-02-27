import socket
import json
from blockchain import Blockchain  # Blockchain sınıfınızı buraya dahil etmelisiniz

def start_server(host='127.0.0.1', port=5001):
    # Sunucu soketini oluştur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # Sunucuyu belirtilen host ve port üzerinde dinlemeye başlat
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    blockchain = Blockchain()  # Blockchain'i başlatıyoruz

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
                blockchain.add_block(block_data)  # Blockchain'e ekliyoruz
                print(f"Updated blockchain: {blockchain.chain}")

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
    start_server()
