letter_to_num = {ch: i for i, ch in enumerate('abcdefghijklmnopqrstuvwxyz')}
num_to_letter = {i: ch for i, ch in enumerate('abcdefghijklmnopqrstuvwxyz')}

def mod_inverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def additive_encrypt(key, plaintext):
    ct = ""
    for ch in plaintext:
        if ch.isalpha():
            is_upper = ch.isupper()
            base = ch.lower()
            ctc_code = (letter_to_num[base] + key) % 26
            ctc = num_to_letter[ctc_code]
            ct += ctc.upper() if is_upper else ctc
        else:
            ct += ch
    return ct

def additive_decrypt(key, ciphertext):
    pt = ""
    for ch in ciphertext:
        if ch.isalpha():
            is_upper = ch.isupper()
            base = ch.lower()
            ptc_code = (letter_to_num[base] - key) % 26
            ptc = num_to_letter[ptc_code]
            pt += ptc.upper() if is_upper else ptc
        else:
            pt += ch
    return pt

def multiplicative_encrypt(key, plaintext):
    ct = ""
    for ch in plaintext:
        if ch.isalpha():
            is_upper = ch.isupper()
            base = ch.lower()
            ctc_code = (letter_to_num[base] * key) % 26
            ctc = num_to_letter[ctc_code]
            ct += ctc.upper() if is_upper else ctc
        else:
            ct += ch
    return ct

def multiplicative_decrypt(key, ciphertext):
    pt = ""
    inv_key = mod_inverse(key)
    if inv_key is None:
        return None
    for ch in ciphertext:
        if ch.isalpha():
            is_upper = ch.isupper()
            base = ch.lower()
            ptc_code = (letter_to_num[base] * inv_key) % 26
            ptc = num_to_letter[ptc_code]
            pt += ptc.upper() if is_upper else ptc
        else:
            pt += ch
    return pt

def affine_encrypt(key_a, key_b, plaintext):
    ct = ""
    for ch in plaintext:
        if ch.isalpha():
            is_upper = ch.isupper()
            base = ch.lower()
            ctc_code = (letter_to_num[base] * key_a + key_b) % 26
            ctc = num_to_letter[ctc_code]
            ct += ctc.upper() if is_upper else ctc
        else:
            ct += ch
    return ct

def affine_decrypt(key_a, key_b, ciphertext):
    pt = ""
    inv_key_a = mod_inverse(key_a)
    if inv_key_a is None:
        return None
    for ch in ciphertext:
        if ch.isalpha():
            is_upper = ch.isupper()
            base = ch.lower()
            ptc_code = (inv_key_a * (letter_to_num[base] - key_b)) % 26
            ptc = num_to_letter[ptc_code]
            pt += ptc.upper() if is_upper else ptc
        else:
            pt += ch
    return pt

def main():
    message = input("Enter original message: ")
    print("Original message:", message)
    plaintext = message
    print("Plaintext (unchanged):", plaintext)

    while True:
        print("\nChoose cipher:")
        print("1. Additive cipher")
        print("2. Multiplicative cipher")
        print("3. Affine cipher")
        print("4. Exit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            try:
                key = int(input("Enter additive key (integer): "))
            except ValueError:
                print("Invalid input. Try again.")
                continue
            ciphertext = additive_encrypt(key, plaintext)
            decrypted = additive_decrypt(key, ciphertext)
            print("Encrypted text:", ciphertext)
            print("Decrypted text:", decrypted)

        elif choice == '2':
            try:
                key = int(input("Enter multiplicative key (integer coprime with 26): "))
                if mod_inverse(key) is None:
                    print("Key is not coprime with 26, no modular inverse. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Try again.")
                continue
            ciphertext = multiplicative_encrypt(key, plaintext)
            decrypted = multiplicative_decrypt(key, ciphertext)
            if decrypted is None:
                print("Error: No modular inverse found. Can't decrypt.")
            else:
                print("Encrypted text:", ciphertext)
                print("Decrypted text:", decrypted)

        elif choice == '3':
            try:
                key_a = int(input("Enter multiplicative key a (coprime with 26): "))
                if mod_inverse(key_a) is None:
                    print("Key a is not coprime with 26, no modular inverse.")
                    continue
                key_b = int(input("Enter additive key b (integer): "))
            except ValueError:
                print("Invalid input.")
                continue
            ciphertext = affine_encrypt(key_a, key_b, plaintext)
            decrypted = affine_decrypt(key_a, key_b, ciphertext)
            if decrypted is None:
                print("Error: No modular inverse found. Can't decrypt.")
            else:
                print("Encrypted text:", ciphertext)
                print("Decrypted text:", decrypted)

        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
