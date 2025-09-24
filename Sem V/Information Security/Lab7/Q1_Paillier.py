from Crypto.Util import number
import random

def lcm(x, y):
    from math import gcd
    return x * y // gcd(x, y)

def generate_keypair(bits=512):
    p = number.getPrime(bits)
    q = number.getPrime(bits)
    n = p * q
    g = n + 1
    lam = lcm(p-1, q-1)
    mu = pow(lam, -1, n)
    return (n, g), (lam, mu)

def encrypt(pub, m):
    n, g = pub
    r = random.randrange(1, n)
    while number.GCD(r, n) != 1:
        r = random.randrange(1, n)
    c = (pow(g, m, n*n) * pow(r, n, n*n)) % (n*n)
    return c

def decrypt(priv, pub, c):
    lam, mu = priv
    n, g = pub
    x = pow(c, lam, n*n)
    L = (x-1)//n
    m = (L * mu) % n
    return m

pub, priv = generate_keypair()
m1 = 15
m2 = 25
c1 = encrypt(pub, m1)
c2 = encrypt(pub, m2)
print("Ciphertext 1:", c1)
print("Ciphertext 2:", c2)
c_sum = (c1 * c2) % (pub[0]**2)
print("Encrypted sum:", c_sum)
decrypted_sum = decrypt(priv, pub, c_sum)
print("Decrypted sum:", decrypted_sum)
