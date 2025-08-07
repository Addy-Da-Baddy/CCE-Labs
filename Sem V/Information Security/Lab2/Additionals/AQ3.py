from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt(pt, key):
    print("Plaintext: ", pt)
    pt = pt.encode('utf-8')

    key = key[:32].encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)

    padded_pt = pad(pt, AES.block_size)
    print("Padded Plaintext (hex):", padded_pt.hex())

    ct = cipher.encrypt(padded_pt)
    print("Ciphertext (hex):", ct.hex())
    return ct

def decrypt(ct, key):
    key = key[:32].encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)

    pt_padded = cipher.decrypt(ct)
    pt = unpad(pt_padded, AES.block_size)
    pt = pt.decode('utf-8')

    print("Decrypted from CT: ", pt)
    return pt

key = "0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF"
message = "Encryption Strength"

ct = encrypt(message, key)
dt = decrypt(ct, key)

print("Successful Encryption and Decryption: ", message == dt)
