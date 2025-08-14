import time
from Crypto.PublicKey import RSA, ECC
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256

def rsa_generate_keys():
    start = time.time()
    rsa_key = RSA.generate(2048)
    rsa_pub = rsa_key.publickey()
    return rsa_key, rsa_pub, time.time() - start

def rsa_encrypt_decrypt(data, rsa_key, rsa_pub):
    cipher_rsa_enc = PKCS1_OAEP.new(rsa_pub)
    cipher_rsa_dec = PKCS1_OAEP.new(rsa_key)
    start_enc = time.time()
    encrypted = cipher_rsa_enc.encrypt(data[:190])  
    enc_time = time.time() - start_enc
    start_dec = time.time()
    decrypted = cipher_rsa_dec.decrypt(encrypted)
    dec_time = time.time() - start_dec
    return enc_time, dec_time, decrypted

def ecc_generate_keys():
    start = time.time()
    priv = ECC.generate(curve='P-256')
    pub = priv.public_key()
    return priv, pub, time.time() - start

def derive_ecc_key(priv, pub):
    shared_point = priv.d * pub.pointQ
    shared_bytes = int(shared_point.x).to_bytes(32, 'big')
    return HKDF(shared_bytes, 32, b'', SHA256)

def ecc_encrypt_decrypt(data, priv, pub):
    eph_priv = ECC.generate(curve='P-256')
    eph_pub = eph_priv.public_key()
    key = derive_ecc_key(eph_priv, pub)
    start_enc = time.time()
    cipher = AES.new(key, AES.MODE_GCM)
    ct, tag = cipher.encrypt_and_digest(data)
    enc_time = time.time() - start_enc
    key_dec = derive_ecc_key(priv, eph_pub)
    start_dec = time.time()
    cipher_dec = AES.new(key_dec, AES.MODE_GCM, nonce=cipher.nonce)
    decrypted = cipher_dec.decrypt_and_verify(ct, tag)
    dec_time = time.time() - start_dec
    return enc_time, dec_time, decrypted


def benchmark(method, size_kb):
    data = get_random_bytes(size_kb * 1024)
    print(f"\n--- {method} Benchmark ({size_kb} KB) ---")
    if method == "RSA":
        rsa_key, rsa_pub, keygen_time = rsa_generate_keys()
        enc_time, dec_time, decrypted = rsa_encrypt_decrypt(data, rsa_key, rsa_pub)
    elif method == "ECC-ElGamal":
        priv, pub, keygen_time = ecc_generate_keys()
        enc_time, dec_time, decrypted = ecc_encrypt_decrypt(data, priv, pub)
    else:
        return
    print(f"Key Generation Time: {keygen_time:.4f} sec")
    print(f"Encryption Time: {enc_time:.4f} sec")
    print(f"Decryption Time: {dec_time:.4f} sec")
    print("Success:", decrypted == data[:len(decrypted)])

for size in [1, 10]:
    benchmark("RSA", size)
    benchmark("ECC-ElGamal", size)
