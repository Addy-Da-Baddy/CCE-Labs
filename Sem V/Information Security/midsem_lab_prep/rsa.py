#!/usr/bin/env python3

"""_Implement a Python program that simulates a secure payment processing system with the following requirements:

- Use the RSA cryptosystem for public-key encryption of payment details (plaintext strings like "Send 55000 to Bob using Mastercard 3048330330393783").
- Use the Schnorr signature scheme for the customer to digitally sign the SHA-512 hash of the plaintext payment details.
- Implement a store for transactions, with roles for Customer, Merchant, and Auditor via interactive menus:
  - *Customer*: Create and "send" a transaction by encrypting the details (RSA), signing the SHA-512 hash (Schnorr), and recording it in history
  - *Merchant*: Process all pending transactions by decrypting (RSA), computing the SHA-512 hash of the decrypted plaintext, verifying it matches the received hash, and verifying the Schnorr signature on the received hash. Record processing results and mark as processed.
  - *Auditor*: View only the received and computed hashes for processed transactions (to check consistency without seeing plaintext), and separately verify Schnorr signatures on the received hashes using the customer's public key.
- Use timestamps from datetime.utcnow.
- Ensure the system demonstrates confidentiality (only merchant decrypts), integrity (hash matching), and auditability (signatures verifiable without plaintext).
- Do not use external files or I/O beyond console input/output.
"""

import sys, time, random
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util import number
from Crypto.Hash import SHA512

# ============================================================
# === RSA ENCRYPTION/DECRYPTION (with OAEP) ==================
# ============================================================

def generate_rsa_keypair(bits=2048):
    key = RSA.generate(bits)
    priv = key
    pub = key.publickey()
    return priv, pub

def rsa_encrypt(pub_key, plaintext_bytes):
    cipher = PKCS1_OAEP.new(pub_key, hashAlgo=SHA512)
    return cipher.encrypt(plaintext_bytes)

def rsa_decrypt(priv_key, ciphertext_bytes):
    cipher = PKCS1_OAEP.new(priv_key, hashAlgo=SHA512)
    return cipher.decrypt(ciphertext_bytes)

# ============================================================
# === SCHNORR SIGNATURE (custom implementation) ==============
# ============================================================

def generate_schnorr_keypair(bits=512):
    # Generate a prime p with q | (p-1)
    q = number.getPrime(bits // 2)
    while True:
        k = number.getRandomRange(2**(bits-2), 2**(bits-1))
        p = q * k + 1
        if number.isPrime(p):
            break
    # generator g of subgroup of order q
    while True:
        g = random.randrange(2, p-1)
        if pow(g, k, p) != 1:
            break
    x = random.randrange(1, q)  # private
    y = pow(g, x, p)            # public
    return {'p': p, 'q': q, 'g': g, 'x': x, 'y': y}

def schnorr_sign(priv, message_bytes):
    p, q, g, x = priv['p'], priv['q'], priv['g'], priv['x']
    k = random.randrange(1, q)
    r = pow(g, k, p)
    e = int.from_bytes(SHA512.new(message_bytes + str(r).encode()).digest(), 'big') % q
    s = (k + x * e) % q
    return (e, s)

def schnorr_verify(pub, signature, message_bytes):
    p, q, g, y = pub['p'], pub['q'], pub['g'], pub['y']
    e, s = signature
    r_check = (pow(g, s, p) * pow(y, -e, p)) % p
    e_check = int.from_bytes(SHA512.new(message_bytes + str(r_check).encode()).digest(), 'big') % q
    return e_check == e

# ============================================================
# === TRANSACTION STORE & MENUS ==============================
# ============================================================

transactions = []
rsa_priv, rsa_pub = generate_rsa_keypair()
schnorr_keys = generate_schnorr_keypair(bits=512)

def customer_menu():
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1) Create & send transaction")
        print("2) Show my public signature key")
        print("0) Back")
        choice = input("> ").strip()
        if choice == "1":
            plaintext = input("Enter payment details (e.g., 'Send 55000 to Bob using Mastercard ...'): ").strip()
            if not plaintext:
                print("Empty transaction aborted."); continue
            tstamp = datetime.utcnow().isoformat() + "Z"
            plaintext_bytes = plaintext.encode()
            try:
                ciphertext = rsa_encrypt(rsa_pub, plaintext_bytes)
            except Exception as e:
                print("Encryption failed:", e); continue
            digest = SHA512.new(plaintext_bytes).digest()
            sig = schnorr_sign(schnorr_keys, digest)
            tx = {
                'id': len(transactions) + 1,
                'timestamp': tstamp,
                'ciphertext': ciphertext,
                'received_hash_hex': digest.hex(),
                'signature': sig,
                'customer_pub': {'p': schnorr_keys['p'], 'q': schnorr_keys['q'], 'g': schnorr_keys['g'], 'y': schnorr_keys['y']},
                'processed': False,
                'merchant_result': None
            }
            transactions.append(tx)
            print("Transaction created and recorded with ID:", tx['id'])
        elif choice == "2":
            print("Schnorr public key (customer):")
            pub = schnorr_keys
            print("p:", pub['p']); print("q:", pub['q']); print("g:", pub['g']); print("y:", pub['y'])
        elif choice == "0":
            return
        else:
            print("Invalid choice")

