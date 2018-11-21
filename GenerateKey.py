import hashlib
import base58
from ecdsa import SigningKey, SECP256k1
from binascii import hexlify, unhexlify


def ripemd160(s):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(unhexlify(s))
    return ripemd160.digest()


def get_address(public_key):
    pk_bin = unhexlify(public_key)
    address_bin = ripemd160(hexlify(hashlib.sha256(pk_bin).digest()))
    temp = hexlify(address_bin).decode('ascii')
    address = base58.b58encode_check(bytes.fromhex(temp))
    return address


class GenerateKey:

    @staticmethod
    def generate_key():
        # use ecdsa generate private key and public key
        private_key_obj = SigningKey.generate(curve=SECP256k1)
        public_key_obj = private_key_obj.get_verifying_key()
        private_key_bytes = private_key_obj.to_string()
        private_key = hexlify(private_key_bytes).decode()
        public_key_bytes = public_key_obj.to_string()
        public_key = hexlify(public_key_bytes).decode()
        address = get_address(public_key)
        return private_key, public_key, address

    @staticmethod
    def generate_sign(private_key, data):
        private_key_obj = SigningKey.from_string(unhexlify(private_key), curve=SECP256k1)
        signature = private_key_obj.sign(data.encode())
        return signature

    @staticmethod
    def verify_public_key(public_key, address):
        temp_address = get_address(public_key)
        if address == temp_address:
            return True
        else:
            return False

    @staticmethod
    def verify_sign(public_key, sign, data):
        public_key_obj = SigningKey.from_string(unhexlify(public_key), curve=SECP256k1)
        return public_key_obj.verify(sign, data.encode())