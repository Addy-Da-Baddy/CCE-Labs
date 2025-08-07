from Crypto.Cipher import AES
from Crypto.Util import Counter

def encrypt_ctr(message, key_str, nonce_str):
    print("Plaintext Message:", message)
    key = key_str.encode('utf-8')[:32]
    nonce = nonce_str.encode('utf-8')[:8]

    ctr = Counter.new(64, prefix=nonce, initial_value=0)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

    ct = cipher.encrypt(message.encode('utf-8'))
    print("Ciphertext (hex):", ct.hex())
    return ct

def decrypt_ctr(ct, key_str, nonce_str):
    key = key_str.encode('utf-8')[:32]
    nonce = nonce_str.encode('utf-8')[:8]

    ctr = Counter.new(64, prefix=nonce, initial_value=0)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

    pt = cipher.decrypt(ct)
    print("Decrypted Plaintext:", pt.decode('utf-8'))
    return pt

key = "0123456789ABCDEF0123456789ABCDEF"
nonce = "00000000"
message = "Cryptography Lab Exercise"

ct = encrypt_ctr(message, key, nonce)
pt = decrypt_ctr(ct, key, nonce)

print("Success:", pt.decode('utf-8') == message)
