import GenerateKey
import Transaction
import sys


class User:

    def __init__(self, private_key=None, public_key=None, address=None):
        if not private_key:
            key = GenerateKey.GenerateKey()
            self.private_key, self.public_key, self.address = key.generate_key()
        else:
            self.private_key = private_key
            self.public_key = public_key
            self.address = address

    def generate_transaction(self, dest_addresses, amounts, ip=None, port=None):
        transaction = Transaction.Transaction(self.address, dest_addresses, amounts)
        # send to miner


if len(sys.argv) > 1:
    if sys.argv[1] == '-c' or '-create':
        mode = 'c'
        user = User()
        print('your private_key is: ')
        print(user.private_key)
        print('your public_key is: ')
        print(user.public_key)
        print('your address is:')
        print(user.address)
    elif sys.argv[1] == '-p' or 'private' or 'private_key':
        mode = 'p'
        user = User(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == '-h' or '-help':
        print('usage: User {-c, -p private_key public_key address}')
        print('-c: create keys')
        print('-p: use your own keys to create the client')
    else:
        print('please use correct format: -c for create keys or -p to input your keys')
        sys.exit()
else:
    print('please use -h to check the usage')
    sys.exit()


while True:

    print('please input your transaction:')
    destination_address = input('please input destination address(s): ').split()
    amount = input('please input amount(s): ').split()
    ip, port = input('please input the ip and port of block chain server: ').split()
    port = int(port)
    amount = list(map(int, amount))
    user.generate_transaction(destination_address, amount)
    print(user)


