# seller_client.py
import socket, json, time, sys
from paillier_rsa_utils import PaillierKeypair, hex_to_int, int_to_hex, hex_to_bytes, bytes_to_hex
from paillier_rsa_utils import rsa_verify
import random

HOST = "localhost"
PORT = 10000

def send_request(obj):
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(json.dumps(obj).encode())
    resp = s.recv(64_000).decode()
    s.close()
    return json.loads(resp)

def get_pubkeys():
    return send_request({"type": "get_pubkeys"})

def submit_tx(seller_name, cipher_hex):
    return send_request({"type": "submit_tx", "seller": seller_name, "tx": cipher_hex})

def get_signed_summary():
    return send_request({"type": "get_signed_summary"})

def run_seller(seller_name, amounts):
    # Obtain Paillier public key
    keys = get_pubkeys()
    n = hex_to_int(keys["paillier"]["n"])
    g = hex_to_int(keys["paillier"]["g"])
    rsa_pub_hex = keys["rsa_pub"]
    print(f"[{seller_name}] Received gateway public keys.")

    # For encryption client-side we need a Paillier *public-only* encryptor:
    # We'll implement a simple public-only encrypt here (no decryption).
    nsq = n * n
    def encrypt_public(m: int):
        # use simple random r coprime to n
        r = random.randrange(1, n)
        # ensure gcd(r,n)==1
        from Crypto.Util.number import GCD
        while GCD(r, n) != 1:
            r = random.randrange(1, n)
        c = (pow(g, m, nsq) * pow(r, n, nsq)) % nsq
        return c

    print(f"[{seller_name}] Encrypting and submitting {len(amounts)} txs...")
    for amt in amounts:
        c = encrypt_public(amt)
        hexc = int_to_hex(c)
        submit_tx(seller_name, hexc)
        print(f"[{seller_name}] submitted amount {amt} -> cipher hex {hexc[:32]}...")

def verify_and_print_summary():
    resp = get_signed_summary()
    if "error" in resp:
        print("Error from gateway:", resp["error"])
        return
    summary = resp["summary"]
    sig = bytes.fromhex(resp["signature_hex"])
    rsa_pub = bytes.fromhex(resp["rsa_pub_hex"])
    # Build canonical message bytes to verify (must match server's sorted dump)
    summary_bytes = json.dumps(summary, sort_keys=True).encode()
    signature_valid = rsa_verify(rsa_pub, summary_bytes, sig)
    
    print("\n" + "="*70)
    print("📊 COMPLETE TRANSACTION SUMMARY - ALL SELLERS")
    print("="*70)
    
    print("\n🔐 DIGITAL SIGNATURE VERIFICATION:")
    print(f"  • Signature Status: {'SIGNED' if sig else 'NOT SIGNED'}")
    print(f"  • Verification Result: {'✓ VALID' if signature_valid else '✗ INVALID'}")
    print(f"  • Hash Algorithm: SHA-256")
    print(f"  • Signature Algorithm: RSA-2048")
    print(f"  • Signature (hex): {resp['signature_hex'][:60]}...")
    
    if not summary:
        print("\n[!] No transactions in the system yet.")
        print("="*70)
        return
    
    for seller, info in summary.items():
        print("\n" + "-"*70)
        print(f"🏪 SELLER: {seller}")
        print("-"*70)
        
        print("\n  📋 Individual Transaction Details:")
        total_plain = 0
        for idx, (enc_hex, dec_amt) in enumerate(zip(info["individual_cipher_hex"], 
                                                       info["individual_decrypted"]), 1):
            print(f"    Transaction #{idx}:")
            print(f"      • Amount: {dec_amt}")
            print(f"      • Encrypted (hex): {enc_hex[:40]}...")
            print(f"      • Decrypted: {dec_amt}")
            total_plain += dec_amt
        
        print(f"\n  📊 Aggregated Summary:")
        print(f"    • Total Transactions: {len(info['individual_decrypted'])}")
        print(f"    • Sum of Individual Amounts: {total_plain}")
        print(f"    • Total Encrypted (hex): {info['total_cipher_hex'][:40]}...")
        print(f"    • Total Decrypted (Homomorphic): {info['total_decrypted']}")
        print(f"    • Verification: {'✓ MATCH' if total_plain == info['total_decrypted'] else '✗ MISMATCH'}")
    
    print("\n" + "="*70)
    print(f"Total Sellers: {len(summary)}")
    total_all = sum(info['total_decrypted'] for info in summary.values())
    print(f"Grand Total (All Sellers): {total_all}")
    print("="*70)

