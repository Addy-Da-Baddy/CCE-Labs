import time
import os
from Crypto.PublicKey import RSA, ECC
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256

def generate_test_file(filename, size_mb):
    with open(filename, 'wb') as f:
        f.write(os.urandom(size_mb * 1024 * 1024))

def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce, ciphertext, tag

def aes_decrypt(nonce, ciphertext, tag, key):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def rsa_encrypt_key(aes_key, rsa_pub):
    cipher_rsa = PKCS1_OAEP.new(rsa_pub)
    return cipher_rsa.encrypt(aes_key)

def rsa_decrypt_key(enc_key, rsa_priv):
    cipher_rsa = PKCS1_OAEP.new(rsa_priv)
    return cipher_rsa.decrypt(enc_key)

def ecc_encrypt_key(aes_key, ecc_pub):
    eph_key = ECC.generate(curve='P-256')
    shared_secret = eph_key.d * ecc_pub.pointQ
    secret_bytes = int(shared_secret.x).to_bytes(32, 'big')
    derived_key = HKDF(secret_bytes, 32, b'', SHA256)
    nonce, ciphertext, tag = aes_encrypt(aes_key, derived_key)
    return eph_key.public_key(), nonce, ciphertext, tag

def ecc_decrypt_key(eph_pub, nonce, ciphertext, tag, ecc_priv):
    shared_secret = ecc_priv.d * eph_pub.pointQ
    secret_bytes = int(shared_secret.x).to_bytes(32, 'big')
    derived_key = HKDF(secret_bytes, 32, b'', SHA256)
    return aes_decrypt(nonce, ciphertext, tag, derived_key)

def benchmark_encryption(filename, method):
    with open(filename, 'rb') as f:
        data = f.read()

    aes_key = get_random_bytes(32)

    start = time.time()
    nonce, ciphertext, tag = aes_encrypt(data, aes_key)
    enc_time = time.time() - start

    if method == 'RSA':
        start = time.time()
        rsa_key = RSA.generate(2048)
        rsa_pub = rsa_key.publickey()
        enc_key = rsa_encrypt_key(aes_key, rsa_pub)
        dec_key = rsa_decrypt_key(enc_key, rsa_key)
        dec_time = time.time() - start
    elif method == 'ECC':
        start = time.time()
        ecc_key = ECC.generate(curve='P-256')
        ecc_pub = ecc_key.public_key()
        eph_pub, nonce_key, ct_key, tag_key = ecc_encrypt_key(aes_key, ecc_pub)
        dec_key = ecc_decrypt_key(eph_pub, nonce_key, ct_key, tag_key, ecc_key)
        dec_time = time.time() - start
    else:
        raise ValueError("Method must be 'RSA' or 'ECC'")

    assert dec_key == aes_key
    print(f"\n--- {method} Benchmark ---")
    print(f"File Size: {len(data) / (1024*1024):.2f} MB")
    print(f"Encryption Time: {enc_time:.4f} sec")
    print(f"{method} Key Enc/Dec Time: {dec_time:.4f} sec")
    print(f"{method} Key Size: {len(dec_key)} bytes")
    print("AES Key Verified")

if __name__ == "__main__":
    generate_test_file("test_1mb.bin", 1)
    generate_test_file("test_10mb.bin", 10)

    benchmark_encryption("test_1mb.bin", "RSA")
    benchmark_encryption("test_10mb.bin", "RSA")

    benchmark_encryption("test_1mb.bin", "ECC")
    benchmark_encryption("test_10mb.bin", "ECC")
