import time
from Crypto.Util import number
import random

def lcm(x, y): 
    from math import gcd
    return x*y//gcd(x, y)

def paillier_setup(bits=512):
    p = number.getPrime(bits)
    q = number.getPrime(bits)
    n = p*q
    g = n+1
    lam = lcm(p-1, q-1)
    mu = pow(lam, -1, n)
    return (n, g), (lam, mu)

def paillier_encrypt(pub, m):
    n, g = pub
    r = random.randint(1, n-1)
    while number.GCD(r, n) != 1:
        r = random.randint(1, n-1)
    return (pow(g, m, n*n) * pow(r, n, n*n)) % (n*n)

def paillier_decrypt(priv, pub, c):
    lam, mu = priv
    n, g = pub
    x = pow(c, lam, n*n)
    L = (x-1)//n
    return (L * mu) % n

def elgamal_setup(bits=256):
    p = number.getPrime(bits)
    g = 2
    x = random.randint(1, p-2)
    h = pow(g, x, p)
    return (p, g, h), x

def elgamal_encrypt(pub, m):
    p, g, h = pub
    y = random.randint(1, p-2)
    c1 = pow(g, y, p)
    c2 = (m * pow(h, y, p)) % p
    return (c1, c2)

def elgamal_decrypt(priv, pub, c):
    p, g, h = pub
    x = priv
    c1, c2 = c
    s = pow(c1, x, p)
    s_inv = pow(s, -1, p)
    return (c2 * s_inv) % p

pa_pub, pa_priv = paillier_setup()
el_pub, el_priv = elgamal_setup()

m1 = 15
m2 = 25

start = time.time()
c1 = paillier_encrypt(pa_pub, m1)
c2 = paillier_encrypt(pa_pub, m2)
c_sum = (c1*c2) % (pa_pub[0]**2)
decrypted_sum = paillier_decrypt(pa_priv, pa_pub, c_sum)
end = time.time()
print("Paillier homomorphic addition:", decrypted_sum, "Time:", end-start)

start = time.time()
c1 = elgamal_encrypt(el_pub, m1)
c2 = elgamal_encrypt(el_pub, m2)
c_mult = (c1[0]*c2[0] % el_pub[0], c1[1]*c2[1] % el_pub[0])
decrypted_mult = elgamal_decrypt(el_priv, el_pub, c_mult)
end = time.time()
print("ElGamal homomorphic multiplication:", decrypted_mult, "Time:", end-start)
