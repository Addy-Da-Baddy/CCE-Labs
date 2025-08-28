import time
import string
import matplotlib.pyplot as plt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes



class PlayfairCipher:
    def __init__(self, keyword):
        self.keyword = keyword.upper()
        self.matrix = self.generate_matrix(self.keyword)

    def generate_matrix(self, keyword):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        seen = set()
        matrix = []

        # Add unique letters from keyword first
        for char in keyword:
            if char not in seen and char in alphabet:
                seen.add(char)
                matrix.append(char)

        for char in alphabet:
            if char not in seen:
                seen.add(char)
                matrix.append(char)

        matrix_5x5 = [matrix[i * 5:(i + 1) * 5] for i in range(5)]
        return matrix_5x5

    def format_text(self, text):
        text = text.upper().replace('J', 'I')
        text = ''.join(filter(lambda x: x in string.ascii_uppercase, text))

        i = 0
        pairs = []
        while i < len(text):
            a = text[i]
            b = ''
            if i + 1 < len(text):
                b = text[i + 1]
            else:
                b = 'X'

            if a == b:
                pairs.append(a + 'X')
                i += 1
            else:
                pairs.append(a + b)
                i += 2

        return pairs

    def find_position(self, char):
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if c == char:
                    return (i, j)
        return None

    def encrypt_pair(self, a, b):
        r1, c1 = self.find_position(a)
        r2, c2 = self.find_position(b)

        if r1 == r2:
            c1 = (c1 + 1) % 5
            c2 = (c2 + 1) % 5
        elif c1 == c2:
            r1 = (r1 + 1) % 5
            r2 = (r2 + 1) % 5
        else:
            c1, c2 = c2, c1

        return self.matrix[r1][c1] + self.matrix[r2][c2]

    def encrypt(self, plaintext):
        pairs = self.format_text(plaintext)
        ciphertext = ""
        for pair in pairs:
            ciphertext += self.encrypt_pair(pair[0], pair[1])
        return ciphertext




def generate_rsa_keypair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def rsa_encrypt(public_key_bytes, data_bytes):
    public_key = RSA.import_key(public_key_bytes)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(data_bytes)
    return encrypted


def rsa_decrypt(private_key_bytes, encrypted_bytes):
    private_key = RSA.import_key(private_key_bytes)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(encrypted_bytes)
    return decrypted



def aes_encrypt(key, plaintext):
    key_bytes = bytes.fromhex(key)
    cipher = AES.new(key_bytes, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes


def aes_decrypt(key, ciphertext):
    key_bytes = bytes.fromhex(key)
    iv = ciphertext[:16]
    ct = ciphertext[16:]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()



def main():
    print("=== Playfair Cipher ===")
    playfair = PlayfairCipher("POTATO")
    msg1 = "The key is hidden under the door pad"
    start_pf = time.time()
    pf_ciphertext = playfair.encrypt(msg1)
    end_pf = time.time()
    print(f"Original message: {msg1}")
    print(f"Encrypted with Playfair: {pf_ciphertext}")
    playfair_time = end_pf - start_pf

    print("\n=== RSA Key Generation for Encoder and Decoder ===")
    encoder_priv, encoder_pub = generate_rsa_keypair()
    decoder_priv, decoder_pub = generate_rsa_keypair()
    print("RSA keys generated for encoder and decoder.")

    aes_key = b'0123456789ABCDEF0123456789ABCDEF'
    print(f"AES key (hex): {aes_key.decode()}")

    encrypted_aes_key = rsa_encrypt(decoder_pub, aes_key)
    print("AES key encrypted with decoder's public key.")

    decrypted_aes_key = rsa_decrypt(decoder_priv, encrypted_aes_key)
    print(f"AES key decrypted by decoder: {decrypted_aes_key.decode()}")

    assert aes_key == decrypted_aes_key, "AES key decryption failed!"

    print("\n=== AES-128 Encryption/Decryption ===")
    msg2 = "Information Security Lab Evaluation One"
    aes_key_hex = "0123456789ABCDEF0123456789ABCDEF"

    start_aes = time.time()
    aes_encrypted = aes_encrypt(aes_key_hex, msg2)
    end_aes_enc = time.time()
    aes_decryption = aes_decrypt(aes_key_hex, aes_encrypted)
    end_aes_dec = time.time()

    print(f"Original message: {msg2}")
    print(f"Encrypted (hex): {aes_encrypted.hex()}")
    print(f"Decrypted message: {aes_decryption}")

    aes_enc_time = end_aes_enc - start_aes
    aes_dec_time = end_aes_dec - end_aes_enc


    methods = ['Playfair', 'AES-128']
    times = [playfair_time, aes_enc_time]

    plt.bar(methods, times, color=['blue', 'green'])
    plt.ylabel('Encryption Time (seconds)')
    plt.title('Encryption Time Comparison: Playfair vs AES-128')
    for i, v in enumerate(times):
        plt.text(i, v + 0.0001, f"{v:.6f}", ha='center')
    plt.show()

    print(f"Playfair encryption time: {playfair_time:.6f} seconds")
    print(f"AES-128 encryption time: {aes_enc_time:.6f} seconds")
    print(f"AES-128 decryption time: {aes_dec_time:.6f} seconds")


if __name__ == "__main__":
    main()
