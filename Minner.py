import json
import socket
import sys
import _thread
import time

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
    s.bind(ip, port)
    s.listen(3)
    while True:
        conn, address = s.accept()
        data = conn.recv(10024)
        if len(data.strip()) == 0:
            conn.sendall('no transaction'.encode('utf-8'))
        else:
            rec_transaction = json.loads(data)
            transaction_pool.append(rec_transaction)
            conn.sendall('success'.encode('utf-8'))


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

transaction_pool =[]
try:
    _thread.start_new_thread(listen_transaction, (miner.ip, miner.port, transaction_pool))
except:
    print('thread start error')





