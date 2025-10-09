from Crypto.Util import number
import random


def lcm(x, y):
    from math import gcd
    return x * y // gcd(x, y)

def generate_keypair(bits=512):
    p = number.getPrime(bits)
    q = number.getPrime(bits)
    n = p * q
    g = n + 1
    lam = lcm(p - 1, q - 1)
    mu = pow(lam, -1, n)
    return (n, g), (lam, mu)

def encrypt(pub, m):
    n, g = pub
    while True:
        r = random.randrange(1, n)
        if number.GCD(r, n) == 1:
            break
    c = (pow(g, m, n * n) * pow(r, n, n * n)) % (n * n)
    return c

def decrypt(priv, pub, c):
    lam, mu = priv
    n, g = pub
    x = pow(c, lam, n * n)
    L = (x - 1) // n
    m = (L * mu) % n
    return m

documents = {
    1: "The football match ended with a thrilling goal in the final minute",
    2: "The striker scored a fantastic hat-trick to lead his team to victory",
    3: "The goalkeeper made several incredible saves during the game",
    4: "Fans cheered loudly as the home team took the lead",
    5: "The coach emphasized teamwork and strategy in the post-match interview",
    6: "A red card was issued after a dangerous tackle on the midfielder",
    7: "The championship will be held at the national stadium next week",
    8: "Defenders blocked multiple shots to maintain a clean sheet",
    9: "The midfielder assisted the winning goal with a perfect pass",
    10: "A last-minute penalty secured the championship for the underdogs",
}

def word_to_int(word):
    return abs(hash(word)) % (10**8)

inverted_index = {}
for doc_id, text in documents.items():
    words = text.lower().split()
    for w in words:
        if w not in inverted_index:
            inverted_index[w] = set()
        inverted_index[w].add(doc_id)

print("Original Inverted Index (plain):")
for word in sorted(inverted_index.keys()):
    print(f"{word}: {sorted(inverted_index[word])}")
print()

pub, priv = generate_keypair()

def encrypt_word_deterministic(pub, m):
    n, g = pub
    r = 1  
    c = (pow(g, m, n * n) * pow(r, n, n * n)) % (n * n)
    return c

encrypted_index = {}
for word, doc_ids in inverted_index.items():
    w_int = word_to_int(word)
    enc_word = encrypt_word_deterministic(pub, w_int)
    enc_doc_ids = [encrypt(pub, doc_id) for doc_id in doc_ids]
    encrypted_index[enc_word] = enc_doc_ids

print("Encrypted Index Sample (first 2 entries):")
for i, (enc_w, enc_docs) in enumerate(encrypted_index.items()):
    if i == 2:
        break
    import base64
    enc_w_b64 = base64.b64encode(enc_w.to_bytes((enc_w.bit_length() + 7) // 8, 'big')).decode()
    enc_docs_b64 = [base64.b64encode(c.to_bytes((c.bit_length() + 7) // 8, 'big')).decode() for c in enc_docs]
    print(f"{enc_w_b64} -> {enc_docs_b64}")
print()

def search(query):
    q_int = word_to_int(query)
    enc_q = encrypt_word_deterministic(pub, q_int)
    if enc_q in encrypted_index:
        enc_doc_ids = encrypted_index[enc_q]
        dec_doc_ids = [decrypt(priv, pub, c) for c in enc_doc_ids]
        results = [documents[d] for d in dec_doc_ids]
        return dec_doc_ids, results
    else:
        return [], []

queries = ['goal', 'midfielder', 'penalty', 'coach', 'referee']

for q in queries:
    doc_ids, res = search(q)
    print(f"Documents matching '{q}':")
    if doc_ids:
        for d_id, doc_text in zip(doc_ids, res):
            print(f"Doc {d_id}: {doc_text}")
    else:
        print(f"No documents found for query '{q}'.")
    print()
