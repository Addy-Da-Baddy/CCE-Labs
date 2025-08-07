from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

def encrypt(hex_data, key):
    print("Hex Input Block: ", hex_data)
    data = bytes.fromhex(hex_data)
    key = key.encode('utf-8')[:8]

    cipher = DES.new(key, DES.MODE_ECB)
    padded_data = pad(data, DES.block_size)
    ct = cipher.encrypt(padded_data)

    print("Ciphertext (hex):", ct.hex())
    return ct

def decrypt(ct, key):
    key = key.encode('utf-8')[:8]
    cipher = DES.new(key, DES.MODE_ECB)

    pt_padded = cipher.decrypt(ct)
    pt = unpad(pt_padded, DES.block_size)

    print("Decrypted Plaintext:", pt.decode('utf-8'))
    return pt

key = "A1B2C3D4E5F60708"

block1 = "54686973206973206120636f6e666964656e7469616c206d657373616765"
block2 = "416e64207468697320697320746865207365636f6e6420626c6f636b"

ct1 = encrypt(block1, key)
ct2 = encrypt(block2, key)

pt1 = decrypt(ct1, key)
pt2 = decrypt(ct2, key)

print("Block 1 Success:", pt1.decode('utf-8') == bytes.fromhex(block1).decode('utf-8'))
print("Block 2 Success:", pt2.decode('utf-8') == bytes.fromhex(block2).decode('utf-8'))
