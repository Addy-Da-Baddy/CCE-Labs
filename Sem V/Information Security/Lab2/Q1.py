from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

def encrypt(message, key):
    print("The Original Message is:", message)

    key_bytes = key.encode('utf-8')
    message_bytes = message.encode('utf-8')

    cipher = DES.new(key_bytes, DES.MODE_ECB)
    padded = pad(message_bytes, DES.block_size)
    ct = cipher.encrypt(padded)

    print("Ciphertext in hexadecimal is:", ct.hex())
    print("Ciphertext as raw bytes:", ct)
    return ct

def decrypt(ct, key):
    key_bytes = key.encode('utf-8')
    cipher = DES.new(key_bytes, DES.MODE_ECB)

    decrypted_padded = cipher.decrypt(ct)
    decrypted = unpad(decrypted_padded, DES.block_size)
    print("Decrypted message is:", decrypted.decode('utf-8'))
    return decrypted.decode('utf-8')

key = "A1B2C3D4"
message = "Confidential Data"

ct = encrypt(message, key)
dt = decrypt(ct, key)

print("Successful Encryption and Decryption: ", message==dt)
