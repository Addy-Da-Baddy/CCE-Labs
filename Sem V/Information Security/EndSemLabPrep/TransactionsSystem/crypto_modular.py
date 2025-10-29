"""
Modular Cryptographic Utilities for Transaction System
"""

import hashlib
import random
from Crypto.Util.number import getPrime, GCD, inverse, bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import config

# ============================================================
# TRANSACTION ENCRYPTION (Homomorphic)
# ============================================================

def lcm(x, y):
    """Compute least common multiple"""
    from math import gcd
    return x * y // gcd(x, y)

class TransactionCrypto:
    """Handles homomorphic encryption for transactions"""
    
    def __init__(self, mode: str = None):
        self.mode = mode or config.TRANSACTION_ENCRYPTION
        
        if self.mode == "Paillier":
            # Paillier key generation
            bits = config.PAILLIER_KEY_SIZE // 2
            self.p = getPrime(bits)
            self.q = getPrime(bits)
            self.n = self.p * self.q
            self.n_sq = self.n * self.n
            self.g = self.n + 1
            self.lam = lcm(self.p - 1, self.q - 1)
            self.mu = pow(self.lam, -1, self.n)
        
        elif self.mode == "RSA":
            # RSA with exponent trick for additive properties
            key = RSA.generate(1024)  # Smaller for practical discrete log
            self.priv = key.export_key()
            self.pub = key.publickey().export_key()
            self.n = key.n
            self.e = key.e
            self.d = key.d
            self.base = 3  # Base for encoding amounts
        
        elif self.mode == "DH":
            # Diffie-Hellman based encryption
            self.p = getPrime(config.DH_PRIME_SIZE)
            self.g = 2
            self.private_key = random.randrange(2, self.p - 1)
            self.public_key = pow(self.g, self.private_key, self.p)
        
        elif self.mode == "Rabin":
            # Rabin cryptosystem (n = p*q where p,q ≡ 3 mod 4)
            bits = config.RABIN_KEY_SIZE // 2
            # Find primes ≡ 3 mod 4
            self.p = getPrime(bits)
            while self.p % 4 != 3:
                self.p = getPrime(bits)
            self.q = getPrime(bits)
            while self.q % 4 != 3:
                self.q = getPrime(bits)
            self.n = self.p * self.q
        
        elif self.mode == "ECC":
            # ECC - using simple discrete log on curve points
            # For demo: using multiplicative group (not true ECC)
            self.p = getPrime(256)
            self.a = random.randrange(1, self.p)
            self.b = random.randrange(1, self.p)
            self.g = 2  # Generator
            self.private_key = random.randrange(2, self.p - 1)
            self.public_key = pow(self.g, self.private_key, self.p)
    
    def encrypt(self, amount: int):
        """Encrypt transaction amount"""
        if self.mode == "Paillier":
            # Paillier encryption with random r
            r = random.randrange(1, self.n)
            while GCD(r, self.n) != 1:
                r = random.randrange(1, self.n)
            c = (pow(self.g, amount, self.n_sq) * pow(r, self.n, self.n_sq)) % self.n_sq
            return c
        
        elif self.mode == "RSA":
            # Encode as base^amount for additive homomorphism
            return pow(self.base, amount, self.n)
        
        elif self.mode == "DH":
            # DH-based: encode as g^amount
            return pow(self.g, amount, self.p)
        
        elif self.mode == "Rabin":
            # Rabin: c = m^2 mod n (encoding amount as base^amount first)
            base = 3
            m = pow(base, amount, self.n)
            return pow(m, 2, self.n)
        
        elif self.mode == "ECC":
            # ECC-like: encode as g^amount
            return pow(self.g, amount, self.p)
    
    def decrypt(self, ciphertext: int):
        """Decrypt transaction amount"""
        if self.mode == "Paillier":
            # Paillier decryption
            x = pow(ciphertext, self.lam, self.n_sq)
            L = (x - 1) // self.n
            m = (L * self.mu) % self.n
            return m
        
        elif self.mode == "RSA":
            # Decrypt by computing discrete log using baby-step giant-step
            return self._discrete_log(ciphertext, self.base, self.n, 50000)
        
        elif self.mode == "DH":
            # DH: discrete log
            return self._discrete_log(ciphertext, self.g, self.p, 10000)
        
        elif self.mode == "Rabin":
            # Rabin decryption: find square root, then discrete log
            # Simplified: use discrete log on sqrt
            roots = self._rabin_sqrt(ciphertext, self.p, self.q, self.n)
            if roots:
                base = 3
                for root in roots:
                    result = self._discrete_log(root, base, self.n, 10000)
                    if result >= 0 and result < 10000:
                        return result
            return -1
        
        elif self.mode == "ECC":
            # ECC-like: discrete log
            return self._discrete_log(ciphertext, self.g, self.p, 10000)
    
    def _discrete_log(self, y, base, mod, max_val):
        """Compute discrete log using baby-step giant-step"""
        step_size = 100
        
        # Quick check with steps
        for i in range(0, min(max_val, 10000), step_size):
            if pow(base, i, mod) == y:
                return i
        
        # Baby-step giant-step
        m = 1000
        cache = {}
        baby = 1
        for j in range(m):
            if baby == y:
                return j
            cache[baby] = j
            baby = (baby * base) % mod
        
        base_inv = pow(base, -m, mod)
        gamma = y
        for i in range(1, max_val // m + 1):
            gamma = (gamma * base_inv) % mod
            if gamma in cache:
                return i * m + cache[gamma]
        
        return -1
    
    def _rabin_sqrt(self, c, p, q, n):
        """Compute square roots for Rabin decryption"""
        try:
            mp = pow(c, (p + 1) // 4, p)
            mq = pow(c, (q + 1) // 4, q)
            
            yp = inverse(p, q)
            yq = inverse(q, p)
            
            r1 = (yp * p * mq + yq * q * mp) % n
            r2 = n - r1
            r3 = (yp * p * mq - yq * q * mp) % n
            r4 = n - r3
            
            return [r1, r2, r3, r4]
        except:
            return []
    
    def homomorphic_add(self, c1: int, c2: int):
        """Add two encrypted values homomorphically"""
        if self.mode == "Paillier":
            # Paillier: E(m1) * E(m2) = E(m1 + m2)
            return (c1 * c2) % self.n_sq
        elif self.mode in ["RSA", "DH", "Rabin", "ECC"]:
            # Multiplicative: base^a * base^b = base^(a+b)
            mod = self.n_sq if self.mode == "Paillier" else (self.n if self.mode in ["RSA", "Rabin"] else self.p)
            return (c1 * c2) % mod
    
    def homomorphic_multiply(self, ciphertext: int, scalar: int):
        """Multiply encrypted value by scalar homomorphically"""
        if self.mode == "Paillier":
            # Paillier: E(m)^k = E(k*m)
            return pow(ciphertext, scalar, self.n_sq)
        elif self.mode in ["RSA", "DH", "Rabin", "ECC"]:
            # Multiplicative: (base^a)^k = base^(a*k)
            mod = self.n_sq if self.mode == "Paillier" else (self.n if self.mode in ["RSA", "Rabin"] else self.p)
            return pow(ciphertext, scalar, mod)
    
    def get_public_params(self):
        """Get public parameters"""
        if self.mode == "Paillier":
            return {"n": self.n, "g": self.g, "mode": "Paillier"}
        elif self.mode == "RSA":
            return {"e": self.e, "n": self.n, "base": self.base, "mode": "RSA"}
        elif self.mode == "DH":
            return {"p": self.p, "g": self.g, "public_key": self.public_key, "mode": "DH"}
        elif self.mode == "Rabin":
            return {"n": self.n, "mode": "Rabin"}
        elif self.mode == "ECC":
            return {"p": self.p, "g": self.g, "a": self.a, "b": self.b, "public_key": self.public_key, "mode": "ECC"}

# ============================================================
# DIGITAL SIGNATURES
# ============================================================

class SignatureEngine:
    """Handles digital signatures with multiple algorithms"""
    
    def __init__(self, mode: str = None, hash_mode: str = None):
        self.mode = mode or config.SIGNATURE_ALGORITHM
        self.hash_mode = hash_mode or config.SIGNATURE_HASH
        
        if self.mode == "RSA":
            self.rsa_key = RSA.generate(config.RSA_KEY_SIZE)
            self.private_key = self.rsa_key
            self.public_key = self.rsa_key.publickey()
        
        elif self.mode == "ElGamal":
            self.p = getPrime(config.ELGAMAL_PRIME_SIZE)
            self.g = 2
            self.x = getPrime(config.ELGAMAL_PRIME_SIZE - 2)
            self.y = pow(self.g, self.x, self.p)
        
        elif self.mode == "Schnorr":
            # Schnorr signature with HARDCODED working parameters
            # These were generated and verified to work correctly
            self.p = 200352848149542087003978138766431076415648341552566979525330145435663198050727
            self.q = 100176424074771043501989069383215538207824170776283489762665072717831599025363
            self.g = 5
            
            # Only generate private key x and compute public key y
            self.x = random.randrange(1, self.q)
            self.y = pow(self.g, self.x, self.p)
        
        elif self.mode == "DH":
            # DH-based signature (similar to ElGamal)
            self.p = getPrime(config.DH_PRIME_SIZE)
            self.g = 2
            self.private_key = random.randrange(2, self.p - 1)
            self.public_key = pow(self.g, self.private_key, self.p)
    
    def _is_prime(self, n):
        """Simple primality test"""
        if n < 2:
            return False
        for i in range(2, min(int(n**0.5) + 1, 1000)):
            if n % i == 0:
                return False
        return True
    
    def _hash_data(self, data: bytes):
        """Hash data based on hash mode"""
        if self.hash_mode == "SHA256":
            return hashlib.sha256(data).digest()
        elif self.hash_mode == "SHA1":
            return hashlib.sha1(data).digest()
        elif self.hash_mode == "MD5":
            return hashlib.md5(data).digest()
        else:  # None
            return data
    
    def sign(self, data: bytes):
        """Sign data"""
        if self.mode == "RSA":
            # RSA signature
            hashed = self._hash_data(data)
            m = bytes_to_long(hashed)
            signature = pow(m, self.private_key.d, self.private_key.n)
            return {
                "signature": signature,
                "mode": "RSA",
                "hash": self.hash_mode
            }
        
        elif self.mode == "ElGamal":
            # ElGamal signature
            hashed = self._hash_data(data)
            m = bytes_to_long(hashed) % self.p
            
            while True:
                k = getPrime(128)
                if GCD(k, self.p - 1) == 1:
                    break
            r = pow(self.g, k, self.p)
            s = ((m - self.x * r) * inverse(k, self.p - 1)) % (self.p - 1)
            return {
                "r": r,
                "s": s,
                "mode": "ElGamal",
                "hash": self.hash_mode
            }
        
        elif self.mode == "Schnorr":
            # Schnorr signature using CORRECT algorithm: s = k + x*e (not k - x*e)
            hashed = self._hash_data(data)
            
            k = random.randrange(1, self.q)
            r = pow(self.g, k, self.p)
            
            # Compute challenge: e = H(r || m)
            r_bytes = r.to_bytes((r.bit_length() + 7) // 8, 'big')
            e = int.from_bytes(hashlib.sha256(r_bytes + hashed).digest(), 'big') % self.q
            
            # Compute signature: s = k + x*e mod q
            s = (k + self.x * e) % self.q
            
            return {
                "e": e,
                "s": s,
                "r": r,
                "mode": "Schnorr",
                "hash": self.hash_mode
            }
        
        elif self.mode == "DH":
            # DH-based signature (ElGamal-like)
            hashed = self._hash_data(data)
            m = bytes_to_long(hashed) % self.p
            
            k = random.randrange(2, self.p - 2)
            while GCD(k, self.p - 1) != 1:
                k = random.randrange(2, self.p - 2)
            
            r = pow(self.g, k, self.p)
            k_inv = inverse(k, self.p - 1)
            s = (k_inv * (m - self.private_key * r)) % (self.p - 1)
            
            return {
                "r": r,
                "s": s,
                "mode": "DH",
                "hash": self.hash_mode
            }
    
    def verify(self, data: bytes, signature: dict, public_key: dict = None):
        """Verify signature"""
        mode = signature.get("mode", self.mode)
        hash_mode = signature.get("hash", self.hash_mode)
        
        # Hash data based on mode used during signing
        if hash_mode == "SHA256":
            hashed = hashlib.sha256(data).digest()
        elif hash_mode == "SHA1":
            hashed = hashlib.sha1(data).digest()
        elif hash_mode == "MD5":
            hashed = hashlib.md5(data).digest()
        else:
            hashed = data
        
        if mode == "RSA":
            # Get expected hash
            expected = bytes_to_long(hashed)
            
            # Use provided public key or own
            if public_key:
                n = public_key["n"]
                e = public_key["e"]
            else:
                n = self.public_key.n
                e = self.public_key.e
            
            sig_value = signature["signature"]
            computed = pow(sig_value, e, n)
            return computed == expected
        
        elif mode == "ElGamal":
            # ElGamal verification
            m = bytes_to_long(hashed) % (public_key["p"] if public_key else self.p)
            
            p = public_key["p"] if public_key else self.p
            g = public_key["g"] if public_key else self.g
            y = public_key["y"] if public_key else self.y
            r, s = signature["r"], signature["s"]
            
            if not (0 < r < p):
                return False
            left = (pow(y, r, p) * pow(r, s, p)) % p
            right = pow(g, m, p)
            return left == right
        
        elif mode == "Schnorr":
            # Schnorr verification using CORRECT algorithm: r' = g^s * y^(-e) mod p
            p = public_key["p"] if public_key else self.p
            g = public_key["g"] if public_key else self.g
            y = public_key["y"] if public_key else self.y
            q = public_key["q"] if public_key else self.q
            
            e, s = signature["e"], signature["s"]
            
            # Recompute r: r' = g^s * y^(-e) mod p
            # This is equivalent to: g^s * inv(y^e) mod p
            r_prime = (pow(g, s, p) * inverse(pow(y, e, p), p)) % p
            
            # Recompute challenge: e' = H(r' || m)
            r_bytes = r_prime.to_bytes((r_prime.bit_length() + 7) // 8, 'big')
            e_prime = int.from_bytes(hashlib.sha256(r_bytes + hashed).digest(), 'big') % q
            
            return e == e_prime
        
        elif mode == "DH":
            # DH signature verification
            m = bytes_to_long(hashed) % (public_key["p"] if public_key else self.p)
            
            p = public_key["p"] if public_key else self.p
            g = public_key["g"] if public_key else self.g
            pub_key = public_key["public_key"] if public_key else self.public_key
            r, s = signature["r"], signature["s"]
            
            if not (0 < r < p):
                return False
            
            # Verify: g^m = y^r * r^s mod p
            left = pow(g, m, p)
            right = (pow(pub_key, r, p) * pow(r, s, p)) % p
            return left == right
        
        return False
    
    def get_public_key(self):
        """Get public key"""
        if self.mode == "RSA":
            return {
                "n": self.public_key.n,
                "e": self.public_key.e,
                "mode": "RSA"
            }
        elif self.mode == "ElGamal":
            return {
                "p": self.p,
                "g": self.g,
                "y": self.y,
                "mode": "ElGamal"
            }
        elif self.mode == "Schnorr":
            return {
                "p": self.p,
                "g": self.g,
                "y": self.y,
                "q": self.q,
                "mode": "Schnorr"
            }
        elif self.mode == "DH":
            return {
                "p": self.p,
                "g": self.g,
                "public_key": self.public_key,
                "mode": "DH"
            }

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def int_to_hex(i: int) -> str:
    """Convert integer to hex string"""
    return hex(i)[2:]

def hex_to_int(h: str) -> int:
    """Convert hex string to integer"""
    return int(h, 16)

def bytes_to_hex(b: bytes) -> str:
    """Convert bytes to hex string"""
    return b.hex()

def hex_to_bytes(h: str) -> bytes:
    """Convert hex string to bytes"""
    return bytes.fromhex(h)
