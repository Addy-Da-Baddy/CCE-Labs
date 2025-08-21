letter_to_num = {ch: i for i, ch in enumerate('abcdefghijklmnopqrstuvwxyz')}
num_to_letter = {i: ch for i, ch in enumerate('abcdefghijklmnopqrstuvwxyz')}

def vigenere_encrypt(plaintext, keyword):
    plaintext = plaintext.lower()
    keyword = keyword.lower()
    ciphertext = []
    key_len = len(keyword)
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            p = letter_to_num[ch]
            k = letter_to_num[keyword[j % key_len]]
            c = (p + k) % 26
            ciphertext.append(num_to_letter[c])
            j += 1
        else:
            ciphertext.append(ch)
    return ''.join(ciphertext)

message = "Life is full of surprises"
keyword = "HEALTH"

ciphertext = vigenere_encrypt(message, keyword)
print(ciphertext)
