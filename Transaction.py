import ecdsa


class Transaction:
    def __init__(self, sour_address, dest_address, amount):
        self.amount = amount
        self.dest_address = dest_address
        self.sour_address = sour_address

    @staticmethod
    def generate_sig(private_key, sour_address, dest_address, amount):
        signature = private_key.sign(sour_address + dest_address + amount)
        return signature

    @staticmethod
    def find_previous_transaction(sour_address):
        pass
