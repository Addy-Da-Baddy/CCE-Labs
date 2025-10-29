"""
Detailed Schnorr debug with inline code
"""

import hashlib
from Crypto.Random import get_random_bytes
from Crypto.Util.number import getPrime

# Setup
q = getPrime(160)
p = 2 * q + 1
while not all(p % i != 0 for i in range(2, min(int(p**0.5) + 1, 1000))):
    q = getPrime(160)
    p = 2 * q + 1

g = 2
x = int.from_bytes(get_random_bytes(20), 'big') % q
y = pow(g, x, p)

print("Parameters:")
print(f"p={p}")
print(f"q={q}")
print(f"x={x}")
print(f"y={y}")

message = "Test message"
hash_option = "SHA256"

# SIGN
print("\n=== SIGNING ===")
k = int.from_bytes(get_random_bytes(20), 'big') % q
r = pow(g, k, p)

if hash_option == "SHA256":
    msg_hash = hashlib.sha256(message.encode()).digest()
    challenge_input = str(r).encode() + msg_hash
else:
    challenge_input = str(r).encode() + message.encode()

e = int.from_bytes(hashlib.sha256(challenge_input).digest(), 'big') % q
s = (k - x * e) % q

print(f"k={k}")
print(f"r={r}")
print(f"e={e}")
print(f"s={s}")

# VERIFY
print("\n=== VERIFICATION ===")
if hash_option == "SHA256":
    msg_hash_v = hashlib.sha256(message.encode()).digest()
    challenge_input_v = str(r).encode() + msg_hash_v
else:
    challenge_input_v = str(r).encode() + message.encode()

ev = int.from_bytes(hashlib.sha256(challenge_input_v).digest(), 'big') % q

print(f"ev={ev}")
print(f"e==ev: {e == ev}")

# Check math
k_reconstructed = (s + x * ev) % q
print(f"\nMath check:")
print(f"k original = {k}")
print(f"k reconstructed = (s + x*ev) % q = {k_reconstructed}")
print(f"k match: {k == k_reconstructed}")

# Try direct computation
r_check = pow(g, k_reconstructed, p)
print(f"r original = {r}")
print(f"r from k_reconstructed = g^k_reconstructed % p = {r_check}")
print(f"r match: {r == r_check}")

# Try the verification equation
rv = (pow(g, s, p) * pow(y, ev, p)) % p
print(f"\nrv = g^s * y^ev % p = {rv}")
print(f"r==rv: {r == rv}")

# Manual check
gs = pow(g, s, p)
ye = pow(y, ev, p)
print(f"\nManual:")
print(f"g^s % p = {gs}")
print(f"y^ev % p = {ye}")
print(f"(g^s * y^ev) % p = {(gs * ye) % p}")

valid = (e == ev) and (r == rv)
print(f"\nValid: {valid}")
