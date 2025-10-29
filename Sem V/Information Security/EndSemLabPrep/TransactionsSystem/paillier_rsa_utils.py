# paillier_rsa_utils.py
import json
from Crypto.Util.number import getPrime, inverse, GCD, bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import random

# ---------------- Paillier ----------------
class PaillierKeypair:
    def __init__(self, bits=512):
        # generate p, q
        self.p = getPrime(bits//2)
        self.q = getPrime(bits//2)
        self.n = self.p * self.q
        self.nsq = self.n * self.n
        self.g = self.n + 1  # common choice
        # lambda = lcm(p-1, q-1)
        self.l = (self.p - 1) * (self.q - 1) // GCD(self.p - 1, self.q - 1)
        # mu = (L(g^lambda mod n^2))^{-1} mod n
        u = pow(self.g, self.l, self.nsq)
        L = (u - 1) // self.n
        self.mu = inverse(L, self.n)

    def public(self):
        return {"n": self.n, "g": self.g}

    def encrypt(self, m: int):
        """Standard Paillier encryption with random r"""
        if m < 0:
            raise ValueError("Negative plaintexts not supported in this simple demo")
        r = random.randrange(1, self.n)
        while GCD(r, self.n) != 1:
            r = random.randrange(1, self.n)
        c = (pow(self.g, m, self.nsq) * pow(r, self.n, self.nsq)) % self.nsq
        return c

    def decrypt(self, c: int):
        u = pow(c, self.l, self.nsq)
        L = (u - 1) // self.n
        m = (L * self.mu) % self.n
        return m

    @staticmethod
    def homomorphic_add(c1: int, c2: int, n):
        """Multiplicative combination gives encryption of sum mod n"""
        nsq = n * n
        return (c1 * c2) % nsq

# ---------------- RSA Sign/Verify ----------------
def generate_rsa(bits=2048):
    key = RSA.generate(bits)
    priv = key.export_key()
    pub = key.publickey().export_key()
    return priv, pub

def rsa_sign(priv_pem: bytes, message_bytes: bytes):
    key = RSA.import_key(priv_pem)
    h = SHA256.new(message_bytes)
    signer = pkcs1_15.new(key)
    sig = signer.sign(h)
    return sig

def rsa_verify(pub_pem: bytes, message_bytes: bytes, signature: bytes):
    key = RSA.import_key(pub_pem)
    h = SHA256.new(message_bytes)
    verifier = pkcs1_15.new(key)
    try:
        verifier.verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

# ---------------- JSON-friendly helpers ----------------
def int_to_hex(i: int) -> str:
    return hex(i)[2:]

def hex_to_int(h: str) -> int:
    return int(h, 16)

def bytes_to_hex(b: bytes) -> str:
    return b.hex()

def hex_to_bytes(h: str) -> bytes:
    return bytes.fromhex(h)
