#!/usr/bin/env python3


"""_Implement a Python program that simulates a secure payment processing system with the following requirements:

- Use the Rabin cryptosystem for public-key encryption of payment details (plaintext strings like "Send 55000 to Bob using Mastercard 3048330330393783"). T

- Use the ElGamal signature scheme for the customer to digitally sign the SHA-512 hash of the plaintext payment details.

- Implement a store for transactions, with roles for Customer, Merchant, and Auditor via interactive menus:
  - *Customer*: Create and "send" a transaction by encrypting the details (Rabin), signing the SHA-512 hash (ElGamal), and recording it in history
  - *Merchant*: Process all pending transactions by decrypting (Rabin, finding the valid root), computing the SHA-512 hash of the decrypted plaintext, verifying it matches the received hash, and verifying the ElGamal signature on the received hash. Record processing resultsand mark as processed.
  - *Auditor*: View only the received and computed hashes for processed transactions (to check consistency without seeing plaintext), and separately verify ElGamal signatures on the received hashes using the customer's public key.
. Use timestamps from

- Ensure the system demonstrates confidentiality (only merchant decrypts), integrity (hash matching), and auditability (signatures verifiable without plaintext). Do not use external files or I/O beyond console input/output.
    """



import sys, random, time
from datetime import datetime
from Crypto.Util import number
from Crypto.Hash import SHA512

MARKER = b'[PAYMENT]'
END_MARK = b'END'
CHECKSUM_LEN = 8

def int_to_bytes(i, length):
    return i.to_bytes(length, byteorder='big')

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')

def generate_rabin_keypair(bits=512):
    while True:
        p = number.getPrime(bits)
        q = number.getPrime(bits)
        if p % 4 == 3 and q % 4 == 3 and p != q:
            break
    n = p * q
    return {'p': p, 'q': q, 'n': n}

def rabin_encrypt(pub, plaintext_bytes):
    n = pub['n']
    k = (n.bit_length() + 7) // 8
    checksum = SHA512.new(plaintext_bytes).digest()[:CHECKSUM_LEN]
    m_bytes = MARKER + plaintext_bytes + b'|' + checksum + END_MARK
    if len(m_bytes) > k:
        raise ValueError("Plaintext too long for key size")
    m_bytes_padded = m_bytes.rjust(k, b'\x00')
    m_int = bytes_to_int(m_bytes_padded)
    c = pow(m_int, 2, n)
    return c

