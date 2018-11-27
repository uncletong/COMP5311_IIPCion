# use this file to create genesis block
import pymongo
import time
import json
from hashlib import sha256

import Transaction
import Merkle2

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['block_chain']
addresses = list()
transactions = list()
addresses.append("5KDUxH6XMYdtkv4UGqyEFkv1YRSGLRxhT")
addresses.append("5ocRwLqmf9rAdRm1cFjQbwhUvRMtAt13q")
addresses.append("HbjVXPZrub1dFfx5ytUzm2FbDiSbzBvFM")
addresses.append("KdoaVaLmHqh7gpk3tF6xfzYaSYd8Am13Y")
addresses.append("2VrkStCq88M749MS2VbNWxp3m3yiFqkdy")
addresses.append("4MvWGcfFXz9t1dTJh6nvy2fqEjvx6ogku")
addresses.append("9cGJfg3eRXDN5biwg6dvGK4VKrw2TgyRh")
addresses.append("EAtPm4Jfo5t9bVwrXf3Vy3V7CRDeDBPac")

block = dict()

for address in addresses:
    transactions.append(Transaction.Transaction(None, address, 20))

transactions_string = list()
for transaction in transactions:
    transactions_string.append(str(transaction.__dict__))
merkle_tree = Merkle2.Merkletree(transactions_string)
merkle_tree.Make_a_tree()
block['index'] = 1
block['time_stamp'] = time.time()
block['pre_hash'] = None
block['target'] = '000000'
block['merkel_root'] = merkle_tree.Get_Root()
block['transactions'] = transactions
block['nonce'] = None
block['hash'] = sha256(str(block).encode()).hexdigest()

# change all to dict
json_str = json.dumps(block, default=lambda obj: obj.__dict__, sort_keys=False, indent=4)
dict_block = json.loads(json_str)

# deal with db
collection_chain = db['chain']
collection_tree = db['tree']
collection_chain.insert_one(dict_block)
collection_tree.insert_one(merkle_tree.Get_all_hash())


