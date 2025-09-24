from Crypto.Util import number

def generate_rsa_keypair(bits=512):
    p = number.getPrime(bits)
    q = number.getPrime(bits)
    n = p * q
    phi = (p-1)*(q-1)
    e = 65537
    d = pow(e, -1, phi)
    return (n, e), (n, d)

def encrypt(pub, m):
    n, e = pub
    return pow(m, e, n)

def decrypt(priv, c):
    n, d = priv
    return pow(c, d, n)

pub, priv = generate_rsa_keypair()
m1 = 7
m2 = 3
c1 = encrypt(pub, m1)
c2 = encrypt(pub, m2)
print("Ciphertext 1:", c1)
print("Ciphertext 2:", c2)
c_mult = (c1 * c2) % pub[0]
print("Encrypted product:", c_mult)
decrypted_product = decrypt(priv, c_mult)
print("Decrypted product:", decrypted_product)
