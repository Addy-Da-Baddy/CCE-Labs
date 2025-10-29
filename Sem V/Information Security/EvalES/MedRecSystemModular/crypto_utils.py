"""
Modular Cryptographic Utilities for Medical Records System
All cryptographic operations with algorithm selection support
"""

import json
import base64
import hashlib
import time
import random
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP, DES3
from Crypto.PublicKey import RSA, ECC, DSA
from Crypto.Signature import DSS
from Crypto.Util.number import getPrime, inverse, GCD, bytes_to_long, long_to_bytes
from Crypto.Util.Padding import pad, unpad
import config

# ============================================================
# 1. KEY ENCRYPTION (For wrapping AES keys)
# ============================================================

def encrypt_key(data: bytes, mode: str = None):
    """
    Encrypt data (e.g., AES key) using specified algorithm
    mode: "RSA", "ElGamal", "AES", "DES", "DH", "Rabin", "ECC"
    Returns: (ciphertext, key_info)
    """
    mode = mode or config.KEY_ENCRYPTION_ALGORITHM
    
    if mode == "RSA":
        # Generate RSA key pair for this operation
        key = RSA.generate(config.RSA_KEY_SIZE)
        cipher = PKCS1_OAEP.new(key.publickey())
        ciphertext = cipher.encrypt(data)
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "mode": "RSA",
            "private_key": key.export_key().decode()
        }
    
    elif mode == "ElGamal":
        # ElGamal encryption for key wrapping
        p = getPrime(config.ELGAMAL_PRIME_SIZE)
        g = 2
        x = getPrime(config.ELGAMAL_PRIME_SIZE - 2)  # Private key
        y = pow(g, x, p)  # Public key
        
        # Encrypt the data as integer
        m = bytes_to_long(data)
        k = getPrime(config.ELGAMAL_PRIME_SIZE - 2)  # Random k
        c1 = pow(g, k, p)
        c2 = (m * pow(y, k, p)) % p
        
        return {
            "c1": c1,
            "c2": c2,
            "mode": "ElGamal",
            "p": p,
            "g": g,
            "x": x  # Private key for decryption
        }
    
    elif mode == "DH":
        # Diffie-Hellman based encryption
        import random
        p = getPrime(config.DH_PRIME_SIZE)
        g = 2
        private_key = random.randrange(2, p - 1)
        public_key = pow(g, private_key, p)
        
        # Ephemeral key for encryption
        k = random.randrange(2, p - 1)
        c1 = pow(g, k, p)
        shared_secret = pow(public_key, k, p)
        
        # Use shared secret to encrypt data
        key_material = hashlib.sha256(str(shared_secret).encode()).digest()
        cipher = AES.new(key_material, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        return {
            "c1": c1,
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "tag": base64.b64encode(tag).decode(),
            "nonce": base64.b64encode(cipher.nonce).decode(),
            "mode": "DH",
            "p": p,
            "g": g,
            "private_key": private_key
        }
    
    elif mode == "Rabin":
        # Rabin cryptosystem
        bits = config.RABIN_KEY_SIZE // 2
        # Find primes ≡ 3 mod 4
        p = getPrime(bits)
        while p % 4 != 3:
            p = getPrime(bits)
        q = getPrime(bits)
        while q % 4 != 3:
            q = getPrime(bits)
        n = p * q
        
        # Pad data to ensure it's less than n
        m = bytes_to_long(data)
        if m >= n:
            # Use hybrid: encrypt data with AES, encrypt AES key with Rabin
            aes_key = get_random_bytes(32)
            cipher_aes = AES.new(aes_key, AES.MODE_GCM)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            m = bytes_to_long(aes_key)
        else:
            ciphertext = None
            tag = None
        
        # Rabin encryption: c = m^2 mod n
        c = pow(m, 2, n)
        
        return {
            "c": c,
            "ciphertext": base64.b64encode(ciphertext).decode() if ciphertext else None,
            "tag": base64.b64encode(tag).decode() if tag else None,
            "nonce": base64.b64encode(cipher_aes.nonce).decode() if ciphertext else None,
            "mode": "Rabin",
            "p": p,
            "q": q,
            "n": n
        }
    
    elif mode == "ECC":
        # ECC-based encryption (simplified using DH over curve)
        import random
        p = getPrime(256)
        a = random.randrange(1, p)
        b = random.randrange(1, p)
        g = 2  # Generator (simplified)
        
        private_key = random.randrange(2, p - 1)
        public_key = pow(g, private_key, p)
        
        # Ephemeral key
        k = random.randrange(2, p - 1)
        c1 = pow(g, k, p)
        shared = pow(public_key, k, p)
        
        # Use shared secret for AES encryption
        key_material = hashlib.sha256(str(shared).encode()).digest()
        cipher = AES.new(key_material, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        return {
            "c1": c1,
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "tag": base64.b64encode(tag).decode(),
            "nonce": base64.b64encode(cipher.nonce).decode(),
            "mode": "ECC",
            "p": p,
            "a": a,
            "b": b,
            "g": g,
            "private_key": private_key
        }
    
    elif mode == "AES":
        # Use a master AES key (would be pre-shared in real system)
        master_key = get_random_bytes(32)
        cipher = AES.new(master_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "nonce": base64.b64encode(cipher.nonce).decode(),
            "tag": base64.b64encode(tag).decode(),
            "mode": "AES",
            "master_key": base64.b64encode(master_key).decode()
        }
    
    elif mode == "DES":
        # Triple DES
        key = DES3.adjust_key_parity(get_random_bytes(24))
        cipher = DES3.new(key, DES3.MODE_CBC)
        ciphertext = cipher.encrypt(pad(data, DES3.block_size))
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "iv": base64.b64encode(cipher.iv).decode(),
            "mode": "DES",
            "key": base64.b64encode(key).decode()
        }
    
    else:
        raise ValueError(f"Unsupported key encryption mode: {mode}")

def decrypt_key(encrypted_data: dict):
    """Decrypt key using the stored mode and parameters"""
    mode = encrypted_data["mode"]
    
    if mode == "RSA":
        key = RSA.import_key(encrypted_data["private_key"].encode())
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(base64.b64decode(encrypted_data["ciphertext"]))
    
    elif mode == "ElGamal":
        # ElGamal decryption
        p = encrypted_data["p"]
        x = encrypted_data["x"]  # Private key
        c1 = encrypted_data["c1"]
        c2 = encrypted_data["c2"]
        
        # Decrypt: m = c2 * (c1^x)^(-1) mod p
        s = pow(c1, x, p)
        s_inv = inverse(s, p)
        m = (c2 * s_inv) % p
        
        # Convert back to bytes
        return long_to_bytes(m)
    
    elif mode == "DH":
        # DH decryption
        p = encrypted_data["p"]
        private_key = encrypted_data["private_key"]
        c1 = encrypted_data["c1"]
        
        # Compute shared secret
        shared_secret = pow(c1, private_key, p)
        key_material = hashlib.sha256(str(shared_secret).encode()).digest()
        
        # Decrypt with AES
        cipher = AES.new(key_material, AES.MODE_GCM, 
                        nonce=base64.b64decode(encrypted_data["nonce"]))
        return cipher.decrypt_and_verify(
            base64.b64decode(encrypted_data["ciphertext"]),
            base64.b64decode(encrypted_data["tag"])
        )
    
    elif mode == "Rabin":
        # Rabin decryption
        p = encrypted_data["p"]
        q = encrypted_data["q"]
        n = encrypted_data["n"]
        c = encrypted_data["c"]
        
        # Compute square roots
        mp = pow(c, (p + 1) // 4, p)
        mq = pow(c, (q + 1) // 4, q)
        
        yp = inverse(p, q)
        yq = inverse(q, p)
        
        r1 = (yp * p * mq + yq * q * mp) % n
        r2 = n - r1
        r3 = (yp * p * mq - yq * q * mp) % n
        r4 = n - r3
        
        # Try to find the right root
        for root in [r1, r2, r3, r4]:
            try:
                if encrypted_data.get("ciphertext"):
                    # It was hybrid encrypted
                    aes_key = long_to_bytes(root)
                    if len(aes_key) == 32:
                        cipher = AES.new(aes_key, AES.MODE_GCM,
                                       nonce=base64.b64decode(encrypted_data["nonce"]))
                        return cipher.decrypt_and_verify(
                            base64.b64decode(encrypted_data["ciphertext"]),
                            base64.b64decode(encrypted_data["tag"])
                        )
                else:
                    # Direct decryption
                    return long_to_bytes(root)
            except:
                continue
        
        raise ValueError("Failed to decrypt with Rabin")
    
    elif mode == "ECC":
        # ECC decryption
        p = encrypted_data["p"]
        private_key = encrypted_data["private_key"]
        c1 = encrypted_data["c1"]
        
        # Compute shared secret
        shared = pow(c1, private_key, p)
        key_material = hashlib.sha256(str(shared).encode()).digest()
        
        # Decrypt with AES
        cipher = AES.new(key_material, AES.MODE_GCM,
                        nonce=base64.b64decode(encrypted_data["nonce"]))
        return cipher.decrypt_and_verify(
            base64.b64decode(encrypted_data["ciphertext"]),
            base64.b64decode(encrypted_data["tag"])
        )
    
    elif mode == "AES":
        master_key = base64.b64decode(encrypted_data["master_key"])
        cipher = AES.new(master_key, AES.MODE_GCM, 
                        nonce=base64.b64decode(encrypted_data["nonce"]))
        return cipher.decrypt_and_verify(
            base64.b64decode(encrypted_data["ciphertext"]),
            base64.b64decode(encrypted_data["tag"])
        )
    
    elif mode == "DES":
        key = base64.b64decode(encrypted_data["key"])
        cipher = DES3.new(key, DES3.MODE_CBC, iv=base64.b64decode(encrypted_data["iv"]))
        return unpad(cipher.decrypt(base64.b64decode(encrypted_data["ciphertext"])), DES3.block_size)
    
    else:
        raise ValueError(f"Unsupported mode: {mode}")

# ============================================================
# 2. DIGITAL SIGNATURES
# ============================================================

class SignatureEngine:
    """Handles digital signatures with multiple algorithms"""
    
    def __init__(self, mode: str = None, hash_option: str = None):
        self.mode = mode or config.SIGNATURE_ALGORITHM
        self.hash_option = hash_option or config.SIGNATURE_HASH
        
        if self.mode == "ElGamal":
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
        
        elif self.mode == "RSA":
            # RSA signature setup
            self.rsa_key = RSA.generate(config.RSA_KEY_SIZE)
            self.private_key = self.rsa_key
            self.public_key = self.rsa_key.publickey()
        
        elif self.mode == "DH":
            # DH signature (simplified ElGamal-like signature)
            self.p = getPrime(config.DH_PRIME_SIZE)
            self.g = 2
            self.private_key = getPrime(config.DH_PRIME_SIZE - 2)
            self.public_key = pow(self.g, self.private_key, self.p)
    
    def _is_prime(self, n):
        """Simple primality test"""
        if n < 2:
            return False
        for i in range(2, min(int(n**0.5) + 1, 1000)):
            if n % i == 0:
                return False
        return True
    
    def _hash_data(self, message: str) -> bytes:
        """Hash data if hashing is enabled"""
        if self.hash_option == "SHA256":
            return hashlib.sha256(message.encode()).digest()
        elif self.hash_option == "SHA1":
            return hashlib.sha1(message.encode()).digest()
        elif self.hash_option == "MD5":
            return hashlib.md5(message.encode()).digest()
        else:  # No hash
            return message.encode()
    
    def sign(self, message: str):
        """Sign a message"""
        if self.mode == "ElGamal":
            # Apply optional hashing
            msg_bytes = self._hash_data(message)
            m = bytes_to_long(msg_bytes) % self.p
            
            while True:
                k = getPrime(128)
                if GCD(k, self.p - 1) == 1:
                    break
            r = pow(self.g, k, self.p)
            s = ((m - self.x * r) * inverse(k, self.p - 1)) % (self.p - 1)
            return {"r": r, "s": s, "ts": int(time.time()), "mode": "ElGamal", "hash": self.hash_option}
        
        elif self.mode == "Schnorr":
            # Schnorr signature using CORRECT algorithm: s = k + x*e (not k - x*e)
            msg_bytes = self._hash_data(message)
            
            k = random.randrange(1, self.q)
            r = pow(self.g, k, self.p)
            
            # Compute challenge: e = H(r || m)
            r_bytes = r.to_bytes((r.bit_length() + 7) // 8, 'big')
            e = int.from_bytes(hashlib.sha256(r_bytes + msg_bytes).digest(), 'big') % self.q
            
            # Compute signature: s = k + x*e mod q
            s = (k + self.x * e) % self.q
            
            return {"e": e, "s": s, "r": r, "ts": int(time.time()), "mode": "Schnorr", "hash": self.hash_option}
        
        elif self.mode == "RSA":
            # Apply optional hashing
            msg_bytes = self._hash_data(message)
            if self.hash_option != "None":
                signature = pow(bytes_to_long(msg_bytes), self.private_key.d, self.private_key.n)
            else:
                # Sign message directly (truncated to fit RSA key size)
                msg_bytes = msg_bytes[:200]  # Limit size
                signature = pow(bytes_to_long(msg_bytes), self.private_key.d, self.private_key.n)
            
            return {
                "signature": signature,
                "ts": int(time.time()),
                "mode": "RSA",
                "hash": self.hash_option
            }
        
        elif self.mode == "DH":
            # DH signature (ElGamal-like)
            msg_bytes = self._hash_data(message)
            m = bytes_to_long(msg_bytes) % self.p
            
            while True:
                k = getPrime(128)
                if GCD(k, self.p - 1) == 1:
                    break
            r = pow(self.g, k, self.p)
            s = ((m - self.private_key * r) * inverse(k, self.p - 1)) % (self.p - 1)
            return {"r": r, "s": s, "ts": int(time.time()), "mode": "DH", "hash": self.hash_option}
    
    def verify(self, message: str, signature: dict):
        """Verify a signature"""
        mode = signature.get("mode", self.mode)
        hash_used = signature.get("hash", self.hash_option)
        
        if mode == "ElGamal":
            # Apply same hashing as during signing
            # Temporarily set hash option for _hash_data
            old_hash = self.hash_option
            self.hash_option = hash_used
            msg_bytes = self._hash_data(message)
            self.hash_option = old_hash
            
            m = bytes_to_long(msg_bytes) % self.p
            
            r, s = signature["r"], signature["s"]
            if not (0 < r < self.p):
                return False
            left = (pow(self.y, r, self.p) * pow(r, s, self.p)) % self.p
            right = pow(self.g, m, self.p)
            return left == right
        
        elif mode == "Schnorr":
            # Schnorr verification using CORRECT algorithm: r' = g^s * y^(-e) mod p
            e, s = signature["e"], signature["s"]
            
            # Apply same hashing as during signing
            old_hash = self.hash_option
            self.hash_option = hash_used
            msg_bytes = self._hash_data(message)
            self.hash_option = old_hash
            
            # Recompute r: r' = g^s * y^(-e) mod p
            # This is equivalent to: g^s * inv(y^e) mod p
            r_prime = (pow(self.g, s, self.p) * inverse(pow(self.y, e, self.p), self.p)) % self.p
            
            # Recompute challenge: e' = H(r' || m)
            r_bytes = r_prime.to_bytes((r_prime.bit_length() + 7) // 8, 'big')
            e_prime = int.from_bytes(hashlib.sha256(r_bytes + msg_bytes).digest(), 'big') % self.q
            
            return e == e_prime
        
        elif mode == "RSA":
            # Apply same hashing as during signing
            old_hash = self.hash_option
            self.hash_option = hash_used
            msg_bytes = self._hash_data(message)
            self.hash_option = old_hash
            
            if hash_used != "None":
                expected_hash = bytes_to_long(msg_bytes)
            else:
                msg_bytes = msg_bytes[:200]
                expected_hash = bytes_to_long(msg_bytes)
            
            sig_value = signature["signature"]
            computed_hash = pow(sig_value, self.public_key.e, self.public_key.n)
            return computed_hash == expected_hash
        
        elif mode == "DH":
            # DH signature verification (ElGamal-like)
            old_hash = self.hash_option
            self.hash_option = hash_used
            msg_bytes = self._hash_data(message)
            self.hash_option = old_hash
            
            m = bytes_to_long(msg_bytes) % self.p
            
            r, s = signature["r"], signature["s"]
            if not (0 < r < self.p):
                return False
            left = (pow(self.public_key, r, self.p) * pow(r, s, self.p)) % self.p
            right = pow(self.g, m, self.p)
            return left == right
        
        return False
    
    def get_public_key(self):
        """Get public key for verification"""
        if self.mode == "ElGamal":
            return {"p": self.p, "g": self.g, "y": self.y, "mode": "ElGamal", "hash": self.hash_option}
        elif self.mode == "Schnorr":
            return {"p": self.p, "g": self.g, "y": self.y, "q": self.q, "mode": "Schnorr", "hash": self.hash_option}
        elif self.mode == "RSA":
            return {
                "n": self.public_key.n,
                "e": self.public_key.e,
                "mode": "RSA",
                "hash": self.hash_option
            }
        elif self.mode == "DH":
            return {"p": self.p, "g": self.g, "public_key": self.public_key, "mode": "DH", "hash": self.hash_option}

# ============================================================
# 3. DEPARTMENT ENCRYPTION (Privacy-Preserving Search)
# ============================================================

class DepartmentCrypto:
    """Handles department encryption for privacy-preserving searches"""
    
    def __init__(self, mode: str = None):
        self.mode = mode or config.DEPARTMENT_ENCRYPTION
        
        if self.mode == "Paillier":
            bits = config.PAILLIER_KEY_SIZE // 2
            self.p = getPrime(bits)
            self.q = getPrime(bits)
            self.n = self.p * self.q
            self.g = self.n + 1
            self.l = (self.p - 1) * (self.q - 1)
            self.mu = inverse(self.l, self.n)
        
        elif self.mode == "AES":
            # For AES, we use deterministic encryption (ECB - not recommended in production)
            self.key = get_random_bytes(32)
    
    def encrypt(self, department: str):
        """Encrypt department for searchable encryption"""
        if self.mode == "Paillier":
            # Deterministic Paillier (no randomness for exact matching)
            m = abs(hash(department)) % self.n
            return pow(self.g, m, self.n * self.n)
        
        elif self.mode == "AES":
            # Deterministic AES (ECB mode for same input = same output)
            cipher = AES.new(self.key, AES.MODE_ECB)
            padded = pad(department.encode(), AES.block_size)
            return base64.b64encode(cipher.encrypt(padded)).decode()
    
    def get_public_key(self):
        """Get public parameters"""
        if self.mode == "Paillier":
            return {"n": self.n, "g": self.g, "mode": "Paillier"}
        elif self.mode == "AES":
            return {"key": base64.b64encode(self.key).decode(), "mode": "AES"}

# ============================================================
# 4. EXPENSE HOMOMORPHIC ENCRYPTION
# ============================================================

def lcm(x, y):
    """Compute least common multiple"""
    from math import gcd
    return x * y // gcd(x, y)

class ExpenseCrypto:
    """Handles homomorphic encryption for expenses"""
    
    def __init__(self, mode: str = None):
        self.mode = mode or config.EXPENSE_ENCRYPTION
        
        if self.mode == "Paillier":
            # Proper Paillier key generation
            bits = config.PAILLIER_KEY_SIZE // 2
            self.p = getPrime(bits)
            self.q = getPrime(bits)
            self.n = self.p * self.q
            self.n_sq = self.n * self.n
            self.g = self.n + 1
            self.lam = lcm(self.p - 1, self.q - 1)
            self.mu = pow(self.lam, -1, self.n)
        
        elif self.mode == "RSA":
            # RSA homomorphic using discrete log trick for additive properties
            # Use smaller key for practical discrete log computation
            key = RSA.generate(1024)
            self.priv = key.export_key()
            self.pub = key.publickey().export_key()
            self.n = key.n
            self.e = key.e
            self.d = key.d
            self.base = 3  # Base for encoding amounts
    
    def encrypt(self, amount: int):
        """Encrypt expense amount"""
        if self.mode == "Paillier":
            # Proper Paillier encryption with random r
            import random
            r = random.randrange(1, self.n)
            while GCD(r, self.n) != 1:
                r = random.randrange(1, self.n)
            c = (pow(self.g, amount, self.n_sq) * pow(r, self.n, self.n_sq)) % self.n_sq
            return c
        
        elif self.mode == "RSA":
            # Encode amount as base^amount for additive homomorphism
            # base^a * base^b = base^(a+b)
            return pow(self.base, amount, self.n)
    
    def decrypt(self, ciphertext: int):
        """Decrypt expense amount"""
        if self.mode == "Paillier":
            # Proper Paillier decryption
            x = pow(ciphertext, self.lam, self.n_sq)
            L = (x - 1) // self.n
            m = (L * self.mu) % self.n
            return m
        
        elif self.mode == "RSA":
            # Decrypt by computing discrete log using baby-step giant-step
            max_expense = 50000  # Maximum sum we expect
            step_size = 100
            
            # First, narrow down range using giant steps
            for i in range(0, max_expense, step_size):
                val = pow(self.base, i, self.n)
                if val == ciphertext:
                    return i
            
            # Baby-step giant-step for exact value
            cache = {}
            m = 1000  # Baby step size
            
            # Baby steps: compute base^j for j = 0 to m-1
            baby = 1
            for j in range(m):
                if baby == ciphertext:
                    return j
                cache[baby] = j
                baby = (baby * self.base) % self.n
            
            # Giant steps: compute ciphertext * (base^(-m))^i
            base_inv = pow(self.base, -m, self.n)
            gamma = ciphertext
            for i in range(1, max_expense // m + 1):
                gamma = (gamma * base_inv) % self.n
                if gamma in cache:
                    return i * m + cache[gamma]
            
            return -1  # Not found
    
    def homomorphic_add(self, c1: int, c2: int):
        """Add two encrypted values homomorphically"""
        if self.mode == "Paillier":
            # Paillier: E(m1) * E(m2) = E(m1 + m2)
            return (c1 * c2) % self.n_sq
        elif self.mode == "RSA":
            # RSA discrete log: base^a * base^b = base^(a+b)
            return (c1 * c2) % self.n
    
    def homomorphic_multiply(self, ciphertext: int, scalar: int):
        """Multiply encrypted value by scalar homomorphically"""
        if self.mode == "Paillier":
            # Paillier: E(m)^k = E(k*m)
            # Scalar multiplication: raising ciphertext to power of scalar
            return pow(ciphertext, scalar, self.n_sq)
        elif self.mode == "RSA":
            # RSA discrete log: (base^a)^k = base^(a*k)
            # For base^a representing 'a', raising to power k gives base^(a*k) representing a*k
            return pow(ciphertext, scalar, self.n)
    
    def get_public_key(self):
        """Get public parameters"""
        if self.mode == "Paillier":
            return {"n": self.n, "g": self.g, "mode": "Paillier"}
        elif self.mode == "RSA":
            return {"e": self.e, "n": self.n, "mode": "RSA"}

# ============================================================
# 5. REPORT CONTENT ENCRYPTION
# ============================================================

def encrypt_report(data: bytes, mode: str = None):
    """
    Encrypt report content with authenticated encryption
    mode: "AES", "RSA", "ElGamal", "DES"
    """
    mode = mode or config.REPORT_ENCRYPTION
    
    if mode == "AES":
        key = get_random_bytes(32)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "nonce": base64.b64encode(cipher.nonce).decode(),
            "tag": base64.b64encode(tag).decode(),
            "key": base64.b64encode(key).decode(),
            "mode": "AES"
        }
    
    elif mode == "DES":
        key = DES3.adjust_key_parity(get_random_bytes(24))
        cipher = DES3.new(key, DES3.MODE_CBC)
        ciphertext = cipher.encrypt(pad(data, DES3.block_size))
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "iv": base64.b64encode(cipher.iv).decode(),
            "key": base64.b64encode(key).decode(),
            "mode": "DES"
        }
    
    elif mode == "RSA":
        # For large data, encrypt data with AES, then wrap AES key with RSA
        aes_key = get_random_bytes(32)
        cipher = AES.new(aes_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        rsa_key = RSA.generate(2048)
        rsa_cipher = PKCS1_OAEP.new(rsa_key.publickey())
        wrapped_key = rsa_cipher.encrypt(aes_key)
        
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "nonce": base64.b64encode(cipher.nonce).decode(),
            "tag": base64.b64encode(tag).decode(),
            "wrapped_key": base64.b64encode(wrapped_key).decode(),
            "rsa_private": rsa_key.export_key().decode(),
            "mode": "RSA"
        }
    
    elif mode == "ElGamal":
        # ElGamal for report: encrypt with AES, wrap key with ElGamal
        aes_key = get_random_bytes(32)
        cipher = AES.new(aes_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        # ElGamal key wrapping
        p = getPrime(config.ELGAMAL_PRIME_SIZE)
        g = 2
        x = getPrime(config.ELGAMAL_PRIME_SIZE - 2)  # Private key
        y = pow(g, x, p)  # Public key
        
        # Encrypt AES key
        m = bytes_to_long(aes_key)
        k = getPrime(config.ELGAMAL_PRIME_SIZE - 2)
        c1 = pow(g, k, p)
        c2 = (m * pow(y, k, p)) % p
        
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "nonce": base64.b64encode(cipher.nonce).decode(),
            "tag": base64.b64encode(tag).decode(),
            "c1": c1,
            "c2": c2,
            "elgamal_p": p,
            "elgamal_g": g,
            "elgamal_x": x,
            "mode": "ElGamal"
        }
    
    else:
        raise ValueError(f"Unsupported report encryption mode: {mode}")

def decrypt_report(encrypted_data: dict):
    """Decrypt report content"""
    mode = encrypted_data["mode"]
    
    if mode == "AES":
        key = base64.b64decode(encrypted_data["key"])
        cipher = AES.new(key, AES.MODE_GCM, nonce=base64.b64decode(encrypted_data["nonce"]))
        return cipher.decrypt_and_verify(
            base64.b64decode(encrypted_data["ciphertext"]),
            base64.b64decode(encrypted_data["tag"])
        )
    
    elif mode == "DES":
        key = base64.b64decode(encrypted_data["key"])
        cipher = DES3.new(key, DES3.MODE_CBC, iv=base64.b64decode(encrypted_data["iv"]))
        return unpad(cipher.decrypt(base64.b64decode(encrypted_data["ciphertext"])), DES3.block_size)
    
    elif mode == "RSA":
        rsa_key = RSA.import_key(encrypted_data["rsa_private"].encode())
        rsa_cipher = PKCS1_OAEP.new(rsa_key)
        aes_key = rsa_cipher.decrypt(base64.b64decode(encrypted_data["wrapped_key"]))
        
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=base64.b64decode(encrypted_data["nonce"]))
        return cipher.decrypt_and_verify(
            base64.b64decode(encrypted_data["ciphertext"]),
            base64.b64decode(encrypted_data["tag"])
        )
    
    elif mode == "ElGamal":
        # Decrypt ElGamal-wrapped AES key
        p = encrypted_data["elgamal_p"]
        x = encrypted_data["elgamal_x"]
        c1 = encrypted_data["c1"]
        c2 = encrypted_data["c2"]
        
        # Decrypt: m = c2 * (c1^x)^(-1) mod p
        s = pow(c1, x, p)
        s_inv = inverse(s, p)
        m = (c2 * s_inv) % p
        
        # Convert back to AES key
        aes_key = long_to_bytes(m)
        
        # Decrypt AES-encrypted content
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=base64.b64decode(encrypted_data["nonce"]))
        return cipher.decrypt_and_verify(
            base64.b64decode(encrypted_data["ciphertext"]),
            base64.b64decode(encrypted_data["tag"])
        )
    
    else:
        raise ValueError(f"Unsupported mode: {mode}")

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def int_to_hex(i: int) -> str:
    """Convert integer to hex string"""
    return hex(i)[2:]

def hex_to_int(h: str) -> int:
    """Convert hex string to integer"""
    return int(h, 16)
