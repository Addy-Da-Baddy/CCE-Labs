def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def additive_cipher(text, key, mode='encrypt'):
    shift = key if mode == 'encrypt' else -key
    return ''.join(chr((ord(c) - 97 + shift) % 26 + 97) for c in text if c.isalpha())

def multiplicative_cipher(text, key, mode='encrypt'):
    inv = modinv(key, 26)
    if mode == 'decrypt' and inv is None:
        raise ValueError(f"Key {key} has no modular inverse mod 26. Choose a coprime key.")
    result = ''
    multiplier = key if mode == 'encrypt' else inv
    for c in text:
        if c.isalpha():
            num = ord(c) - 97
            result += chr((num * multiplier) % 26 + 97)
    return result

def affine_cipher(text, a, b, mode='encrypt'):
    a_inv = modinv(a, 26)
    if mode == 'decrypt' and a_inv is None:
        raise ValueError(f"Key {a} has no modular inverse mod 26. Choose a coprime key.")
    result = ''
    for c in text:
        if c.isalpha():
            x = ord(c) - 97
            if mode == 'encrypt':
                result += chr((a * x + b) % 26 + 97)
            else:
                result += chr((a_inv * (x - b)) % 26 + 97)
    return result

# Input text
original = "iamlearninginformationsecurity"

# Additive Cipher
key_add = 5
enc_add = additive_cipher(original, key_add)
dec_add = additive_cipher(enc_add, key_add, 'decrypt')
print("Additive Cipher")
print("Encrypted:", enc_add)
print("Decrypted:", dec_add)

# Multiplicative Cipher
key_mul = 7
enc_mul = multiplicative_cipher(original, key_mul)
dec_mul = multiplicative_cipher(enc_mul, key_mul, 'decrypt')
print("\nMultiplicative Cipher")
print("Encrypted:", enc_mul)
print("Decrypted:", dec_mul)

# Affine Cipher
key_a = 11
key_b = 6
enc_affine = affine_cipher(original, key_a, key_b)
dec_affine = affine_cipher(enc_affine, key_a, key_b, 'decrypt')
print("\nAffine Cipher")
print("Encrypted:", enc_affine)
print("Decrypted:", dec_affine)
