import json
import socket
import sys
import _thread
import time
import random
import pymongo
from hashlib import sha256

import Merkle2
import GenerateKey

transaction_pool = list()
#  neighbour


class Miner:

    def __init__(self, port, temp_address):
        self.address = temp_address
        self.transaction_pool = []
        self.port = port
        self.neighbours = []

    # def add_neighbour(self, ip, port):
    #     for neighbor in self.neighbours:
    #         if ip == neighbor.ip:
    #             neighbor.add_port(port)
    #             return
    #     self.neighbours.append({'ip':ip,'port':port})

    def remove_neighbour(self, ip, port=None):
        if port:
            self.neighbours.remove(self.neighbours.index(ip))
        else:
            self.neighbours[self.neighbours.index(ip)].remove_port(port)


def listen_transaction(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(3)
    print('---server turned on in ' + ip + ':' + str(port) + '---')
    while True:
        conn, add = s.accept()
        data = conn.recv(10024).decode()
        print('----done---')
        print(data)
        if len(data.strip()) == 0:
            conn.sendall('no transaction'.encode('utf-8'))
            continue
        else:
            pub_key = data[-128:]
            transaction = data.strip(public_key)
            print('---public key---')
            print(public_key)
            rec_transaction = json.loads(transaction)
            flag = False
            for temp_transaction in transaction_pool:
                if temp_transaction['sour_address'] == rec_transaction['sour_address']:
                    conn.sendall('duplicate transaction'.encode('utf-8'))
                    flag = True
                    break
            if flag:
                continue
            temp_transaction = chain.find({'transactions.dest_address': rec_transaction['sour_address']}, {'transactions.amount.$': 1})

            # find last transaction
            temp = None
            for temp in temp_transaction:
                pass

            if not temp:
                conn.sendall('this address not in system'.encode())
                continue
            elif temp['transactions'][0]['amount'] < (sum(rec_transaction['amount'])):
                conn.sendall(('no enough balance, balance:' + str(temp['transactions'][0]['amount'])).encode())
                continue
            else:
                # two times verify
                if not GenerateKey.verify_public_key(public_key=pub_key, address=rec_transaction['sour_address']):
                    conn.sendall('public key verify fail'.encode())
                    continue
                elif not GenerateKey.verify_sign(public_key=pub_key, sign=rec_transaction['signature'], data=(str(rec_transaction['sour_address']) + str(rec_transaction['dest_address']) + str(rec_transaction['amount']))):
                    print('---data---')
                    print((str(rec_transaction['sour_address']) + str(rec_transaction['dest_address']) + str(rec_transaction['amount'])))
                    conn.sendall('sign verify fail'.encode())
                    continue
                else:
                    transaction_pool.append(rec_transaction)
                    print('success, transaction pool len: ' + str(len(transaction_pool)))
                    conn.sendall('success'.encode('utf-8'))


def proof_of_work(target, temp_block):
    nonce = int(20000000 * random.random())
    local_time = time.asctime(time.localtime(time.time()))
    print('---start time: ' + local_time + '---')
    while True:
        block_str = str(temp_block) + str(nonce)
        temp_hash = sha256(block_str.encode()).hexdigest()
        block_target = temp_hash[-4:]
        if block_target == target:
            break
        else:
            nonce = nonce + 1

    local_time = time.asctime(time.localtime(time.time()))
    print('---end time: ' + local_time + '---')
    return temp_hash, nonce


if len(sys.argv) > 1:
    if sys.argv[1] == '-c':
        key = GenerateKey.GenerateKey()
        private_key, public_key, address = key.generate_key()
        miner = Miner(int(sys.argv[3]), address)
        print('your private_key is: ')
        print(private_key)
        print('your public_key is: ')
        print(public_key)
        print('your address is:')
        print(address)
    elif sys.argv[1] == '-a':
        miner = Miner(sys.argv[2], sys.argv[4])
    elif sys.argv[1] == '-h':
        print('usage: {-c,-a}{-p port} {}')
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
db = client.block_chain
chain = db.chain
tree = db.tree
try:
    # start a new thread to listen transactions
    _thread.start_new_thread(listen_transaction, ('', miner.port))
except:
    print('thread start error')

while True:
    if len(transaction_pool) < 7:
        # if number of transaction is less than 8, sleep one minute
        print('---have checked the transaction pool---')
        print('length of transaction pool: ' + str(len(transaction_pool)))
        time.sleep(60)
    else:
        block = dict()
        chain_len = chain.find().count()
        block['index'] = chain_len + 1
        block['time_stamp'] = time.time()
        block['prev_hash'] = chain.find_one({'index': chain_len})['hash']
        # cal time is around 60s using this target
        block['target'] = '0000'
        transactions = transaction_pool[0:7]
        transactions.append({'sour_address': None, 'dest_address': miner.address, 'amount': 20})
        block['transactions'] = transactions
        transactions_string = list()
        for transaction in transactions:
            transactions_string.append(str(transaction))

        merkle_tree = Merkle2.Merkletree(transactions_string)
        merkle_tree.Make_a_tree()
        block['merkel_root'] = merkle_tree.Get_Root()
        for i in range(0, 7):
            transaction_pool.pop(6 - i)
        print('---start to mining---')
        block_hash, block_nonce = proof_of_work(block['target'], block)
        block['hash'] = block_hash
        block['nonce'] = block_nonce
        print('---end of mining---')
        chain.insert_one(block)
        tree.insert_one(merkle_tree.Get_all_hash())
