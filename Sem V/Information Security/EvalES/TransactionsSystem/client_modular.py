# client_modular.py
import socket, json, time
import config
from crypto_modular import TransactionCrypto, SignatureEngine, hex_to_int, int_to_hex

HOST = config.SERVER_HOST
PORT = config.SERVER_PORT

def send_request(obj):
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(json.dumps(obj).encode())
    resp = s.recv(128_000).decode()
    s.close()
    return json.loads(resp)

def get_config():
    return send_request({"type": "get_config"})

def get_pubkeys():
    return send_request({"type": "get_pubkeys"})

def submit_tx(seller_name, cipher_hex):
    return send_request({"type": "submit_tx", "seller": seller_name, "tx": cipher_hex})

def multiply_tx(seller_name, scalar):
    return send_request({"type": "multiply_tx", "seller": seller_name, "scalar": scalar})

def get_signed_summary():
    return send_request({"type": "get_signed_summary"})

def run_seller(seller_name, amounts):
    # Get public keys from gateway
    keys = get_pubkeys()
    tx_params = keys["transaction"]
    
    print(f"[{seller_name}] Received gateway public keys.")
    print(f"  • Encryption: {tx_params['mode']}")
    
    # Initialize local crypto with server's public parameters
    if tx_params['mode'] == "Paillier":
        from crypto_modular import TransactionCrypto
        local_crypto = TransactionCrypto("Paillier")
        local_crypto.n = tx_params["n"]
        local_crypto.g = tx_params["g"]
        local_crypto.n_sq = local_crypto.n * local_crypto.n
    elif tx_params['mode'] == "RSA":
        from crypto_modular import TransactionCrypto
        local_crypto = TransactionCrypto("RSA")
        local_crypto.n = tx_params["n"]
        local_crypto.e = tx_params["e"]
        local_crypto.base = tx_params.get("base", 3)
    
    print(f"[{seller_name}] Encrypting and submitting {len(amounts)} transaction(s)...")
    for amt in amounts:
        c = local_crypto.encrypt(amt)
        hexc = int_to_hex(c)
        submit_tx(seller_name, hexc)
        print(f"  • Submitted amount {amt} -> cipher {hexc[:32]}...")
    
    print(f"[{seller_name}] ✓ All transactions submitted!")

def multiply_seller_transactions():
    """Multiply a seller's total transactions by a scalar"""
    print("\n--- Multiply Transactions (Homomorphic) ---")
    seller_name = input("Enter Seller Name: ").strip()
    
    try:
        scalar = int(input("Enter multiplier (e.g., 2 for double, 3 for triple): ").strip())
    except ValueError:
        print("[!] Invalid multiplier")
        return
    
    result = multiply_tx(seller_name, scalar)
    
    if result.get("status") == "ok":
        print(f"\n✓ Transaction multiplication successful!")
        print(f"  • Seller: {seller_name}")
        print(f"  • Multiplier: {scalar}")
        print(f"  • Result (encrypted hex): {result['result_encrypted_hex'][:40]}...")
        print(f"  • Result (decrypted): {result['result_decrypted']}")
        print(f"\n  Note: Computed {seller_name}'s total × {scalar} while encrypted!")
    else:
        print(f"✗ Error: {result.get('msg', 'Unknown error')}")

def verify_and_print_summary():
    resp = get_signed_summary()
    if "error" in resp:
        print("Error from gateway:", resp["error"])
        return
    
    summary = resp["summary"]
    signature = resp["signature"]
    sig_pubkey = resp["signature_pubkey"]
    crypto_config = resp.get("crypto_config", {})
    
    # Verify signature
    summary_bytes = json.dumps({"summary": summary, "config": crypto_config}, sort_keys=True).encode()
    sig_engine = SignatureEngine(crypto_config.get("signature_algorithm"), crypto_config.get("signature_hash"))
    signature_valid = sig_engine.verify(summary_bytes, signature, sig_pubkey)
    
    print("\n" + "="*70)
    print("📊 COMPLETE TRANSACTION SUMMARY - ALL SELLERS")
    print("="*70)
    
    print("\n📋 CRYPTOGRAPHIC CONFIGURATION:")
    print(f"  • Transaction Encryption: {crypto_config.get('transaction_encryption')}")
    print(f"  • Signature Algorithm: {crypto_config.get('signature_algorithm')}")
    print(f"  • Signature Hash: {crypto_config.get('signature_hash')}")
    
    print("\n🔐 DIGITAL SIGNATURE VERIFICATION:")
    print(f"  • Signature Status: {'SIGNED' if signature else 'NOT SIGNED'}")
    print(f"  • Verification Result: {'✓ VALID' if signature_valid else '✗ INVALID'}")
    print(f"  • Algorithm: {crypto_config.get('signature_algorithm')}")
    print(f"  • Hash: {crypto_config.get('signature_hash')}")
    
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

def get_seller_info(seller_name):
    """Get and display transaction summary for a specific seller"""
    resp = get_signed_summary()
    if "error" in resp:
        print("Error from gateway:", resp["error"])
        return
    
    summary = resp["summary"]
    signature = resp["signature"]
    sig_pubkey = resp["signature_pubkey"]
    crypto_config = resp.get("crypto_config", {})
    
    # Verify signature
    summary_bytes = json.dumps({"summary": summary, "config": crypto_config}, sort_keys=True).encode()
    sig_engine = SignatureEngine(crypto_config.get("signature_algorithm"), crypto_config.get("signature_hash"))
    signature_valid = sig_engine.verify(summary_bytes, signature, sig_pubkey)
    
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
    print(f"    • Signature Status: {'SIGNED' if signature else 'NOT SIGNED'}")
    print(f"    • Signature Verification: {'✓ VALID' if signature_valid else '✗ INVALID'}")
    print(f"    • Algorithm: {crypto_config.get('signature_algorithm')}")
    print(f"    • Hash: {crypto_config.get('signature_hash')}")
    
    print("="*60)

def interactive_mode():
    """Interactive menu for sellers"""
    print("\n" + "="*70)
    print("🏦 MODULAR PAYMENT GATEWAY - SELLER PORTAL")
    print("="*70)
    
    # Display server configuration
    try:
        cfg = get_config()
        print("\n📋 Server Configuration:")
        print(f"  • Transaction Encryption: {cfg['transaction_encryption']}")
        print(f"  • Signature Algorithm: {cfg['signature_algorithm']}")
        print(f"  • Signature Hash: {cfg['signature_hash']}")
    except:
        print("\n[!] Could not fetch server configuration")
    
    seller_name = input("\nEnter your Seller Name: ").strip()
    
    while True:
        print("\n" + "-"*70)
        print(f"Logged in as: {seller_name}")
        print("-"*70)
        print("1. Submit New Transaction(s)")
        print("2. View My Transaction Summary & Report")
        print("3. Multiply My Transactions (Homomorphic)")
        print("4. View All Sellers Summary (Admin View)")
        print("5. Switch Seller / Exit")
        print("-"*70)
        
        choice = input("Enter your choice (1-5): ").strip()
        
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
            multiply_seller_transactions()
        
        elif choice == "4":
            print("\n--- All Sellers Summary ---")
            verify_and_print_summary()
        
        elif choice == "5":
            print("\n[✓] Logging out... Goodbye!")
            break
        
        else:
            print("[!] Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    interactive_mode()
