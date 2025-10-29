# server.py
import socket, threading, json, time, os
import config
from crypto_modular import TransactionCrypto, SignatureEngine, int_to_hex, hex_to_int, bytes_to_hex

HOST = config.SERVER_HOST
PORT = config.SERVER_PORT

# Create keys for the gateway using modular crypto
transaction_crypto = TransactionCrypto(config.TRANSACTION_ENCRYPTION)
signature_engine = SignatureEngine(config.SIGNATURE_ALGORITHM, config.SIGNATURE_HASH)

# Persistent storage
STORAGE_FILE = "transactions_storage.json"
storage_lock = threading.Lock()

def _load_storage():
    """Load storage from JSON file"""
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, 'r') as f:
                data = json.load(f)
                return data.get("sellers", {}), data.get("summary_signed", None)
        except:
            return {}, None
    return {}, None

def _save_storage():
    """Save storage to JSON file"""
    try:
        with open(STORAGE_FILE, 'w') as f:
            json.dump({
                "sellers": sellers,
                "summary_signed": summary_signed
            }, f, indent=2)
    except Exception as e:
        print(f"[!] Storage save error: {e}")

# Load existing data
sellers, summary_signed = _load_storage()

def handle_client(conn, addr):
    try:
        raw = conn.recv(64_000).decode()
        req = json.loads(raw)
        typ = req.get("type")
        
        if typ == "get_config":
            # Return system configuration
            resp = {
                "transaction_encryption": config.TRANSACTION_ENCRYPTION,
                "signature_algorithm": config.SIGNATURE_ALGORITHM,
                "signature_hash": config.SIGNATURE_HASH
            }
            conn.send(json.dumps(resp).encode())
        
        elif typ == "get_pubkeys":
            # Return public keys
            tx_params = transaction_crypto.get_public_params()
            sig_pubkey = signature_engine.get_public_key()
            resp = {
                "transaction": tx_params,
                "signature": sig_pubkey
            }
            conn.send(json.dumps(resp).encode())

        elif typ == "submit_tx":
            seller = req["seller"]
            tx_hex = req["tx"]  # ciphertext hex
            with storage_lock:
                sellers.setdefault(seller, []).append(tx_hex)
                _save_storage()
            conn.send(json.dumps({"status": "ok"}).encode())
        
        elif typ == "multiply_tx":
            # Multiply seller's total by scalar
            seller = req["seller"]
            scalar = req["scalar"]
            
            with storage_lock:
                if seller not in sellers or not sellers[seller]:
                    conn.send(json.dumps({"status": "error", "msg": "No transactions found"}).encode())
                    return
                
                # Compute current total
                txlist = sellers[seller]
                individual = [hex_to_int(x) for x in txlist]
                total_enc = individual[0]
                for c in individual[1:]:
                    total_enc = transaction_crypto.homomorphic_add(total_enc, c)
                
                # Multiply by scalar
                result_enc = transaction_crypto.homomorphic_multiply(total_enc, scalar)
                result_dec = transaction_crypto.decrypt(result_enc)
                
                conn.send(json.dumps({
                    "status": "ok",
                    "result_encrypted_hex": int_to_hex(result_enc),
                    "result_decrypted": result_dec,
                    "scalar": scalar
                }).encode())

        elif typ == "get_signed_summary":
            # Build summary with decrypted totals and sign it
            with storage_lock:
                summary = {}
                crypto_config = {
                    "transaction_encryption": config.TRANSACTION_ENCRYPTION,
                    "signature_algorithm": config.SIGNATURE_ALGORITHM,
                    "signature_hash": config.SIGNATURE_HASH
                }
                
                for s, txlist in sellers.items():
                    individual = [hex_to_int(x) for x in txlist]
                    decrypted_individual = [transaction_crypto.decrypt(c) for c in individual]
                    
                    # Compute total encrypted by adding ciphertexts
                    total_enc = individual[0] if individual else 0
                    for c in individual[1:]:
                        total_enc = transaction_crypto.homomorphic_add(total_enc, c)
                    
                    total_dec = transaction_crypto.decrypt(total_enc) if individual else 0
                    
                    summary[s] = {
                        "individual_cipher_hex": txlist,
                        "individual_decrypted": decrypted_individual,
                        "total_cipher_hex": int_to_hex(total_enc) if individual else "0",
                        "total_decrypted": total_dec
                    }
                
                # Serialize summary and sign
                summary_bytes = json.dumps({"summary": summary, "config": crypto_config}, sort_keys=True).encode()
                signature = signature_engine.sign(summary_bytes)
                sig_pubkey = signature_engine.get_public_key()
                
                summary_signed_local = {
                    "summary": summary,
                    "crypto_config": crypto_config,
                    "signature": signature,
                    "signature_pubkey": sig_pubkey
                }
                
                # cache
                global summary_signed
                summary_signed = summary_signed_local
                _save_storage()
            conn.send(json.dumps(summary_signed_local).encode())

        else:
            conn.send(json.dumps({"error": "unknown request"}).encode())
    except Exception as e:
        conn.send(json.dumps({"error": str(e)}).encode())
    finally:
        conn.close()

def main():
    print("\n" + "="*70)
    print("🏦 MODULAR PAYMENT GATEWAY - SERVER")
    print("="*70)
    print("\n📋 Active Cryptographic Configuration:")
    print(f"  • Transaction Encryption: {config.TRANSACTION_ENCRYPTION}")
    print(f"  • Signature Algorithm: {config.SIGNATURE_ALGORITHM}")
    print(f"  • Signature Hash: {config.SIGNATURE_HASH}")
    print(f"\n[*] Server listening on {HOST}:{PORT}")
    print("="*70 + "\n")
    
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(10)
    while True:
        c, a = s.accept()
        threading.Thread(target=handle_client, args=(c, a), daemon=True).start()

if __name__ == "__main__":
    main()
