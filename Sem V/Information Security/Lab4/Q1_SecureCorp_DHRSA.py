from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import random

class Subsystem:
    def __init__(self, name, dh_prime, dh_generator=2):
        self.name = name
        self.rsa_key = RSA.generate(2048)
        self.public_key = self.rsa_key.publickey()

        self.dh_prime = dh_prime
        self.dh_generator = dh_generator

        self.dh_private_key = random.randint(2, dh_prime - 2)
        self.dh_public_key = pow(self.dh_generator, self.dh_private_key, self.dh_prime)

    def get_rsa_public_key(self):
        return self.public_key.export_key()

    def get_dh_public_key(self):
        return self.dh_public_key

    def generate_shared_secret(self, other_dh_public_key):
        shared_secret = pow(other_dh_public_key, self.dh_private_key, self.dh_prime)
        shared_bytes = long_to_bytes(shared_secret)
        key = SHA256.new(shared_bytes).digest()
        return key

    def rsa_encrypt(self, plaintext_bytes, recipient_rsa_pubkey_bytes):
        recipient_key = RSA.import_key(recipient_rsa_pubkey_bytes)
        cipher = PKCS1_OAEP.new(recipient_key)
        return cipher.encrypt(plaintext_bytes)

    def rsa_decrypt(self, ciphertext_bytes):
        cipher = PKCS1_OAEP.new(self.rsa_key)
        return cipher.decrypt(ciphertext_bytes)

    def aes_encrypt(self, plaintext_bytes, key):
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(plaintext_bytes, AES.block_size))
        return iv + ct_bytes 

    def aes_decrypt(self, ciphertext_bytes, key):
        iv = ciphertext_bytes[:16]
        ct = ciphertext_bytes[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt

class KeyManagementSystem:
    def __init__(self):
        self.subsystems = {}
        self.dh_prime = getPrime(2048)
        self.dh_generator = 2

    def add_subsystem(self, subsystem_name):
        subsystem = Subsystem(subsystem_name, self.dh_prime, self.dh_generator)
        self.subsystems[subsystem_name] = subsystem
        print(f"[KMS] Added subsystem: {subsystem_name}")
        return subsystem

    def revoke_subsystem(self, subsystem_name):
        if subsystem_name in self.subsystems:
            del self.subsystems[subsystem_name]
            print(f"[KMS] Revoked subsystem: {subsystem_name}")
        else:
            print(f"[KMS] Subsystem {subsystem_name} not found")

    def get_subsystem(self, subsystem_name):
        return self.subsystems.get(subsystem_name)

if __name__ == "__main__":
    kms = KeyManagementSystem()

    finance = kms.add_subsystem("Finance")
    hr = kms.add_subsystem("HR")

    finance_dh_pub = finance.get_dh_public_key()
    hr_dh_pub = hr.get_dh_public_key()

    finance_shared_key = finance.generate_shared_secret(hr_dh_pub)
    hr_shared_key = hr.generate_shared_secret(finance_dh_pub)

    assert finance_shared_key == hr_shared_key

    message = b"Confidential Financial Report Q3"
    encrypted_msg = finance.aes_encrypt(message, finance_shared_key)
    print(f"[Finance -> HR] Encrypted message: {encrypted_msg.hex()}")

    decrypted_msg = hr.aes_decrypt(encrypted_msg, hr_shared_key)
    print(f"[HR] Decrypted message: {decrypted_msg.decode()}")
