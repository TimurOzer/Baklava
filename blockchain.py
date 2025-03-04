import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __str__(self):
        return f"Block {self.index} - Hash: {self.hash}, Previous Hash: {self.previous_hash}, Transactions: {self.transactions}, Timestamp: {self.timestamp}"


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.balances = {}  # Cüzdan adresleri ve bakiyeleri

    def create_genesis_block(self):
        genesis_transactions = [{
            "sender": "0",  # Sistem tarafından oluşturuldu
            "recipient": "03f010ab12973e6a66bb57b6447c8e3f59dcc054592a8093133413b3096bf4d7",  # Geliştirici cüzdanı
            "amount": 21000000  # Toplam arz
        }]
        return Block(0, "0", genesis_transactions, time.time())

    def add_block(self, transactions):
        new_block = Block(len(self.chain), self.get_latest_block().hash, transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.update_balances(transactions)  # Bakiyeleri güncelle

    def update_balances(self, transactions):
        for transaction in transactions:
            sender = transaction["sender"]
            recipient = transaction["recipient"]
            amount = transaction["amount"]

            # Gönderenin bakiyesini azalt
            if sender in self.balances:
                self.balances[sender] -= amount
            else:
                self.balances[sender] = -amount

            # Alıcının bakiyesini artır
            if recipient in self.balances:
                self.balances[recipient] += amount
            else:
                self.balances[recipient] = amount

    def get_balance(self, address):
        return self.balances.get(address, 0)

    def get_latest_block(self):
        return self.chain[-1]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def __str__(self):
        return "\n".join([str(block) for block in self.chain])