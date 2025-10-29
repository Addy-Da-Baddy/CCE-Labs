"""
Debug script for Schnorr signature
"""

import hashlib
from Crypto.Random import get_random_bytes
from Crypto.Util.number import getPrime
import config

# Schnorr setup
q = getPrime(160)
p = 2 * q + 1
while not all(p % i != 0 for i in range(2, min(int(p**0.5) + 1, 1000))):
    q = getPrime(160)
    p = 2 * q + 1

g = 2
x = int.from_bytes(get_random_bytes(20), 'big') % q
y = pow(g, x, p)

print(f"Schnorr Parameters:")
print(f"p = {p}")
print(f"q = {q}")
print(f"g = {g}")
print(f"x (private) = {x}")
print(f"y (public) = {y}")

# Test message
message = "This is a test"
hash_option = "SHA256"

# SIGNING
print(f"\n=== SIGNING ===")
k = int.from_bytes(get_random_bytes(20), 'big') % q
r = pow(g, k, p)
print(f"k (random) = {k}")
print(f"r = g^k mod p = {r}")

if hash_option == "SHA256":
    msg_hash = hashlib.sha256(message.encode()).digest()
    challenge_input = str(r).encode() + msg_hash
else:
    challenge_input = str(r).encode() + message.encode()

print(f"Challenge input: {challenge_input[:50]}...")
e = int.from_bytes(hashlib.sha256(challenge_input).digest(), 'big') % q
s = (k - x * e) % q

print(f"e (challenge) = {e}")
print(f"s = k - x*e mod q = {s}")

signature = {"r": r, "s": s, "e": e}

# VERIFICATION
print(f"\n=== VERIFICATION ===")
r_sig = signature["r"]
s_sig = signature["s"]
e_sig = signature["e"]

print(f"r from signature = {r_sig}")
print(f"s from signature = {s_sig}")
print(f"e from signature = {e_sig}")

# Recompute challenge
if hash_option == "SHA256":
    msg_hash_v = hashlib.sha256(message.encode()).digest()
    challenge_input_v = str(r_sig).encode() + msg_hash_v
else:
    challenge_input_v = str(r_sig).encode() + message.encode()

ev = int.from_bytes(hashlib.sha256(challenge_input_v).digest(), 'big') % q
print(f"ev (recomputed challenge) = {ev}")
print(f"Challenge match: {e_sig == ev}")

# Check if (s + x*e) mod q == k mod q
reconstructed_k = (s_sig + x * ev) % q
original_k_mod_q = k % q
print(f"\nMath check:")
print(f"Original k mod q = {original_k_mod_q}")
print(f"Reconstructed (s + x*e) mod q = {reconstructed_k}")
print(f"Match: {reconstructed_k == original_k_mod_q}")

# Verify equation: g^s * y^ev == r (mod p)
rv = (pow(g, s_sig, p) * pow(y, ev, p)) % p
print(f"\nrv = g^s * y^ev mod p = {rv}")
print(f"r from signature = {r_sig}")
print(f"Commitment match (using ev): {rv == r_sig}")

# Final verification
valid = (e_sig == ev) and (rv == r_sig)
print(f"\nSignature valid: {valid}")
