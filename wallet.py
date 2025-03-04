import hashlib
import os
import json

class Wallet:
    def __init__(self):
        self.private_key = os.urandom(32).hex()  # Rastgele özel anahtar
        self.address = self.generate_address()   # Cüzdan adresi

    def generate_address(self):
        # Özel anahtarı kullanarak cüzdan adresi oluştur
        return hashlib.sha256(self.private_key.encode()).hexdigest()

    def save_to_file(self, filename="wallet.json"):
        # Cüzdan bilgilerini dosyaya kaydet
        wallet_data = {
            "private_key": self.private_key,
            "address": self.address
        }
        with open(filename, 'w') as file:
            json.dump(wallet_data, file, indent=4)

    @staticmethod
    def load_from_file(filename="wallet.json"):
        # Cüzdan bilgilerini dosyadan yükle
        try:
            with open(filename, 'r') as file:
                wallet_data = json.load(file)
            return wallet_data
        except FileNotFoundError:
            return None

# Yeni cüzdan oluştur
def create_wallet():
    wallet = Wallet()
    wallet.save_to_file()
    print(f"Yeni cüzdan oluşturuldu. Adres: {wallet.address}")
    return wallet