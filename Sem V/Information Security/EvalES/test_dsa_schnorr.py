import random
from hashlib import sha256

def is_prime(n, k=20):
    if n < 2:
        return False
    s, d = 0, n-1
    while d % 2 == 0:
        d >>= 1
        s += 1
    for _ in range(k):
        a = random.randrange(2, n-1)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(s-1):
            x = (x * x) % n
            if x == n-1:
                break
        else:
            return False
    return True

def gen_prime(bits=256):
    while True:
        p = random.getrandbits(bits)
        p |= (1 << bits-1) | 1
        if is_prime(p):
            return p

def gen_prime_order_subgroup(p):
    while True:
        q = gen_prime(bits=256)
        if (p-1) % q == 0:
            return q

def inv_mod(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError("No inverse")
    return x % m

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)

def hash_bytes(*args):
    h = sha256()
    for a in args:
        if isinstance(a, int):
            h.update(a.to_bytes((a.bit_length() + 7) // 8, 'big'))
        else:
            h.update(a)
    return int.from_bytes(h.digest(), 'big')

def gen_elgamal_params():
    p = gen_prime(512)
    g = 2
    return p, g

def elgamal_keygen(p, g):
    x = random.randrange(2, p-2)
    y = pow(g, x, p)
    return x, y

def elgamal_sign(m, p, g, x):
    k = random.randrange(2, p-2)
    while extended_gcd(k, p-1)[0] != 1:
        k = random.randrange(2, p-2)
    r = pow(g, k, p)
    k_inv = inv_mod(k, p-1)
    h = hash_bytes(m)
    s = (k_inv * (h - x * r)) % (p-1)
    return (r, s)

def elgamal_verify(m, sig, p, g, y):
    r, s = sig
    if not (0 < r < p):
        return False
    h = hash_bytes(m)
    v1 = (pow(y, r, p) * pow(r, s, p)) % p
    v2 = pow(g, h, p)
    return v1 == v2

def gen_schnorr_params():
    while True:
        q = gen_prime(256)
        p = 2 * q + 1
        if is_prime(p):
            break
    g = 2
    while pow(g, q, p) == 1:
        g += 1
    return p, q, g

def schnorr_keygen(p, q, g):
    x = random.randrange(1, q)
    y = pow(g, x, p)
    return x, y

def schnorr_sign(m, p, q, g, x):
    k = random.randrange(1, q)
    r = pow(g, k, p)
    e = hash_bytes(r.to_bytes((r.bit_length()+7)//8, 'big'), m) % q
    s = (k + x*e) % q
    return (e, s)

def schnorr_verify(m, sig, p, q, g, y):
    e, s = sig
    r = (pow(g, s, p) * inv_mod(pow(y, e, p), p)) % p
    e2 = hash_bytes(r.to_bytes((r.bit_length()+7)//8, 'big'), m) % q
    return e == e2

m = b"message"

p_elgamal, g_elgamal = gen_elgamal_params()
x_elgamal, y_elgamal = elgamal_keygen(p_elgamal, g_elgamal)
sig_elgamal = elgamal_sign(m, p_elgamal, g_elgamal, x_elgamal)
ver_elgamal = elgamal_verify(m, sig_elgamal, p_elgamal, g_elgamal, y_elgamal)

p_schnorr, q_schnorr, g_schnorr = gen_schnorr_params()
x_schnorr, y_schnorr = schnorr_keygen(p_schnorr, q_schnorr, g_schnorr)
sig_schnorr = schnorr_sign(m, p_schnorr, q_schnorr, g_schnorr, x_schnorr)
ver_schnorr = schnorr_verify(m, sig_schnorr, p_schnorr, q_schnorr, g_schnorr, y_schnorr)

print(f"message: {m.decode()}")
print(f"elgamal signature: {sig_elgamal}")
print(f"Schnorr signature: {sig_schnorr}")
print(f"verified (EG): {'verified' if ver_elgamal else 'Not Verified'}")
print(f"verified (Schorr): {'verified' if ver_schnorr else 'Not Verified'}")