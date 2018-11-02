import hashlib
import base58
import random
import ecdsa
from binascii import hexlify, unhexlify


def ripemd160(s):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(unhexlify(s))
    return ripemd160.digest()


def get_address(public_key):
    pkbin = unhexlify(public_key)
    addressbin = ripemd160(hexlify(hashlib.sha256(pkbin).digest()))
    temp = '00' + hexlify(addressbin).decode('ascii')
    address = base58.b58encode_check(bytes.fromhex(temp))
    return address


class GenerateKey:

    def __init__(self):
        pass

    def generateKeyDefault(self):
        # generate a random 1000-bits string then do sha256 to get private key, public key and address
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        random_chars = []
        for i in range(1000):
            random_chars.append(random.choice(seed))
        random_string = ''.join(random_chars)
        # generate private key through sha256
        private_key_hex = hashlib.sha256(random_string.encode('ascii')).hexdigest()

        # generate private key wif format
        private_key_hex_wif_unencode = '80' + private_key_hex + '01'
        private_key_hex_wif = base58.b58encode_check(bytes.fromhex(private_key_hex_wif_unencode))

        # generate public key through SECP256k1
        secret = unhexlify(private_key_hex)
        order = ecdsa.SigningKey.from_string(secret, curve=ecdsa.SECP256k1).curve.generator.order()
        p = ecdsa.SigningKey.from_string(secret, curve=ecdsa.SECP256k1).verifying_key.pubkey.point
        x_str = ecdsa.util.number_to_string(p.x(), order)
        y_str = ecdsa.util.number_to_string(p.y(), order)
        compressed_public_key_hex = hexlify(bytes(chr(2 + (p.y() & 1)), 'ascii') + x_str).decode('ascii')
        uncompressed_public_key_hex = hexlify(bytes(chr(4), 'ascii') + x_str + y_str).decode('ascii')

        # generate address through public key
        address = get_address(compressed_public_key_hex)

        return private_key_hex, private_key_hex_wif, compressed_public_key_hex, uncompressed_public_key_hex, address



    def genrateKeyByGUI(self):
        pass
