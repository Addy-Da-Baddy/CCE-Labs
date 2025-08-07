from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad

def encrypt(pt ,key):
    print("Plaintext: ", pt)
    pt = pt.encode('utf-8')
    key = key[:16].encode('utf-8') #as AES-128 only first 16 bytes
    cipher = AES.new(key, AES.MODE_ECB)
    padded_pt = pad(pt,AES.block_size)
    ct = cipher.encrypt(padded_pt)
    print("Ciphertext: ", ct.hex())
    return ct

def decrypt(ct,key):
    key = key[:16].encode('utf-8')
    cipher = AES.new(key,AES.MODE_ECB)
    pt_padded = cipher.decrypt(ct)
    pt = unpad(pt_padded, AES.block_size)
    pt = pt.decode('utf-8')
    print("Decrypted from CT: ", pt)
    return pt

key = "0123456789ABCDEF0123456789ABCDEF"
message = "Sensitive Information"

ct = encrypt(message, key)
dt = decrypt(ct,key)
print("Successful Encryption and Decryption: ", message==dt)
