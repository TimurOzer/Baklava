import socket
import threading
import hashlib
import os

def calculate_file_hash(filename):
    """Dosyanın hash'ini hesapla"""
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def handle_client(client_socket, client_address):
    print(f"🔗 {client_address} bağlandı.")
    
    try:
        # Client.py dosyasının güncel hash'ini gönder
        current_client_hash = calculate_file_hash('client.py')
        client_socket.send(current_client_hash.encode('utf-8'))
        
        # Güncelleme isteği kontrolü
        update_request = client_socket.recv(1024).decode('utf-8')
        
        if update_request == 'UPDATE_NEEDED':
            # Client.py dosyasını gönder
            with open('client.py', 'rb') as file:
                client_socket.sendfile(file)
            print(f"📦 {client_address} için client.py güncellendi.")
        
        # Normal mesaj alışverişi
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message:
                break
            
            print(f"📩 {client_address} mesaj gönderdi: {message}")
    
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    finally:
        print(f"❌ {client_address} bağlantısı kesildi.")
        client_socket.close()

def start_server():
    host = '192.168.1.106'
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"🌐 Sunucu {host}:{port} üzerinde çalışıyor...")

    while True:
        client_socket, client_address = server_socket.accept()
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()