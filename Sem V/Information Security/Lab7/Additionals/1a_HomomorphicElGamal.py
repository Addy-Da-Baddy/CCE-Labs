from Crypto.Util import number
import random

def generate_elgamal_key(bits=256):
    p = number.getPrime(bits)
    g = 2
    x = random.randint(1, p-2)
    h = pow(g, x, p)
    return (p, g, h), x

def encrypt(pub, m):
    p, g, h = pub
    y = random.randint(1, p-2)
    c1 = pow(g, y, p)
    c2 = (m * pow(h, y, p)) % p
    return (c1, c2)

def decrypt(priv, pub, c):
    p, g, h = pub
    x = priv
    c1, c2 = c
    s = pow(c1, x, p)
    s_inv = pow(s, -1, p)
    m = (c2 * s_inv) % p
    return m

pub, priv = generate_elgamal_key()
m1 = 7
m2 = 3
c1 = encrypt(pub, m1)
c2 = encrypt(pub, m2)
print("Ciphertext 1:", c1)
print("Ciphertext 2:", c2)

c_mult = (c1[0]*c2[0] % pub[0], c1[1]*c2[1] % pub[0])
print("Encrypted product:", c_mult)

decrypted_product = decrypt(priv, pub, c_mult)
print("Decrypted product:", decrypted_product)
