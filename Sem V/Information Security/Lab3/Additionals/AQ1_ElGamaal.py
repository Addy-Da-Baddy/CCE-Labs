from Crypto.Util.number import inverse
from Crypto.Random import random

p = 7919
g = 2
h = 6465
x = 2999  # private key

message = "Asymmetric Algorithms"

def elgamal_encrypt_char(m, public_key):
    p, g, h = public_key
    k = random.randint(2, p-2)
    c1 = pow(g, k, p)
    c2 = (m * pow(h, k, p)) % p
    return c1, c2

def elgamal_decrypt_char(c1, c2, private_key, p):
    s = pow(c1, private_key, p)
    s_inv = inverse(s, p)
    m = (c2 * s_inv) % p
    return m

public_key = (p, g, h)

ciphertext = []
for ch in message:
    m = ord(ch)
    c1, c2 = elgamal_encrypt_char(m, public_key)
    ciphertext.append((c1, c2))

decrypted_chars = []
for c1, c2 in ciphertext:
    m = elgamal_decrypt_char(c1, c2, x, p)
    decrypted_chars.append(chr(m))

decrypted_message = ''.join(decrypted_chars)

print("Original message:", message)
print("Decrypted message:", decrypted_message)
print("Successful" if decrypted_message == message else "Unsuccessful")
