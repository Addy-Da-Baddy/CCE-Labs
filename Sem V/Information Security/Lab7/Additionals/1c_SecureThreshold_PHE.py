from Crypto.Util import number
import random

def lcm(x, y): 
    from math import gcd
    return x*y//gcd(x, y)

def generate_paillier(bits=512):
    p = number.getPrime(bits)
    q = number.getPrime(bits)
    n = p*q
    g = n+1
    lam = lcm(p-1, q-1)
    mu = pow(lam, -1, n)
    return (n, g), (lam, mu)

def encrypt(pub, m):
    n, g = pub
    r = random.randint(1, n-1)
    while number.GCD(r, n) != 1:
        r = random.randint(1, n-1)
    return (pow(g, m, n*n) * pow(r, n, n*n)) % (n*n)

def decrypt(priv, pub, c):
    lam, mu = priv
    n, g = pub
    x = pow(c, lam, n*n)
    L = (x-1)//n
    return (L * mu) % n

pub, priv = generate_paillier()
party_data = [5, 12, 7, 20]
encrypted_data = [encrypt(pub, x) for x in party_data]

threshold = 3
combined = 1
for val in encrypted_data[:threshold]:
    combined = (combined*val) % (pub[0]**2)

decrypted_result = decrypt(priv, pub, combined)
print(f"Decrypted result using {threshold} parties:", decrypted_result)
