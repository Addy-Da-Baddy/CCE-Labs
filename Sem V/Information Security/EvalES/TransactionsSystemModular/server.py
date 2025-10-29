# server.py
import socket, threading, json, time
from paillier_rsa_utils import PaillierKeypair, generate_rsa, rsa_sign, int_to_hex, hex_to_int, bytes_to_hex
from paillier_rsa_utils import PaillierKeypair
from paillier_rsa_utils import int_to_hex as i2h
from paillier_rsa_utils import bytes_to_hex as b2h

HOST = "localhost"
PORT = 10000

# Create keys for the gateway
paillier = PaillierKeypair(bits=512)
rsa_priv, rsa_pub = generate_rsa(2048)

# In-memory storage for sellers' encrypted transactions (hex-encoded ints)
storage_lock = threading.Lock()
sellers = {}  # seller_name -> list of ciphertext hex strings (individual tx)
# We'll also store decrypted plaintexts for display after computing totals (server computes)
summary_signed = None  # cached signed summary after aggregation

def handle_client(conn, addr):
    try:
        raw = conn.recv(64_000).decode()
        req = json.loads(raw)
        typ = req.get("type")
        if typ == "get_pubkeys":
            # Return Paillier public key and server RSA public key
            resp = {
                "paillier": {"n": i2h(paillier.n), "g": i2h(paillier.g)},
                "rsa_pub": b2h(rsa_pub)
            }
            conn.send(json.dumps(resp).encode())

        elif typ == "submit_tx":
            seller = req["seller"]
            tx_hex = req["tx"]  # ciphertext hex
            with storage_lock:
                sellers.setdefault(seller, []).append(tx_hex)
            conn.send(json.dumps({"status": "ok"}).encode())

        elif typ == "get_signed_summary":
            # Build summary with decrypted totals and sign it
            with storage_lock:
                summary = {}
                for s, txlist in sellers.items():
                    individual = [hex_to_int(x) for x in txlist]
                    # decrypt each individual? The requirements ask to include decrypted transaction amounts.
                    # Paillier decrypts ciphertexts to amounts.
                    decrypted_individual = [paillier.decrypt(c) for c in individual]
                    # Compute total encrypted by multiplying ciphertexts
                    total_enc = 1
                    for c in individual:
                        total_enc = PaillierKeypair.homomorphic_add(total_enc, c, paillier.n)
                    total_dec = paillier.decrypt(total_enc)
                    summary[s] = {
                        "individual_cipher_hex": txlist,
                        "individual_decrypted": decrypted_individual,
                        "total_cipher_hex": i2h(total_enc),
                        "total_decrypted": total_dec
                    }
                # Serialize summary deterministically (sorted keys) and sign
                summary_bytes = json.dumps(summary, sort_keys=True).encode()
                signature = rsa_sign(rsa_priv, summary_bytes)
                summary_signed_local = {
                    "summary": summary,
                    "signature_hex": bytes_to_hex(signature),
                    "rsa_pub_hex": bytes_to_hex(rsa_pub)
                }
                # cache
                global summary_signed
                summary_signed = summary_signed_local
            conn.send(json.dumps(summary_signed_local).encode())

        else:
            conn.send(json.dumps({"error": "unknown request"}).encode())
    except Exception as e:
        conn.send(json.dumps({"error": str(e)}).encode())
    finally:
        conn.close()

def main():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(10)
    print(f"[Gateway] Listening on {HOST}:{PORT}")
    while True:
        c, a = s.accept()
        threading.Thread(target=handle_client, args=(c, a), daemon=True).start()

if __name__ == "__main__":
    main()