def merchant_menu():
    while True:
        print("\n--- MERCHANT MENU ---")
        print("1) List pending transactions")
        print("2) Process pending transactions")
        print("3) Show processed transaction details (except plaintext)")
        print("0) Back")
        choice = input("> ").strip()
        if choice == "1":
            pend = [t for t in transactions if not t['processed']]
            if not pend:
                print("No pending transactions.")
            else:
                for t in pend:
                    print(f"ID:{t['id']} ts:{t['timestamp']} hash:{t['received_hash_hex'][:16]}... sig_e:{t['signature'][0]}")
        elif choice == "2":
            for t in transactions:
                if t['processed']: continue
                print(f"\nProcessing transaction ID {t['id']} ...")
                c = t['ciphertext']
                try:
                    payload = rsa_decrypt(rsa_priv, c)
                except Exception as e:
                    print("Decryption failed:", e)
                    t['processed'] = True
                    t['merchant_result'] = {'success': False, 'reason': 'decryption_failed'}
                    continue
                computed_digest = SHA512.new(payload).digest()
                computed_hex = computed_digest.hex()
                received_hex = t['received_hash_hex']
                hash_match = (computed_hex == received_hex)
                sig_ok = schnorr_verify(t['customer_pub'], t['signature'], computed_digest)
                t['processed'] = True
                t['merchant_result'] = {
                    'success': True,
                    'plaintext': payload.decode(errors='replace'),
                    'computed_hash_hex': computed_hex,
                    'hash_match': hash_match,
                    'signature_valid': sig_ok,
                    'processing_time': datetime.utcnow().isoformat() + "Z"
                }
                print("Decryption successful.")
                print("Computed hash matches received hash:", hash_match)
                print("Schnorr signature valid:", sig_ok)
        elif choice == "3":
            for t in transactions:
                if not t['processed']: continue
                mr = t['merchant_result'] or {}
                print(f"\nID: {t['id']}")
                print("Timestamp:", t['timestamp'])
                print("Received hash:", t['received_hash_hex'])
                print("Computed hash:", mr.get('computed_hash_hex'))
                print("Hash match:", mr.get('hash_match'))
                print("Signature valid:", mr.get('signature_valid'))
                print("Processed at:", mr.get('processing_time'))
        elif choice == "0":
            return
        else:
            print("Invalid choice")

def auditor_menu():
    while True:
        print("\n--- AUDITOR MENU ---")
        print("1) List processed transactions (hashes only)")
        print("2) Verify signature for a processed transaction")
        print("0) Back")
        choice = input("> ").strip()
        if choice == "1":
            processed = [t for t in transactions if t['processed']]
            if not processed:
                print("No processed transactions.")
            else:
                for t in processed:
                    mr = t['merchant_result'] or {}
                    print(f"ID:{t['id']} ts:{t['timestamp']} received_hash:{t['received_hash_hex'][:20]}... computed_hash:{mr.get('computed_hash_hex','')[:20]}... sig_e:{t['signature'][0]}")
        elif choice == "2":
            tid = input("Enter transaction ID to verify: ").strip()
            if not tid.isdigit(): print("Invalid ID"); continue
            tid = int(tid)
            t = next((x for x in transactions if x['id'] == tid), None)
            if not t: print("Transaction not found"); continue
            if not t['processed']: print("Transaction not processed yet"); continue
            received_hash_hex = t['received_hash_hex']
            received_hash_bytes = bytes.fromhex(received_hash_hex)
            ok = schnorr_verify(t['customer_pub'], t['signature'], received_hash_bytes)
            print("Signature valid on received hash (auditor check):", ok)
        elif choice == "0":
            return
        else:
            print("Invalid choice")

def main_menu():
    print("Secure Payment Processing Simulation (RSA + Schnorr)")
    while True:
        print("\nMain Menu:")
        print("1) Customer")
        print("2) Merchant")
        print("3) Auditor")
        print("4) Show system keys (debug)")
        print("0) Exit")
        choice = input("> ").strip()
        if choice == "1":
            customer_menu()
        elif choice == "2":
            merchant_menu()
        elif choice == "3":
            auditor_menu()
        elif choice == "4":
            print("\nRSA public key (n,e):", rsa_pub.n, rsa_pub.e)
            print("Schnorr public (p,q,g,y):", schnorr_keys['p'], schnorr_keys['q'], schnorr_keys['g'], schnorr_keys['y'])
        elif choice == "0":
            print("Exiting."); sys.exit(0)
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main_menu()
