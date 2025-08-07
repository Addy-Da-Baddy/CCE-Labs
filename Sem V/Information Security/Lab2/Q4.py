from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

def encrypt(pt, key):
    print("Plaintext: ", pt)
    pt = pt.encode('utf-8')

    #key is 24 bytes for DES3
    key = key[:24].encode('utf-8')
    cipher = DES3.new(key, DES3.MODE_ECB)

    padded_pt = pad(pt, DES3.block_size)
    ct = cipher.encrypt(padded_pt)

    print("Ciphertext: ", ct.hex())
    return ct

def decrypt(ct, key):
    key = key[:24].encode('utf-8')
    cipher = DES3.new(key, DES3.MODE_ECB)

    pt_padded = cipher.decrypt(ct)
    pt = unpad(pt_padded, DES3.block_size)
    pt = pt.decode('utf-8')

    print("Decrypted from CT: ", pt)
    return pt

key = "1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF"
message = "Classified Text"

ct = encrypt(message, key)
dt = decrypt(ct, key)

print("Successful Encryption and Decryption: ", message == dt)
