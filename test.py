import socket

import User
import json

prik1 = '2f387c18177570b293b0d70d05afc810109937ba03957d016d55b40d292fb2c2'
pubk1 = '40b186aa0237862a39f21d068015d79eca211a3540dfd5f089cb64ea498945900f90ba5b2d062bdc137b8d93bed007c9e81e69552d4f4375e7249133546f434e'
addr1 = 'EAtPm4Jfo5t9bVwrXf3Vy3V7CRDeDBPac'

prik2 = 'a84b6cca37985736fe26abfa56725b43ff6dd37c6ddfea3f3324b35b136489bc'
pubk2 = '37b72dbb3ecc35a54bbe575d10da6d999a3ceb36df710adcc114f0b8f43fe857384f2fd44ba72050418f7928ff2a8230bea6b02f6590d3b823efac582cede9c0'
addr2 = '9cGJfg3eRXDN5biwg6dvGK4VKrw2TgyRh'

prik3 = '0a1fe077136d32c3309525f26556368e625915db9e3c1b2cb1be59054acbea0a'
pubk3 = '386bf73734c4d99b43aed374055923c28a1c21135549014593ed5f520c659b1963720141515ee44b0f68c86e074dc9629765f1e5bb8fa9e90d555e8de69ba632'
addr3 = '4MvWGcfFXz9t1dTJh6nvy2fqEjvx6ogku'

prik4 = 'e51c5e570b6f608daeba26979cbe1ad5b34e8622bde46e73e324702523b2eeeb'
pubk4 = '2a6d3ac650897f03a51db8f69c54139f9d9b901e0429152a2a1cb21ba97cd080e73edb6e5b3155d08164c96698fb1c8d3a64e728dbe211436c27e5afe41e90fc'
addr4 = '5KDUxH6XMYdtkv4UGqyEFkv1YRSGLRxhT'

prik5 = '8f0e97e8128c46ac86adef1e9b5a6a717a08f5050491b42cc39d2c271b406242'
pubk5 = 'a095e1a1cad26590be857e5b86115bca27be375995e464bf052ea97ef8f9fdd933ee7eddc0102b5be23d1050f07b30d909fce4f6997918f52e2141ba5ddf651a'
addr5 = '5ocRwLqmf9rAdRm1cFjQbwhUvRMtAt13q'

prik6 = '83e8d1cf43d1d82a1b50bd278a5924b683f2fa4404cc1a4f9c4f8ebcc76a7ae3'
pubk6 = '84925841e18303c7548bf210cec79ad16cab804006dbaf2e227af3d5d47b7d2dddec58dc011f1210d199ae6d94d003490000a19da7cc99bcab7147bc9a6b3829'
addr6 = 'HbjVXPZrub1dFfx5ytUzm2FbDiSbzBvFM'

prik7 = '8805f4c7d2d43fa8ae307a5704032e65ba6777c310111c118bc11814183c1276'
pubk7 = '367ed282146b6e7acc7a4d103c998e16b9b21dc633871f4d00302f5d643ecd0fa5e8bc9b8287df7dbd45a88633046f74dc8b1636caead22116b8aa10e0f8d627'
addr7 = 'KdoaVaLmHqh7gpk3tF6xfzYaSYd8Am13Y'

user1 = User.User(prik1, pubk1, addr1)
user2 = User.User(prik2, pubk2, addr2)
user3 = User.User(prik3, pubk3, addr3)
user4 = User.User(prik4, pubk4, addr4)
user5 = User.User(prik5, pubk5, addr5)
user6 = User.User(prik6, pubk6, addr6)
user7 = User.User(prik7, pubk7, addr7)

users = [user1, user2, user3, user4, user5, user6, user7]
ip = '159.203.74.214'
port = 8888
for temp in users:
    address = input('please input destination address: ').split()
    amount = input('please input your amount: ').split()
    amount = list(map(int, amount))
    temp.generate_transaction(address, amount)
    temp.transaction.generate_sig(private_key=temp.private_key,sour_address=temp.address, dest_address=address,amount=amount)
    transaction_json = json.dumps(temp.transaction, default=lambda obj: obj.__dict__, sort_keys=False, indent=4)
    print('---transaction---')
    print(transaction_json)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    try:
        s.sendall((transaction_json + ' ' + temp.public_key).encode())
        receive_message = s.recv(1024).decode()
        print(receive_message)
    finally:
        s.close()
