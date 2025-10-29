"""Debug Schnorr signature"""
import hashlib
import random
from Crypto.Util.number import inverse, getPrime

# Generate proper Schnorr parameters
q = getPrime(160)  # 160-bit prime
# For Schnorr, we need p where q divides (p-1)
# Simplest: p = 2q + 1 (safe prime)
p = 2 * q + 1
while not all(pow(p, 1, i) == 0 for i in [2, 3, 5, 7] if p % i != 0):
    q = getPrime(160)
    p = 2 * q + 1

# Find generator g of order q in Z_p*
# For p = 2q + 1, any h^2 mod p (where h != 1, p-1) has order q
h = 2
while pow(h, q, p) != 1 or h == 1 or h == p-1:
    h += 1
    if h >= p:
        h = 2
g = h

print(f"p = {p}")
print(f"q = {q}")
print(f"g = {g}")
print(f"Checking: g^q mod p = {pow(g, q, p)} (should be 1)")
print(f"Checking: g^2 mod p = {pow(g, 2, p)} (should NOT be 1)")

# Key generation
x = random.randrange(1, q)
y = pow(g, x, p)

print(f"p = {p}")
print(f"q = {q}")
print(f"g = {g}")
print(f"x (private) = {x}")
print(f"y (public) = {y}")

# Message
message = b"Test message"

# Sign
k = random.randrange(1, q)
r = pow(g, k, p)

r_bytes = r.to_bytes((r.bit_length() + 7) // 8, 'big')
e = int.from_bytes(hashlib.sha256(r_bytes + message).digest(), 'big') % q

s = (k + x * e) % q

print(f"\nSignature:")
print(f"k = {k}")
print(f"r = {r}")
print(f"e = {e}")
print(f"s = {s}")

# Verify
r_prime = (pow(g, s, p) * inverse(pow(y, e, p), p)) % p

r_prime_bytes = r_prime.to_bytes((r_prime.bit_length() + 7) // 8, 'big')
e_prime = int.from_bytes(hashlib.sha256(r_prime_bytes + message).digest(), 'big') % q

print(f"\nVerification:")
print(f"r' = {r_prime}")
print(f"e' = {e_prime}")
print(f"r == r': {r == r_prime}")
print(f"e == e': {e == e_prime}")
print(f"Valid: {e == e_prime}")
