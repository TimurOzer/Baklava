import socket
import hashlib
import os
import sys

def calculate_file_hash(filename):
    """Dosyanın hash'ini hesapla"""
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def start_client():
    host = '192.168.1.106'
    port = 5555

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"✅ Sunucuya bağlandınız: {host}:{port}")

        # Sunucudan mevcut client.py hash'ini al
        server_client_hash = client_socket.recv(1024).decode('utf-8')
        
        # Yerel client.py hash'ini hesapla
        try:
            local_client_hash = calculate_file_hash('client.py')
        except FileNotFoundError:
            local_client_hash = None

        # Hash'ler farklıysa güncelleme yap
        if local_client_hash != server_client_hash:
            print("🔄 Güncelleme gerekiyor...")
            client_socket.send('UPDATE_NEEDED'.encode('utf-8'))
            
            # Yeni client.py dosyasını al
            with open('client.py', 'wb') as file:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
            
            print("✅ Client güncellendi. Yeniden başlatılıyor...")
            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            client_socket.send('NO_UPDATE'.encode('utf-8'))
            print("✅ Güncel sürümdesiniz.")

        # Normal mesaj gönderme
        while True:
            message = input("Mesaj gönder (çıkış için 'quit'): ")
            
            if message.lower() == 'quit':
                break
            
            client_socket.send(message.encode('utf-8'))

    except ConnectionRefusedError:
        print("❌ Sunucuya bağlanılamadı. IP adresini kontrol edin.")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()