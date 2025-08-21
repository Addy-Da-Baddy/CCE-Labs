import os
import json
import logging
from datetime import datetime, timedelta
from Crypto.Util.number import getPrime, getRandomRange, inverse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Setup logging
logging.basicConfig(filename="drm_kms.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ElGamal:
    def __init__(self, p=None, g=None, x=None, y=None):
        self.p = p
        self.g = g
        self.x = x
        self.y = y

    def generate_keys(self, bits=2048):
        self.p = getPrime(bits)
        self.g = 2  # Common choice, should be primitive root mod p
        self.x = getRandomRange(2, self.p - 2)
        self.y = pow(self.g, self.x, self.p)
        logging.info("Generated ElGamal key pair")
        return (self.p, self.g, self.y), self.x

    def encrypt(self, m):
        # m must be an integer < p
        k = getRandomRange(2, self.p - 2)
        c1 = pow(self.g, k, self.p)
        c2 = (m * pow(self.y, k, self.p)) % self.p
        return (c1, c2)

    def decrypt(self, c1, c2):
        s = pow(c1, self.x, self.p)
        s_inv = inverse(s, self.p)
        m = (c2 * s_inv) % self.p
        return m

class DRMKeyManagementService:
    def __init__(self, key_size=2048, storage_file="drm_keys.json", aes_key=None):
        self.key_size = key_size
        self.storage_file = storage_file
        self.master_key = None  # instance of ElGamal
        self.access_control = {}  # {customer_id: {content_id: expiry_datetime}}
        self.aes_key = aes_key or get_random_bytes(32)  # For encrypting private key storage
        self.load_keys()

    def generate_master_keypair(self):
        self.master_key = ElGamal()
        public_key, private_key = self.master_key.generate_keys(self.key_size)
        self.save_keys(private_key)
        logging.info("Master ElGamal key pair generated")
        return public_key

    def save_keys(self, private_key):
        # Store keys with encrypted private key
        # Serialize private key as bytes and encrypt with AES
        priv_key_bytes = private_key.to_bytes((private_key.bit_length() + 7) // 8, 'big')
        iv = get_random_bytes(16)
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(priv_key_bytes, AES.block_size))

        data = {
            "public_key": {
                "p": self.master_key.p,
                "g": self.master_key.g,
                "y": self.master_key.y
            },
            "private_key": (iv + ct).hex()
        }

        with open(self.storage_file, "w") as f:
            json.dump(data, f)

    def load_keys(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                data = json.load(f)
            p = int(data["public_key"]["p"])
            g = int(data["public_key"]["g"])
            y = int(data["public_key"]["y"])

            priv_encrypted = bytes.fromhex(data["private_key"])
            iv = priv_encrypted[:16]
            ct = priv_encrypted[16:]
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
            priv_padded = cipher.decrypt(ct)
            priv_bytes = unpad(priv_padded, AES.block_size)
            x = int.from_bytes(priv_bytes, 'big')

            self.master_key = ElGamal(p, g, x, y)
            logging.info("Loaded master key from storage")
        else:
            logging.warning("No stored keys found, generate keys first.")

    def encrypt_content(self, content_bytes):
        # Hybrid encryption:
        # 1) Generate random AES key
        aes_key = get_random_bytes(32)
        iv = get_random_bytes(16)
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        encrypted_content = iv + cipher.encrypt(pad(content_bytes, AES.block_size))

        # 2) Encrypt AES key using ElGamal public key
        aes_key_int = int.from_bytes(aes_key, 'big')
        if aes_key_int >= self.master_key.p:
            raise ValueError("AES key integer too large for ElGamal encryption")
        c1, c2 = self.master_key.encrypt(aes_key_int)

        logging.info("Content encrypted with AES + ElGamal hybrid encryption")
        return {
            "elgamal_encrypted_key": (c1, c2),
            "encrypted_content": encrypted_content.hex()
        }

    def decrypt_content(self, c1, c2, encrypted_content_hex):
        # Decrypt AES key using private key
        aes_key_int = self.master_key.decrypt(c1, c2)
        aes_key = aes_key_int.to_bytes(32, 'big')

        # Decrypt content
        encrypted_content = bytes.fromhex(encrypted_content_hex)
        iv = encrypted_content[:16]
        ct = encrypted_content[16:]
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        content = unpad(cipher.decrypt(ct), AES.block_size)

        logging.info("Content decrypted successfully")
        return content

    def grant_access(self, customer_id, content_id, duration_hours):
        expiry = datetime.now() + timedelta(hours=duration_hours)
        if customer_id not in self.access_control:
            self.access_control[customer_id] = {}
        self.access_control[customer_id][content_id] = expiry
        logging.info(f"Granted access to customer {customer_id} for content {content_id} until {expiry}")

    def revoke_access(self, customer_id, content_id):
        if customer_id in self.access_control and content_id in self.access_control[customer_id]:
            del self.access_control[customer_id][content_id]
            logging.info(f"Revoked access for customer {customer_id} on content {content_id}")

    def check_access(self, customer_id, content_id):
        if customer_id in self.access_control and content_id in self.access_control[customer_id]:
            expiry = self.access_control[customer_id][content_id]
            if datetime.now() < expiry:
                return True
        return False

    def distribute_private_key(self, customer_id):
        # Simulate secure distribution by returning private key if authorized
        # In reality, would involve secure channel, auth, and key wrapping
        # Here, just simulate: only authorized customers (for demo)
        # WARNING: Distributing master private key is risky!
        authorized_customers = {"customer1", "customer2"}  # example
        if customer_id in authorized_customers:
            logging.info(f"Distributed master private key to {customer_id}")
            return self.master_key.x  # private key integer
        else:
            logging.warning(f"Unauthorized key request by {customer_id}")
            return None

    def revoke_master_key(self):
        self.master_key = None
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)
        logging.warning("Master key revoked and storage cleared")

    def renew_master_key(self):
        self.generate_master_keypair()
        logging.info("Master key renewed")

# ----------------------------
# Demo usage:

if __name__ == "__main__":
    drm = DRMKeyManagementService()

    # Generate master keys if not present
    if drm.master_key is None:
        public_key = drm.generate_master_keypair()
        print("Master public key generated.")

    # Content creator uploads content
    content = b"Top secret movie file bytes ..."
    encrypted_data = drm.encrypt_content(content)
    print("Content encrypted.")

    # Grant access to customer1 for 1 hour
    drm.grant_access("customer1", "movie1", duration_hours=1)

    # Check access
    print("Customer1 access to movie1:", drm.check_access("customer1", "movie1"))

    # Customer tries to get private key
    priv_key = drm.distribute_private_key("customer1")
    if priv_key:
        print("Customer1 received private key.")
    else:
        print("Customer1 NOT authorized for private key.")

    # Customer decrypts content if access allowed
    if drm.check_access("customer1", "movie1"):
        c1, c2 = encrypted_data["elgamal_encrypted_key"]
        decrypted_content = drm.decrypt_content(c1, c2, encrypted_data["encrypted_content"])
        print("Decrypted content:", decrypted_content)

    # Revoke access
    drm.revoke_access("customer1", "movie1")
    print("Access revoked.")

    # Re-check access
    print("Customer1 access to movie1:", drm.check_access("customer1", "movie1"))

    # Revoke master key (e.g. breach)
    drm.revoke_master_key()
    print("Master key revoked.")

    # Renew master key (e.g. 24 months later)
    drm.renew_master_key()
    print("Master key renewed.")
