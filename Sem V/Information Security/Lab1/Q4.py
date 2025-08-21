import numpy as np
import string

letter_to_num = {ch: i for i, ch in enumerate(string.ascii_uppercase)}
num_to_letter = {i: ch for i, ch in enumerate(string.ascii_uppercase)}


def preprocess_text(text):

    text = text.upper()
    filtered = [ch for ch in text if ch in string.ascii_uppercase]
    if len(filtered) % 2 != 0:
        filtered.append('X')
    return filtered


def hill_encrypt(text, key_matrix):
    text_nums = [letter_to_num[ch] for ch in text]
    ciphertext = []

    for i in range(0, len(text_nums), 2):
        pair = np.array([[text_nums[i]], [text_nums[i + 1]]])
        encrypted_pair = np.dot(key_matrix, pair) % 26
        ciphertext.append(num_to_letter[encrypted_pair[0, 0]])
        ciphertext.append(num_to_letter[encrypted_pair[1, 0]])

    return ''.join(ciphertext)


message = "We live in an insecure world"
key = np.array([[3, 3],
                [2, 7]])

processed_text = preprocess_text(message)

encrypted_message = hill_encrypt(processed_text, key)

print("Original message:", message)
print("Processed text (letters only, padded):", ''.join(processed_text))
print("Encrypted message:", encrypted_message)
