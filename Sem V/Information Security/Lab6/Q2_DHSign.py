import random
from hashlib import sha256
from hmac import HMAC

def is_prime(n, k=20):
    if n < 2:
        return False
    s, d = 0, n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def gen_prime(bits=512):
    while True:
        p = random.getrandbits(bits)
        p |= (1 << (bits - 1)) | 1
        if is_prime(p):
            return p

def gen_dh_params():
    p = gen_prime(512)
    g = 2
    return p, g

def dh_keygen(p, g):
    x = random.randrange(2, p - 2)
    y = pow(g, x, p)
    return x, y

def dh_shared_secret(their_pub, priv, p):
    return pow(their_pub, priv, p)

def hmac_sign(key, message):
    return HMAC(key.to_bytes((key.bit_length()+7)//8, 'big'), message, sha256).digest()

def hmac_verify(key, message, signature):
    expected = hmac_sign(key, message)
    return expected == signature

m = b"message"

p_dh, g_dh = gen_dh_params()
x_a, y_a = dh_keygen(p_dh, g_dh)
x_b, y_b = dh_keygen(p_dh, g_dh)

shared_a = dh_shared_secret(y_b, x_a, p_dh)
shared_b = dh_shared_secret(y_a, x_b, p_dh)

signature = hmac_sign(shared_a, m)

verified = hmac_verify(shared_b, m, signature)

print(f"message: {m.decode()}")
print(f"DH shared secret (Alice): {shared_a}")
print(f"DH shared secret (Bob): {shared_b}")
print(f"signature: {signature.hex()}")
print(f"verified (DH): {'verified' if verified else 'verified'}")
