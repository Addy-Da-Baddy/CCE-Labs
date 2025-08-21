letter_to_num = {ch: i for i, ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
num_to_letter = {i: ch for i, ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def brute_force_affine_keys(pt_pair, ct_pair):
    p0, p1 = letter_to_num[pt_pair[0].upper()], letter_to_num[pt_pair[1].upper()]
    c0, c1 = letter_to_num[ct_pair[0].upper()], letter_to_num[ct_pair[1].upper()]
    for a in range(1, 26):
        if gcd(a, 26) != 1:
            continue
        for b in range(26):
            if (a * p0 + b) % 26 == c0 and (a * p1 + b) % 26 == c1:
                return a, b
    return None, None

def mod_inverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_decrypt(ciphertext, a, b):
    inv_a = mod_inverse(a, 26)
    plaintext = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            c = letter_to_num[ch]
            p = (inv_a * (c - b)) % 26
            plaintext += num_to_letter[p]
        else:
            plaintext += ch
    return plaintext

if __name__ == "__main__":
    plaintext_pair = "AB"
    ciphertext_pair = "GL"
    ciphertext = "XPALASXYFGFUKPXUSOGEUTKCDGEXANMGNV"

    a, b = brute_force_affine_keys(plaintext_pair, ciphertext_pair)
    if a is None:
        print("No valid keys found.")
    else:
        print(f"Found keys: a={a}, b={b}")
        decrypted_text = affine_decrypt(ciphertext, a, b)
        print("Decrypted text:", decrypted_text)
