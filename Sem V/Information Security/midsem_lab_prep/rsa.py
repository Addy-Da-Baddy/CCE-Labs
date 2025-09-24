#!/usr/bin/env python3
"""
Secure Payment Simulation using PyCryptodome RSA + Schnorr SHA-512 signatures

Roles:
- Customer: Creates and encrypts payment transactions, signs them.
- Merchant: Decrypts and verifies transactions.
- Auditor: Checks hashes and signatures without seeing plaintext.
"""

import sys, random
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512
from Crypto.Util import number

# ----------------- UTILITY FUNCTIONS -----------------
def hash_bytes(data: bytes) -> bytes:
    """Compute SHA-512 digest of the input bytes."""
    return SHA512.new(data).digest()

def int_to_bytes(i: int, length: int) -> bytes:
    """Convert integer i to bytes of given length."""
    return i.to_bytes(length, 'big')

# ----------------- RSA ENCRYPTION/DECRYPTION -----------------
def generate_rsa_keypair(bits=2048):
    """
    Generate RSA keypair using PyCryptodome.
    Returns (private_key, public_key)
    """
    key = RSA.generate(bits)
    return key, key.publickey()

def rsa_encrypt(pub_key: RSA.RsaKey, plaintext: bytes) -> bytes:
    """
    Encrypt plaintext using RSA + OAEP.
    pub_key: RSA public key
    plaintext: bytes
    Returns ciphertext bytes
    """
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(plaintext)

def rsa_decrypt(priv_key: RSA.RsaKey, ciphertext: bytes) -> bytes:
    """
    Decrypt ciphertext using RSA + OAEP.
    priv_key: RSA private key
    ciphertext: bytes
    Returns plaintext bytes
    """
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)

# ----------------- SCHNORR SIGNATURE -----------------
def generate_schnorr_keypair(bits=512):
    """
    Generate Schnorr-like keypair over prime field.
    Returns dict with p, g, x (private), y (public)
    """
    while True:
        p = number.getPrime(bits)
        if p % 4 == 3:  # Schnorr-friendly prime
            break
    g = 2
    x = random.randint(1, p-2)
    y = pow(g, x, p)
    return {'p': p, 'g': g, 'x': x, 'y': y}

def schnorr_sign(priv_key: dict, message_bytes: bytes):
    """
    Sign message using Schnorr-style scheme.
    Returns tuple (R, s)
    """
    h = SHA512.new(message_bytes).digest()
    h_int = int.from_bytes(h, 'big')
    k = random.randint(1, priv_key['p']-2)
    R = pow(priv_key['g'], k, priv_key['p'])
    e = SHA512.new(int_to_bytes(R, priv_key['p'].bit_length()//8) + message_bytes).digest()
    e_int = int.from_bytes(e, 'big') % (priv_key['p']-1)
    s = (k - priv_key['x'] * e_int) % (priv_key['p']-1)
    return (R, s)

def schnorr_verify(pub_key: dict, signature: tuple, message_bytes: bytes) -> bool:
    """
    Verify Schnorr signature (R, s) on message_bytes
    Returns True if valid, False otherwise
    """
    R, s = signature
    e = SHA512.new(int_to_bytes(R, pub_key['p'].bit_length()//8) + message_bytes).digest()
    e_int = int.from_bytes(e, 'big') % (pub_key['p']-1)
    left = pow(pub_key['g'], s, pub_key['p']) * pow(pub_key['y'], e_int, pub_key['p']) % pub_key['p']
    return left == R

# ----------------- TRANSACTION STORE -----------------
transactions = []
rsa_priv_key, rsa_pub_key = generate_rsa_keypair()
schnorr_key_customer = generate_schnorr_keypair(bits=512)

# ----------------- CUSTOMER FUNCTIONS -----------------
def create_transaction(plaintext: str):
    """
    Customer creates a transaction:
    1. Encrypts plaintext using RSA
    2. Computes SHA-512 digest
    3. Signs digest using Schnorr
    4. Stores transaction
    """
    plaintext_bytes = plaintext.encode()
    ciphertext = rsa_encrypt(rsa_pub_key, plaintext_bytes)
    digest = hash_bytes(plaintext_bytes)
    signature = schnorr_sign(schnorr_key_customer, plaintext_bytes)
    tx = {
        'id': len(transactions)+1,
        'timestamp': datetime.utcnow().isoformat()+'Z',
        'ciphertext': ciphertext,
        'received_hash_hex': digest.hex(),
        'signature': signature,
        'customer_pub': schnorr_key_customer,
        'processed': False,
        'merchant_result': None
    }
    transactions.append(tx)
    print(f"Transaction created with ID {tx['id']}")

# ----------------- MERCHANT FUNCTIONS -----------------
def process_transaction(tx: dict):
    """
    Merchant decrypts transaction, computes digest, and verifies signature.
    """
    try:
        plaintext_bytes = rsa_decrypt(rsa_priv_key, tx['ciphertext'])
    except Exception:
        tx['processed'] = True
        tx['merchant_result'] = {'success': False, 'reason': 'decryption_failed'}
        return
    computed_digest = hash_bytes(plaintext_bytes)
    hash_match = (computed_digest.hex() == tx['received_hash_hex'])
    sig_ok = schnorr_verify(tx['customer_pub'], tx['signature'], plaintext_bytes)
    tx['processed'] = True
    tx['merchant_result'] = {
        'success': True,
        'computed_hash_hex': computed_digest.hex(),
        'hash_match': hash_match,
        'signature_valid': sig_ok,
        'processed_at': datetime.utcnow().isoformat()+'Z'
    }

# ----------------- MAIN MENU -----------------
def main_menu():
    while True:
        print("\n--- MAIN MENU ---")
        print("1) Customer: create transaction")
        print("2) Merchant: process pending transactions")
        print("3) Show all transactions (hashes & results)")
        print("0) Exit")
        choice = input("> ").strip()
        if choice == "1":
            plaintext = input("Enter payment details: ").strip()
            if plaintext:
                create_transaction(plaintext)
        elif choice == "2":
            for tx in transactions:
                if not tx['processed']:
                    process_transaction(tx)
        elif choice == "3":
            for tx in transactions:
                print(f"ID {tx['id']} ts {tx['timestamp']}")
                print("Received hash:", tx['received_hash_hex'])
                if tx['processed']:
                    mr = tx['merchant_result']
                    print("Hash match:", mr['hash_match'], "Signature valid:", mr['signature_valid'])
                else:
                    print("Not yet processed")
                print("-"*40)
        elif choice == "0":
            sys.exit(0)
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main_menu()
