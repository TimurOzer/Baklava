import socket
import json

def send_block_to_network(host='127.0.0.1', port=5000, block_data=None):
    if block_data is None:
        block_data = {"index": 1, "previous_hash": "0000", "transactions": "Alice->Bob 10 BTC", "timestamp": 123456789}

    try:
        # İstemci soketi oluşturuluyor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Şifreyi gönder
        password = "Baklava123"
        client_socket.send(password.encode('utf-8'))

        # Sunucudan gelen yanıtı al (şifre doğrulaması)
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

        if "accepted" in response:
            # Şifre doğruysa veri gönder
            data = json.dumps(block_data)
            client_socket.send(data.encode('utf-8'))
            print(f"Sent block data: {data}")
            
            # Sunucudan gelen yanıtı al
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
        else:
            print("Incorrect password. Closing connection.")
        
        client_socket.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_block_to_network()
