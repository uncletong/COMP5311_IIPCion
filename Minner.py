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

    # def add_neighbour(self, ip, port):
    #     for neighbor in self.neighbours:
    #         if ip == neighbor.ip:
    #             neighbor.add_port(port)
    #             return
    #     self.neighbours.append({'ip':ip,'port':port})

    # def remove_neighbour(self, ip, port=None):
    #     if port:
    #         self.neighbours.remove(self.neighbours.index(ip))
    #     else:
    #         self.neighbours[self.neighbours.index(ip)].remove_port(port)


def broadcast_transaction_to_spv(temp_transaction,prev_transaction):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('159.65.148.98', 8888))
    print('---broadcast_to_spv---')
    s.sendall(temp_transaction)
    s.sendall(prev_transaction)
    s.close()


def broadcast_transaction(temp_transaction):
    for temp_ip in neighbour_ip:
        temp_port = neighbour_port[neighbour_ip.index(temp_ip)]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((temp_ip, temp_port))
        s.sendall(temp_transaction)
        s.close()


def broadcast_block(temp_block):
    json_block = json.dumps(temp_block)
    for temp_ip in neighbour_ip:
        temp_port = 8887
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((temp_ip, temp_port))
        print('---broadcast block---')
        print(json_block)
        print('---broadcast block---')
        s.sendall(json_block.encode())
        s.close()


def get_neighbours():
    file = open('neighbour.txt')
    data = file.readline()
    while data:
        ip, port = data.split(' ')
        neighbour_ip.append(ip)
        neighbour_port.append(int(port.strip('\n')))
        data = file.readline()
    print(neighbour_ip)
    print(neighbour_port)


def request(temp_key):
    ip = '159.203.74.214'
    port = 8889
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(temp_key.encode())
    data = s.recv(10020).decode()
    while data:
        print('---receive ' + temp_key + '---')
        data = json.loads(data)
        print(data)
        if temp_key == 'chain':
            chain.insert_one(data)
        elif temp_key == 'tree':
            tree.insert_one(data)
        data = s.recv(10020).decode()


def listen_block_request(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(3)
    print('---block request listening---')
    while True:
        conn, add = s.accept()
        req = conn.recv(1024).decode()
        print('---received block request---')
        if req == 'chain':
            blocks = chain.find()
            for temp_block in blocks:
                del temp_block['_id']
                block_json = json.dumps(temp_block, default=lambda obj: obj.__dict__, sort_keys=False, indent=4)
                print(block_json)
                conn.sendall(block_json.encode())
            conn.close()
        elif req == 'tree':
            trees = tree.find()
            for temp_tree in trees:
                del temp_tree['_id']
                tree_json = json.dumps(temp_tree, default=lambda obj: obj.__dict__, sort_keys=False, indent=4)
                print(tree_json)
                conn.sendall(tree_json.encode())
            conn.close()
        else:
            conn.close()


def listen_block(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(3)
    print('---block listening---')
    while True:
        conn, add = s.accept()
        temp_block = conn.recv(10024).decode()
        print('---received block---')
        print(temp_block)
        temp_block = json.loads(temp_block)
        chain_length = chain.find().count()
        # it means system have mined the chain first
        if temp_block['index'] <= chain_length:
            print('---broadcast too late---')
            conn.close()
            continue
        else:
            temp_hash = temp_block['hash']
            del temp_block['hash']
            if temp_hash == sha256(str(temp_block).encode()).hexdigest():
                temp_block['hash'] = temp_hash
                if temp_block['index'] <= chain.find().count():
                    print('---broadcast too late---')
                    continue
                chain.insert_one(temp_block)
                temp_tree = Merkle2.Merkletree(Trans=temp_block['transactions'])
                temp_tree.make_tree()
                tree.insert_one(temp_tree.all_hash)
                print('---have verified the block and store---')
                conn.close()
            else:
                print('---verify fail---')
                conn.close()


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
            re_transaction = data.strip(public_key)
            print('---public key---')
            print(pub_key)
            rec_transaction = json.loads(re_transaction)
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
                    broadcast_transaction(data.encode())
                    broadcast_transaction_to_spv(data.encode(), json.dumps(temp['transactions'][0]).encode())
                    print('success, transaction pool len: ' + str(len(transaction_pool)))
                    conn.sendall('success'.encode('utf-8'))


def proof_of_work(target, temp_block):
    nonce = int(20000000 * random.random())
    local_time = time.asctime(time.localtime(time.time()))
    print('---start mining time: ' + local_time + '---')
    while True:
        temp_block['nonce'] = nonce
        block_str = str(temp_block)
        temp_hash = sha256(block_str.encode()).hexdigest()
        block_target = temp_hash[-6:]
        if block_target == target:
            break
        else:
            nonce = nonce + 1

    local_time = time.asctime(time.localtime(time.time()))
    print('---end mining time: ' + local_time + '---')
    block['nonce'] = nonce
    block['hash'] = temp_hash
    length = chain.find().count()
    if block['index'] <= length:
        print('mining to late')
        pass
    else:
        broadcast_block(block)
        chain.insert_one(block)
        tree.insert_one(merkle_tree.all_hash)


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
    elif sys.argv[1] == '-sc':
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client.block_chain
        chain = db.chain
        request('chain')
        sys.exit()
    elif sys.argv[1] == '-st':
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client.block_chain
        tree = db.tree
        request('tree')
        sys.exit()
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

# get neighours' ip and address
neighbour_ip = list()
neighbour_port = list()
get_neighbours()
# listen
_thread.start_new_thread(listen_block_request, ('', 8889))
_thread.start_new_thread(listen_block, ('', 8887))
# start a new thread to listen transactions
_thread.start_new_thread(listen_transaction, ('', miner.port))

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
        block['target'] = '000000'
        transactions = transaction_pool[0:7]
        transactions.append({'sour_address': None, 'dest_address': miner.address, 'amount': 20})
        block['transactions'] = transactions
        transactions_string = list()
        for transaction in transactions:
            transactions_string.append(str(transaction))

        merkle_tree = Merkle2.Merkletree(transactions_string)
        merkle_tree.make_tree()
        block['merkel_root'] = merkle_tree.root
        for i in range(0, 7):
            transaction_pool.pop(6 - i)
        thread_mine = _thread.start_new_thread(proof_of_work, (block['target'], block))
