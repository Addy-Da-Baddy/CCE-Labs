letter_to_num = {ch: i for i, ch in enumerate('abcdefghijklmnopqrstuvwxyz')}
num_to_letter = {i: ch for i, ch in enumerate('abcdefghijklmnopqrstuvwxyz')}

def preprocess_text(text):
    return ''.join(ch.lower() if ch.isalpha() else ch for ch in text)

def vigenere_encrypt(key, plaintext):
    ciphertext = []
    key = key.lower()
    key_len = len(key)
    key_nums = [letter_to_num[k] for k in key]

    j = 0
    for ch in plaintext:
        if ch.isalpha():
            p = letter_to_num[ch]
            k = key_nums[j % key_len]
            c = (p + k) % 26
            ciphertext.append(num_to_letter[c])
            j += 1
        else:
            ciphertext.append(ch)
    return ''.join(ciphertext)

def vigenere_decrypt(key, ciphertext):
    plaintext = []
    key = key.lower()
    key_len = len(key)
    key_nums = [letter_to_num[k] for k in key]

    j = 0
    for ch in ciphertext:
        if ch.isalpha():
            c = letter_to_num[ch]
            k = key_nums[j % key_len]
            p = (c - k) % 26
            plaintext.append(num_to_letter[p])
            j += 1
        else:
            plaintext.append(ch)
    return ''.join(plaintext)

def autokey_encrypt(key, plaintext):
    ciphertext = []
    key = key.lower()
    key_nums = [letter_to_num[k] for k in key]

    extended_key = key_nums + [letter_to_num[ch] for ch in plaintext if ch.isalpha()]
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            p = letter_to_num[ch]
            k = extended_key[j]
            c = (p + k) % 26
            ciphertext.append(num_to_letter[c])
            j += 1
        else:
            ciphertext.append(ch)
    return ''.join(ciphertext)

def autokey_decrypt(key, ciphertext):
    plaintext = []
    key = key.lower()
    key_nums = [letter_to_num[k] for k in key]

    j = 0
    for ch in ciphertext:
        if ch.isalpha():
            c = letter_to_num[ch]
            if j < len(key_nums):
                k = key_nums[j]
            else:
                k = letter_to_num[plaintext[j - len(key_nums)]]
            p = (c - k) % 26
            plaintext.append(num_to_letter[p])
            j += 1
        else:
            plaintext.append(ch)
    return ''.join(plaintext)

# Example usage:
if __name__ == "__main__":
    pt = "HELLO, World!"
    key = "KEY"

    pt_processed = preprocess_text(pt)
    print("Plaintext:", pt)
    print("Processed:", pt_processed)

    # Vigenère
    ct_vig = vigenere_encrypt(key, pt_processed)
    print("Vigenère Encrypted:", ct_vig)
    print("Vigenère Decrypted:", vigenere_decrypt(key, ct_vig))

    # Autokey
    ct_auto = autokey_encrypt(key, pt_processed)
    print("Autokey Encrypted:", ct_auto)
    print("Autokey Decrypted:", autokey_decrypt(key, ct_auto))
