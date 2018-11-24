# use this file to create genesis block
import pymongo
import time
from hashlib import sha256

import Transaction
import Merkle2

client = pymongo.MongoClient(host='local_host', port=27017)
db = client.blockchian
collection_chain = db.chain

addresses = []
transactions = []
block = dict()

for address in addresses:
    transactions.append(Transaction.Transaction(None, address, 20))
block['index'] = 1
block['time_stamp'] = time.time()
block['pre_hash'] = None
block['target'] = '000000'
block['transactions'] = transactions
block['nonce'] = None
block['hash'] = sha256(str(block).encode()).hexdigest()

