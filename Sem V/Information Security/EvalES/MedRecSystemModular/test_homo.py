"""
Quick test to verify RSA homomorphic encryption is working correctly
"""
import socket, json
from crypto_utils import *

SERVER = ("localhost", 9999)

# Generate keys
exp_priv, exp_pub, N_exp, e_exp = generate_rsa_homomorphic()

def send_request(payload):
    s = socket.socket()
    s.connect(SERVER)
    s.send(json.dumps(payload).encode())
    resp = s.recv(65536).decode()
    s.close()
    try:
        return json.loads(resp)
    except:
        return {"status": "error", "msg": resp}

print("\n" + "="*60)
print("Testing RSA Homomorphic Encryption")
print("="*60)

# Test encryption/decryption
print("\n1. Testing individual encryption/decryption:")
test_values = [100, 50, 25]
for val in test_values:
    enc = rsa_homo_encrypt(val, N_exp, e_exp)
    dec = rsa_homo_decrypt(enc, exp_priv)
    print(f"  Value: {val}, Encrypted: {str(enc)[:40]}..., Decrypted: {dec}")
    assert dec == val, f"Decryption failed! Expected {val}, got {dec}"

print("  ✓ All individual tests passed!")

# Test homomorphic addition
print("\n2. Testing homomorphic addition (multiplication of ciphertexts):")
enc1 = rsa_homo_encrypt(100, N_exp, e_exp)
enc2 = rsa_homo_encrypt(50, N_exp, e_exp)
enc_sum = rsa_homo_add(enc1, enc2, N_exp)
dec_sum = rsa_homo_decrypt(enc_sum, exp_priv)
print(f"  100 + 50 = {dec_sum}")
assert dec_sum == 150, f"Addition failed! Expected 150, got {dec_sum}"
print("  ✓ Homomorphic addition works!")

# Test with server
print("\n3. Testing with server (Doctor 3: 100 + 10 = 110):")

# Clear old data first (optional - comment out if you want to keep old data)
import os
if os.path.exists("storage.json"):
    print("  (Old database exists - server will use it)")

# Add expenses for doctor TEST_DOC
test_doc = "TEST_DOC"
expenses = [100, 10]

for exp in expenses:
    enc = rsa_homo_encrypt(exp, N_exp, e_exp)
    payload = {
        "action": "add_expense",
        "id": test_doc,
        "amount": enc,
        "n": N_exp
    }
    resp = send_request(payload)
    print(f"  Added expense {exp}: {resp.get('status')}")

# Query back
payload = {"action": "sum_doctor_expenses", "doctor_id": test_doc, "n": N_exp}
resp = send_request(payload)

if resp.get("status") == "ok":
    enc_sum = resp.get("encrypted_sum")
    if enc_sum:
        dec_sum = rsa_homo_decrypt(enc_sum, exp_priv)
        print(f"  Server returned encrypted sum")
        print(f"  Decrypted: {dec_sum}")
        print(f"  Expected: {sum(expenses)}")
        if dec_sum == sum(expenses):
            print("  ✓ Server homomorphic encryption works correctly!")
        else:
            print(f"  ✗ Error: Expected {sum(expenses)}, got {dec_sum}")
    else:
        print("  ✗ No encrypted sum returned")
else:
    print(f"  ✗ Server error: {resp.get('msg')}")

print("\n" + "="*60)
print("Test Complete!")
print("="*60)
