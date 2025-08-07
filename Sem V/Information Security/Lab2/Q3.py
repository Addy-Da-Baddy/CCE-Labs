import time
import matplotlib.pyplot as plt
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad

def aes_encrypt(pt, key):
    key_bytes = key[:32].encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    pt_bytes = pt.encode('utf-8')
    padded_pt = pad(pt_bytes, AES.block_size)
    ct = cipher.encrypt(padded_pt)
    return ct

def aes_decrypt(ct, key):
    key_bytes = key[:32].encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    pt_padded = cipher.decrypt(ct)
    pt = unpad(pt_padded, AES.block_size).decode('utf-8')
    return pt

def des_encrypt(pt, key):
    key_bytes = key[:8].encode('utf-8')  # DES key 8 bytes
    cipher = DES.new(key_bytes, DES.MODE_ECB)
    pt_bytes = pt.encode('utf-8')
    padded_pt = pad(pt_bytes, DES.block_size)
    ct = cipher.encrypt(padded_pt)
    return ct

def des_decrypt(ct, key):
    key_bytes = key[:8].encode('utf-8')
    cipher = DES.new(key_bytes, DES.MODE_ECB)
    pt_padded = cipher.decrypt(ct)
    pt = unpad(pt_padded, DES.block_size).decode('utf-8')
    return pt

def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start, result

def main():
    message = "Performance Testing of Encryption Algorithms"
    aes_key = "0123456789ABCDEF0123456789ABCDEF01234567"
    des_key = "A1B2C3D4"

    aes_enc_time, aes_ct = measure_time(aes_encrypt, message, aes_key)
    aes_dec_time, aes_pt = measure_time(aes_decrypt, aes_ct, aes_key)

    des_enc_time, des_ct = measure_time(des_encrypt, message, des_key)
    des_dec_time, des_pt = measure_time(des_decrypt, des_ct, des_key)

    assert aes_pt == message, "AES decryption failed"
    assert des_pt == message, "DES decryption failed"

    print(f"AES-256 Encryption Time: {aes_enc_time*1000:.4f} ms")
    print(f"AES-256 Decryption Time: {aes_dec_time*1000:.4f} ms")
    print(f"DES Encryption Time: {des_enc_time*1000:.4f} ms")
    print(f"DES Decryption Time: {des_dec_time*1000:.4f} ms")

    labels = ['AES-256', 'DES']
    enc_times = [aes_enc_time*1000, des_enc_time*1000]
    dec_times = [aes_dec_time*1000, des_dec_time*1000]

    x = range(len(labels))

    plt.figure(figsize=(8,5))
    plt.bar(x, enc_times, width=0.4, label='Encryption Time (ms)', align='center')
    plt.bar(x, dec_times, width=0.4, label='Decryption Time (ms)', align='edge')
    plt.xticks(x, labels)
    plt.ylabel('Time (milliseconds)')
    plt.title('AES-256 vs DES Encryption and Decryption Time')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
    #Output:
    #AES-256 Encryption Time: 1.1083 ms
    #AES-256 Decryption Time: 0.0401 ms
    #DES Encryption Time: 0.0556 ms
    #DES Decryption Time: 0.0265 ms
