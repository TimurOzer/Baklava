# blockchain.py
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.balances = {}  # Cüzdan adresleri ve bakiyeleri

    def create_genesis_block(self):
    genesis_transactions = [{
        "sender": "0",  # Sistem tarafından oluşturuldu
        "recipient": "developer_wallet_address",  # Geliştirici cüzdanı
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