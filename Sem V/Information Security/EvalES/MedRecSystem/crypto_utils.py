import json
import base64
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.number import getPrime, inverse, GCD, bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA
import time

# ---------------------- AES - Authenticated Encryption ----------------------
def aes_encrypt(data: bytes, key: bytes):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }

def aes_decrypt(payload: dict, key: bytes):
    cipher = AES.new(key, AES.MODE_GCM,
                     nonce=base64.b64decode(payload["nonce"]))
    return cipher.decrypt_and_verify(
        base64.b64decode(payload["ciphertext"]),
        base64.b64decode(payload["tag"])
    )

# ---------------------- RSA ----------------------
def generate_rsa_keys(bits=2048):
    key = RSA.generate(bits)
    return key.export_key(), key.publickey().export_key()

def rsa_encrypt(data: bytes, pubkey: bytes):
    key = RSA.import_key(pubkey)
    cipher = PKCS1_OAEP.new(key)
    return base64.b64encode(cipher.encrypt(data)).decode()

def rsa_decrypt(ciphertext: str, privkey: bytes):
    key = RSA.import_key(privkey)
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(base64.b64decode(ciphertext))

# ---------------------- ElGamal Signatures ----------------------
class ElGamal:
    def __init__(self, bits=256):
        self.p = getPrime(bits)
        self.g = 2
        self.x = getPrime(bits - 2)
        self.y = pow(self.g, self.x, self.p)

    def sign(self, message: str):
        m = bytes_to_long(message.encode())
        while True:
            k = getPrime(128)
            if GCD(k, self.p - 1) == 1:
                break
        r = pow(self.g, k, self.p)
        s = ((m - self.x * r) * inverse(k, self.p - 1)) % (self.p - 1)
        return {"r": r, "s": s, "ts": int(time.time())}

    def verify(self, message: str, sig: dict):
        m = bytes_to_long(message.encode())
        r, s = sig["r"], sig["s"]
        if not (0 < r < self.p):
            return False
        left = (pow(self.y, r, self.p) * pow(r, s, self.p)) % self.p
        right = pow(self.g, m, self.p)
        return left == right

# ---------------------- Paillier (Deterministic for Exact Match) ----------------------
class Paillier:
    def __init__(self, bits=256):
        self.p = getPrime(bits)
        self.q = getPrime(bits)
        self.n = self.p * self.q
        self.g = self.n + 1
        self.l = (self.p - 1) * (self.q - 1)
        self.mu = inverse(self.l, self.n)

    def encrypt(self, m: int):  # deterministic (no randomness)
        return pow(self.g, m, self.n * self.n)

    def decrypt(self, c: int):
        u = pow(c, self.l, self.n * self.n)
        return ((u - 1) // self.n) * self.mu % self.n

# ---------------------- Homomorphic RSA expense trick ----------------------
def generate_rsa_homomorphic():
    """Generate keys for homomorphic encryption using smaller modulus for discrete log"""
    # Use smaller key size for practical discrete log computation
    key = RSA.generate(1024)  # Smaller for demo
    priv = key.export_key()
    pub = key.publickey().export_key()
    return priv, pub, key.n, key.e

def rsa_homo_encrypt(amount, n, e):
    """
    Encode amount as base^amount for additive homomorphism
    base^a * base^b = base^(a+b)
    """
    base = 3  # Use 3 as base (small prime)
    return pow(base, amount, n)

def rsa_homo_add(enc1, enc2, n):
    """Multiply ciphertexts to add the underlying amounts"""
    return (enc1 * enc2) % n

def rsa_homo_decrypt(cipher, privkey):
    """
    Decrypt by computing discrete log
    For practical demo with reasonable expense amounts (0-10000)
    """
    key = RSA.import_key(privkey)
    n = key.n
    base = 3
    
    # Baby-step giant-step or simple iteration for small values
    # For demo: iterate up to reasonable expense amount
    max_expense = 50000  # Maximum sum we expect
    step_size = 100  # Check every 100 to speed up
    
    # First, narrow down the range using giant steps
    current = 1
    for i in range(0, max_expense, step_size):
        val = pow(base, i, n)
        if val == cipher:
            return i
        current = val
    
    # If not found in giant steps, do detailed search in last range
    # More efficient: use baby-step giant-step properly
    cache = {}
    m = 1000  # Baby step size
    
    # Baby steps: compute base^j for j = 0 to m-1
    baby = 1
    for j in range(m):
        if baby == cipher:
            return j
        cache[baby] = j
        baby = (baby * base) % n
    
    # Giant steps: compute cipher * (base^(-m))^i
    base_inv = pow(base, -m, n)
    gamma = cipher
    for i in range(1, max_expense // m + 1):
        gamma = (gamma * base_inv) % n
        if gamma in cache:
            return i * m + cache[gamma]
    
    return -1  # Not found
