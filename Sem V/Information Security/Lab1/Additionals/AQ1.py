letter_to_num = {ch: i for i, ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
num_to_letter = {i: ch for i, ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}

def additive_decrypt(ciphertext, key):
    plaintext = ""
    for ch in ciphertext:
        if ch.isalpha():
            c = letter_to_num[ch.upper()]
            p = (c - key) % 26
            if ch.isupper():
                plaintext += num_to_letter[p]
            else:
                plaintext += num_to_letter[p].lower()
        else:
            plaintext += ch
    return plaintext

ciphertext = "NCJAEZRCLAS/LYODEPRLYZRCLASJLCPEHZDTOPDZOLN&BY"

print("Trying keys near 13 (8 to 18):\n")
for key in range(8, 19):
    decrypted = additive_decrypt(ciphertext, key)
    print(f"Key = {key}:")
    print(decrypted)
    print()
