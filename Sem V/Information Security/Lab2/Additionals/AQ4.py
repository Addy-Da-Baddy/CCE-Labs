from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

def encrypt_cbc(message, key, iv):
    print("Plaintext Message:", message)
    data = message.encode('utf-8')
    key = key.encode('utf-8')[:8]
    iv = iv.encode('utf-8')[:8]

    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_data = pad(data, DES.block_size)
    ct = cipher.encrypt(padded_data)

    print("Ciphertext (hex):", ct.hex())
    return ct

def decrypt_cbc(ct, key, iv):
    key = key.encode('utf-8')[:8]
    iv = iv.encode('utf-8')[:8]

    cipher = DES.new(key, DES.MODE_CBC, iv)
    pt_padded = cipher.decrypt(ct)
    pt = unpad(pt_padded, DES.block_size)

    print("Decrypted Plaintext:", pt.decode('utf-8'))
    return pt

key = "A1B2C3D4"
iv = "12345678"
message = "Secure Communication"

ct = encrypt_cbc(message, key, iv)
pt = decrypt_cbc(ct, key, iv)

print("Success:", pt.decode('utf-8') == message)
