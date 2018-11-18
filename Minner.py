import json
import socket
import sys
import _thread
import time
import random
import pymongo
from hashlib import sha256

import Host
from User import User


class Miner:

    def __init__(self, port, address):
        self.address = address
        self.transaction_pool = []
        self.port = port
        self.ip = socket.gethostbyname(socket.gethostname())
        self.neighbours = []

    def add_neighbour(self, ip, port):
        for neighbor in self.neighbours:
            if ip == neighbor.ip:
                neighbor.add_port(port)
                return
        self.neighbours.append(Host.Host(ip, port))

    def remove_neighbour(self, ip, port=None):
        if port:
            self.neighbours.remove(self.neighbours.index(ip))
        else:
            self.neighbours[self.neighbours.index(ip)].remove_port(port)


def listen_transaction(ip, port, transaction_pool):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(3)
    while True:
        conn, address = s.accept()
        data = conn.recv(10024)
        flag = 0
        if len(data.strip()) == 0:
            conn.sendall('no transaction'.encode('utf-8'))
        else:
            rec_transaction = json.loads(data)
            for temp_transaction in transaction_pool:
                if temp_transaction['sour_address'] == rec_transaction['sour_address']:
                    conn.sendall('duplicate transaction'.encode('utf-8'))
                    flag = 1
                    break
            if flag:
                transaction_pool.append(rec_transaction)
                conn.sendall('success'.encode('utf-8'))
                # verify transaction


def proof_of_work(target, temp_block):
    nonce = int(20000000 * random.random())
    block_str = str(temp_block) + str(nonce)
    while True:
        block_hash = sha256(block_str.encode()).hexdigest()
        block_target = block_hash[-6:]
        if block_target == target:
            break
        else:
            nonce = nonce + 1
    return block_hash, nonce


if len(sys.argv) > 3:
    if sys.argv[3] == '-c' or '-create':
        user = User()
        miner = Miner(sys.argv[2], user.address)
        print('your private_key is: ')
        print(user.private_key)
        print('your public_key is: ')
        print(user.public_key)
        print('your address is:')
        print(user.address)
    elif sys.argv[3] == '-a' or '-address':
        miner = Miner(sys.argv[2], sys.argv[4])
    elif sys.argv[1] == '-h' or '-help':
        print('usage: User {-p port} {}')
        print('-c: create keys')
        print('-p: port')
        print('-a input address')
    else:
        print('please use -h to check the usage')
        sys.exit()
else:
    print('please use -h to check the usage')
    sys.exit()

# connect to database
client = pymongo.MongoClient(host='localhost', port=27017)
db = client.blockchian
collection = db.chain
transaction_pool =[]
try:
    # start a new thread to listen transactions
    _thread.start_new_thread(listen_transaction, (miner.ip, miner.port, transaction_pool))
except:
    print('thread start error')

while True:
    if len(transaction_pool) < 8:
        # if number of transaction is less than 8, sleep one minute
        time.sleep(60)
    else:
        block = dict()
        chain_len = collection.find().count()
        block['index'] = chain_len + 1
        block['time_stamp'] = time.time()
        block['prev_hash'] = collection.find_one({'index': chain_len})['hash']
        # cal time is around 60s using this target
        block['target'] = '000000'
        block['transaction'] = transaction_pool[0:8]
        for i in range(0,8):
            transaction_pool.pop(i)
        block_hash, block_nonce = proof_of_work(block['target'], block)
        block['hash'] = block_hash
        block['nonce'] = block_nonce
        collection.insert_one(block)
