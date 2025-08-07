import time
import matplotlib.pyplot as plt
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

messages = [
    "This a super secret message",
    "This information cannot be leaked anywhere",
    "Consequences will be disastrous if leaked",
    "messi>ronaldo",
    "cope"
]

modes = {
    "ECB": lambda cipher, data: cipher.encrypt(pad(data, cipher.block_size)),
    "CBC": lambda cipher, data: cipher.encrypt(pad(data, cipher.block_size)),
    "CFB": lambda cipher, data: cipher.encrypt(data),
    "OFB": lambda cipher, data: cipher.encrypt(data)
}

def encrypt_des(pt, key, mode_name):
    pt = pt.encode('utf-8')
    key = key[:8].encode('utf-8')
    iv = get_random_bytes(8)

    if mode_name == "ECB":
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode_name == "CBC":
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif mode_name == "CFB":
        cipher = DES.new(key, DES.MODE_CFB, iv)
    elif mode_name == "OFB":
        cipher = DES.new(key, DES.MODE_OFB, iv)

    ct = modes[mode_name](cipher, pt)
    return ct

def encrypt_aes(pt, key, mode_name, key_size):
    pt = pt.encode('utf-8')
    key = key[:key_size].encode('utf-8')
    iv = get_random_bytes(16)

    if mode_name == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode_name == "CBC":
        cipher = AES.new(key, AES.MODE_CBC, iv)
    elif mode_name == "CFB":
        cipher = AES.new(key, AES.MODE_CFB, iv)
    elif mode_name == "OFB":
        cipher = AES.new(key, AES.MODE_OFB, iv)

    ct = modes[mode_name](cipher, pt)
    return ct

def measure_time(func, *args):
    start = time.perf_counter()
    func(*args)
    end = time.perf_counter()
    return (end - start) * 1000  # milliseconds

results = {}

for mode in modes.keys():
    results[mode] = {"DES": 0, "AES-128": 0, "AES-192": 0, "AES-256": 0}
    for msg in messages:
        results[mode]["DES"] += measure_time(encrypt_des, msg, "12345678ABCDEFGH", mode)
        results[mode]["AES-128"] += measure_time(encrypt_aes, msg, "FEDCBA9876543210FEDCBA9876543210", mode, 16)
        results[mode]["AES-192"] += measure_time(encrypt_aes, msg, "FEDCBA9876543210FEDCBA9876543210", mode, 24)
        results[mode]["AES-256"] += measure_time(encrypt_aes, msg, "FEDCBA9876543210FEDCBA9876543210", mode, 32)

labels = list(results.keys())
x = range(len(labels))
width = 0.2

des_times = [results[mode]["DES"] for mode in labels]
aes128_times = [results[mode]["AES-128"] for mode in labels]
aes192_times = [results[mode]["AES-192"] for mode in labels]
aes256_times = [results[mode]["AES-256"] for mode in labels]

plt.figure(figsize=(10, 6))
plt.bar([i - 1.5*width for i in x], des_times, width, label='DES')
plt.bar([i - 0.5*width for i in x], aes128_times, width, label='AES-128')
plt.bar([i + 0.5*width for i in x], aes192_times, width, label='AES-192')
plt.bar([i + 1.5*width for i in x], aes256_times, width, label='AES-256')

plt.xticks(x, labels)
plt.ylabel("Time (ms)")
plt.title("Encryption Time Comparison by Mode and Algorithm")
plt.legend()
plt.tight_layout()
plt.savefig("encryption_time_comparison.png")
plt.show()
