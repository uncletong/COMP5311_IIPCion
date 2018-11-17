

class Transaction:
    def __init__(self, sour_address, dest_address, amount):
        self.amount = amount
        self.dest_address = dest_address
        self.sour_address = sour_address
        self.signature = None

    def generate_sig(self, private_key, sour_address, dest_address, amount):
        self.signature = private_key.sign(sour_address + dest_address + amount)

    @staticmethod
    def find_previous_transaction(sour_address):
        pass