# Demo helper to simulate two sellers each with many txs
def demo_run():
    # Seller A and Seller B with at least two transactions each
    sellers = {
        "SellerA": [100, 250, 50],
        "SellerB": [40, 60, 300]
    }
    # Submit transactions
    for s, txs in sellers.items():
        run_seller(s, txs)
    # Give server a small moment to aggregate
    time.sleep(1)
    # Get summary and verify
    verify_and_print_summary()

def get_seller_info(seller_name):
    """Get and display transaction summary for a specific seller"""
    resp = get_signed_summary()
    if "error" in resp:
        print("Error from gateway:", resp["error"])
        return
    
    summary = resp["summary"]
    sig = bytes.fromhex(resp["signature_hex"])
    rsa_pub = bytes.fromhex(resp["rsa_pub_hex"])
    
    # Build canonical message bytes to verify
    summary_bytes = json.dumps(summary, sort_keys=True).encode()
    signature_valid = rsa_verify(rsa_pub, summary_bytes, sig)
    
    # Check if seller exists
    if seller_name not in summary:
        print(f"\n[!] No transactions found for seller '{seller_name}'")
        return
    
    info = summary[seller_name]
    
    print("\n" + "="*60)
    print(f"TRANSACTION SUMMARY FOR: {seller_name}")
    print("="*60)
    
    print("\n📋 INDIVIDUAL TRANSACTIONS:")
    print("-" * 60)
    for idx, (enc_hex, dec_amt) in enumerate(zip(info["individual_cipher_hex"], 
                                                   info["individual_decrypted"]), 1):
        print(f"  Transaction #{idx}:")
        print(f"    • Amount: {dec_amt}")
        print(f"    • Encrypted (hex): {enc_hex[:40]}...")
        print(f"    • Decrypted: {dec_amt}")
    
    print("\n" + "-" * 60)
    print("📊 TOTAL SUMMARY:")
    print(f"    • Total Encrypted (hex): {info['total_cipher_hex'][:40]}...")
    print(f"    • Total Decrypted Amount: {info['total_decrypted']}")
    print(f"    • Number of Transactions: {len(info['individual_decrypted'])}")
    
    print("\n" + "-" * 60)
    print("🔐 DIGITAL SIGNATURE:")
    print(f"    • Signature Status: {'SIGNED' if sig else 'NOT SIGNED'}")
    print(f"    • Signature Verification: {'✓ VALID' if signature_valid else '✗ INVALID'}")
    print(f"    • Hash Algorithm: SHA-256")
    print(f"    • Signature Algorithm: RSA-2048")
    
    print("="*60)

def interactive_mode():
    """Interactive menu for sellers"""
    print("\n" + "="*60)
    print("🏦 PAYMENT GATEWAY - SELLER PORTAL")
    print("="*60)
    
    seller_name = input("\nEnter your Seller Name: ").strip()
    
    while True:
        print("\n" + "-"*60)
        print(f"Logged in as: {seller_name}")
        print("-"*60)
        print("1. Submit New Transaction(s)")
        print("2. View My Transaction Summary & Report")
        print("3. View All Sellers Summary (Admin View)")
        print("4. Switch Seller / Exit")
        print("-"*60)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\n--- Submit New Transaction(s) ---")
            txs_raw = input("Enter transaction amounts (comma-separated, e.g., 100,250,50): ")
            try:
                txs = [int(x.strip()) for x in txs_raw.split(",") if x.strip()]
                if not txs:
                    print("[!] No valid transactions entered.")
                    continue
                run_seller(seller_name, txs)
                print(f"[✓] Successfully submitted {len(txs)} transaction(s)!")
            except ValueError:
                print("[!] Invalid input. Please enter numbers only.")
        
        elif choice == "2":
            print("\n--- Your Transaction Summary ---")
            get_seller_info(seller_name)
        
        elif choice == "3":
            print("\n--- All Sellers Summary ---")
            verify_and_print_summary()
        
        elif choice == "4":
            print("\n[✓] Logging out... Goodbye!")
            break
        
        else:
            print("[!] Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "demo":
        demo_run()
    else:
        interactive_mode()
