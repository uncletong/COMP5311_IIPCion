import GenerateKey

class Transaction:
    def __init__(self, sour_address, dest_address, amount):
        self.amount = amount
        self.dest_address = dest_address
        self.sour_address = sour_address
        self.signature = None

    def generate_sig(self, private_key, sour_address, dest_address, amount):
        print((str(sour_address) + str(dest_address) + str(amount)))
        print('------data-------')
        self.signature = GenerateKey.generate_sign(private_key, (str(sour_address) + str(dest_address) + str(amount)))

    @staticmethod
    def find_previous_transaction(sour_address):
        pass