def rabin_decrypt(priv, c):
    p = priv['p']; q = priv['q']; n = priv['n']
    k = (n.bit_length() + 7) // 8
    r_p = pow(c, (p + 1) // 4, p)
    r_q = pow(c, (q + 1) // 4, q)
    inv_p_mod_q = pow(p, -1, q)
    roots = []
    for s1 in (r_p, (-r_p) % p):
        for s2 in (r_q, (-r_q) % q):
            u = (s2 - s1) % q
            t = (u * inv_p_mod_q) % q
            x = (s1 + p * t) % n
            roots.append(x)
    for root in roots:
        b = int_to_bytes(root, k)
        # find marker anywhere (handles leading zeros)
        start = b.find(MARKER)
        if start == -1:
            continue
        end = b.find(END_MARK, start + len(MARKER))
        if end == -1:
            continue
        inner = b[start + len(MARKER):end]
        # inner should be msg|checksum
        if b'|' not in inner:
            continue
        msg, cs = inner.rsplit(b'|', 1)
        if len(cs) != CHECKSUM_LEN:
            continue
        if SHA512.new(msg).digest()[:CHECKSUM_LEN] == cs:
            return msg, root
    return None, None

def generate_elgamal_keypair(bits=512):
    while True:
        p = number.getPrime(bits)
        if p > 3:
            break
    g = 2
    x = random.randint(2, p - 2)
    y = pow(g, x, p)
    return {'p': p, 'g': g, 'y': y, 'x': x}

def elgamal_sign_digest(key_priv, digest_bytes):
    p = key_priv['p']; g = key_priv['g']; x = key_priv['x']
    h_int = int.from_bytes(digest_bytes, 'big') % (p - 1)
    while True:
        k = random.randint(2, p - 2)
        if number.GCD(k, p - 1) == 1:
            break
    r = pow(g, k, p)
    k_inv = pow(k, -1, p - 1)
    s = (k_inv * (h_int - x * r)) % (p - 1)
    return (r, s)

def elgamal_verify_digest(key_pub, signature, digest_bytes):
    p = key_pub['p']; g = key_pub['g']; y = key_pub['y']
    r, s = signature
    if not (0 < r < p):
        return False
    h_int = int.from_bytes(digest_bytes, 'big') % (p - 1)
    left = pow(g, h_int, p)
    right = (pow(y, r, p) * pow(r, s, p)) % p
    return left == right

transactions = []
rabin_keys = generate_rabin_keypair(bits=512)
elgamal_key_customer = generate_elgamal_keypair(bits=512)

def customer_menu():
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1) Create & send transaction")
        print("2) Show my public signature key")
        print("0) Back")
        choice = input("> ").strip()
        if choice == "1":
            plaintext = input("Enter payment details (e.g., 'Send 55000 to Bob using Mastercard ...'): ").strip()
            if plaintext == "":
                print("Empty transaction aborted."); continue
            tstamp = datetime.utcnow().isoformat() + "Z"
            plaintext_bytes = plaintext.encode()
            try:
                ciphertext = rabin_encrypt(rabin_keys, plaintext_bytes)
            except Exception as e:
                print("Encryption failed:", e); continue
            digest = SHA512.new(plaintext_bytes).digest()
            sig = elgamal_sign_digest(elgamal_key_customer, digest)
            tx = {
                'id': len(transactions) + 1,
                'timestamp': tstamp,
                'ciphertext': ciphertext,
                'received_hash_hex': digest.hex(),
                'signature': sig,
                'customer_pub': {'p': elgamal_key_customer['p'], 'g': elgamal_key_customer['g'], 'y': elgamal_key_customer['y']},
                'processed': False,
                'merchant_result': None
            }
            transactions.append(tx)
            print("Transaction created and recorded with ID:", tx['id'])
        elif choice == "2":
            pub = elgamal_key_customer
            print("ElGamal public key (customer):")
            print("p:", pub['p'])
            print("g:", pub['g'])
            print("y:", pub['y'])
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
                    print(f"ID:{t['id']} ts:{t['timestamp']} hash:{t['received_hash_hex'][:16]}... sig_r:{t['signature'][0]}")
        elif choice == "2":
            for t in transactions:
                if t['processed']: continue
                print(f"\nProcessing transaction ID {t['id']} ...")
                c = t['ciphertext']
                payload, root = rabin_decrypt(rabin_keys, c)
                if payload is None:
                    print("Failed to find valid Rabin root -> cannot decrypt. Marking failed.")
                    t['processed'] = True
                    t['merchant_result'] = {'success': False, 'reason': 'decryption_failed'}
                    continue
                computed_digest = SHA512.new(payload).digest()
                computed_hex = computed_digest.hex()
                received_hex = t['received_hash_hex']
                hash_match = (computed_hex == received_hex)
                sig_ok = elgamal_verify_digest(t['customer_pub'], t['signature'], computed_digest)
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
                print("ElGamal signature valid:", sig_ok)
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
                    print(f"ID:{t['id']} ts:{t['timestamp']} received_hash:{t['received_hash_hex'][:20]}... computed_hash:{mr.get('computed_hash_hex','')[:20]}... sig_r:{t['signature'][0]}")
        elif choice == "2":
            tid = input("Enter transaction ID to verify: ").strip()
            if not tid.isdigit(): print("Invalid ID"); continue
            tid = int(tid)
            t = next((x for x in transactions if x['id'] == tid), None)
            if not t: print("Transaction not found"); continue
            if not t['processed']: print("Transaction not processed yet"); continue
            received_hash_hex = t['received_hash_hex']
            received_hash_bytes = bytes.fromhex(received_hash_hex)
            ok = elgamal_verify_digest(t['customer_pub'], t['signature'], received_hash_bytes)
            print("Signature valid on received hash (auditor check):", ok)
        elif choice == "0":
            return
        else:
            print("Invalid choice")

def main_menu():
    print("Secure Payment Processing Simulation (Rabin + ElGamal) - FIXED")
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
            print("\nRabin public modulus n:", rabin_keys['n'])
            print("ElGamal public (customer): p,g,y:", elgamal_key_customer['p'], elgamal_key_customer['g'], elgamal_key_customer['y'])
        elif choice == "0":
            print("Exiting."); sys.exit(0)
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main_menu()
