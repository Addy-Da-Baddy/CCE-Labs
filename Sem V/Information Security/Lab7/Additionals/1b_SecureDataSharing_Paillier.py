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
party1 = 10
party2 = 15

c1 = encrypt(pub, party1)
c2 = encrypt(pub, party2)
print("Encrypted Party1:", c1)
print("Encrypted Party2:", c2)

c_sum = (c1*c2) % (pub[0]**2)
decrypted_sum = decrypt(priv, pub, c_sum)
print("Decrypted combined sum:", decrypted_sum)
