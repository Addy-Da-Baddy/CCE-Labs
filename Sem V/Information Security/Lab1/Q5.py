def letter_to_num(ch):
    return ord(ch.lower()) - ord('a')

def num_to_letter(n):
    return chr(n + ord('a'))

def find_shift_key(plaintext, ciphertext):
    p = letter_to_num(plaintext[0])
    c = letter_to_num(ciphertext[0])
    key = (c - p) % 26
    return key

def decrypt_shift(ciphertext, key):
    plaintext = ""
    for ch in ciphertext:
        if ch.isalpha():
            c = letter_to_num(ch)
            p = (c - key) % 26
            plaintext += num_to_letter(p)
        else:
            plaintext += ch
    return plaintext

known_plaintext = "yes"
known_ciphertext = "CIW"
unknown_ciphertext = "XVIEWYWI"

key = find_shift_key(known_plaintext, known_ciphertext)
print(f"Found shift key: {key}")

decrypted = decrypt_shift(unknown_ciphertext, key)
print(f"Decrypted message: {decrypted}")

print("Type of attack: Known plaintext attack")
