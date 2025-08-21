import os
import json
import logging
import time
from Crypto.Util.number import getPrime, inverse
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta

logging.basicConfig(filename="kms.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class RabinKeyPair:
    def __init__(self, p, q, n):
        self.p = p
        self.q = q
        self.n = n

class KeyManagementService:
    def __init__(self, key_size=1024, storage_file="keys_storage.json", aes_key=None):
        self.key_size = key_size
        self.storage_file = storage_file
        self.keys = {}  
        
        self.aes_key = aes_key or get_random_bytes(32)
        
        self.load_keys()
        
    def generate_rabin_keypair(self):
        while True:
            p = getPrime(self.key_size // 2)
            if p % 4 == 3:
                break
        while True:
            q = getPrime(self.key_size // 2)
            if q % 4 == 3 and q != p:
                break
        n = p * q
        return RabinKeyPair(p, q, n)
    
    def encrypt_private_key(self, p, q):
        data = json.dumps({'p': p, 'q': q}).encode()
        iv = get_random_bytes(16)
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(data, AES.block_size))
        return iv + ct
    
    def decrypt_private_key(self, encrypted_data):
        iv = encrypted_data[:16]
        ct = encrypted_data[16:]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        data = unpad(cipher.decrypt(ct), AES.block_size)
        keys = json.loads(data.decode())
        return keys['p'], keys['q']
    
    def add_facility(self, name):
        if name in self.keys:
            logging.warning(f"Add facility failed: {name} already exists.")
            return None
        
        keypair = self.generate_rabin_keypair()
        encrypted_priv = self.encrypt_private_key(keypair.p, keypair.q)
        
        self.keys[name] = {
            'public_key': keypair.n,
            'private_key_encrypted': encrypted_priv.hex(),
            'created_at': datetime.utcnow().isoformat(),
            'revoked': False
        }
        self.save_keys()
        logging.info(f"Key generated for facility: {name}")
        return keypair.n, (keypair.p, keypair.q)
    
    def get_keys(self, name):
        if name not in self.keys:
            logging.warning(f"Key request failed: {name} not found.")
            return None
        
        record = self.keys[name]
        if record['revoked']:
            logging.warning(f"Key request failed: {name} keys revoked.")
            return None
        
        n = record['public_key']
        p, q = self.decrypt_private_key(bytes.fromhex(record['private_key_encrypted']))
        logging.info(f"Keys retrieved for facility: {name}")
        return n, (p, q)
    
    def revoke_keys(self, name):
        if name not in self.keys:
            logging.warning(f"Revoke failed: {name} not found.")
            return False
        self.keys[name]['revoked'] = True
        self.save_keys()
        logging.info(f"Keys revoked for facility: {name}")
        return True
    
    def renew_keys(self, name):
        if name not in self.keys:
            logging.warning(f"Renew failed: {name} not found.")
            return False
        keypair = self.generate_rabin_keypair()
        encrypted_priv = self.encrypt_private_key(keypair.p, keypair.q)
        self.keys[name].update({
            'public_key': keypair.n,
            'private_key_encrypted': encrypted_priv.hex(),
            'created_at': datetime.utcnow().isoformat(),
            'revoked': False
        })
        self.save_keys()
        logging.info(f"Keys renewed for facility: {name}")
        return True
    
    def renew_all_keys(self):
        for name in list(self.keys.keys()):
            if not self.keys[name]['revoked']:
                self.renew_keys(name)
        logging.info("All active keys renewed.")
    
    def save_keys(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.keys, f)
    
    def load_keys(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                self.keys = json.load(f)
        else:
            self.keys = {}

if __name__ == "__main__":
    kms = KeyManagementService(key_size=1024)
    
    print("Adding hospital A keys...")
    pub, priv = kms.add_facility("Hospital_A")
    print(f"Hospital_A public key (n): {pub}")
    
    print("Retrieving Hospital_A keys...")
    keys = kms.get_keys("Hospital_A")
    print(f"Retrieved keys: {keys}")
    
    print("Revoking Hospital_A keys...")
    kms.revoke_keys("Hospital_A")
    
    print("Trying to retrieve revoked keys...")
    revoked_keys = kms.get_keys("Hospital_A")
    print(f"Revoked keys retrieval result: {revoked_keys}")
    
    print("Renewing Hospital_A keys (should succeed since revoked)")
    kms.renew_keys("Hospital_A")
    
    renewed_keys = kms.get_keys("Hospital_A")
    print(f"Renewed keys: {renewed_keys}")
    
    kms.renew_all_keys()
