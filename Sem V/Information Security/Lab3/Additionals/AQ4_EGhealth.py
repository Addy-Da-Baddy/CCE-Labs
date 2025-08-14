import time
from Crypto.PublicKey import ECC
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

def generate_ecc_keys():
    priv = ECC.generate(curve='P-256')
    pub = priv.public_key()
    return priv, pub

def derive_shared_key(priv, pub):
    shared_point = priv.d * pub.pointQ
    shared_bytes = int(shared_point.x).to_bytes(32, 'big')
    return HKDF(shared_bytes, 32, b'', SHA256)

def encrypt_data(data, pub):
    eph_priv = ECC.generate(curve='P-256')
    eph_pub = eph_priv.public_key()
    key = derive_shared_key(eph_priv, pub)
    cipher = AES.new(key, AES.MODE_GCM)
    ct, tag = cipher.encrypt_and_digest(data)
    return eph_pub, cipher.nonce, ct, tag

def decrypt_data(eph_pub, nonce, ct, tag, priv):
    key = derive_shared_key(priv, eph_pub)
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    return cipher.decrypt_and_verify(ct, tag)

def benchmark_ecc_elgamal(size_kb):
    data = get_random_bytes(size_kb * 1024)
    priv, pub = generate_ecc_keys()

    start = time.time()
    eph_pub, nonce, ct, tag = encrypt_data(data, pub)
    enc_time = time.time() - start

    start = time.time()
    decrypted = decrypt_data(eph_pub, nonce, ct, tag, priv)
    dec_time = time.time() - start

    print(f"\nECC-ElGamal Benchmark ({size_kb} KB):")
    print(f"Encryption Time: {enc_time:.4f} sec")
    print(f"Decryption Time: {dec_time:.4f} sec")
    print("Success:", decrypted == data)

for size in [1, 10, 100]:
    benchmark_ecc_elgamal(size)
