from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

documents = {
    1: "the football match ended with a thrilling goal in the final minute",
    2: "the striker scored a hat-trick to lead his team to victory",
    3: "the goalkeeper made several incredible saves during the game",
    4: "fans cheered loudly as the home team took the lead",
    5: "the coach emphasized teamwork and strategy in the post-match interview",
    6: "a red card was issued after a dangerous tackle on the midfielder",
    7: "the championship final will be held at the national stadium next week",
    8: "defenders blocked multiple shots to maintain a clean sheet",
    9: "the midfielder assisted the winning goal with a perfect pass",
    10: "a last-minute penalty secured the championship for the underdogs"
}

key = get_random_bytes(16)  

fixed_iv = b'\x00' * 16

def encrypt(text, fixed=False):
    if fixed:
        cipher = AES.new(key, AES.MODE_CBC, iv=fixed_iv)
    else:
        cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ":" + ct

def decrypt(enc_text):
    iv, ct = enc_text.split(":")
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

inverted_index = {}

for doc_id, text in documents.items():
    words = text.lower().split()
    for word in words:
        if word not in inverted_index:
            inverted_index[word] = set()
        inverted_index[word].add(doc_id)

for word in inverted_index:
    inverted_index[word] = sorted(list(inverted_index[word]))

print("Original Inverted Index (plain):")
for k, v in inverted_index.items():
    print(f"{k}: {v}")

encrypted_index = {}

for word, doc_ids in inverted_index.items():
    enc_word = encrypt(word, fixed=True) 
    enc_doc_ids = encrypt(",".join(map(str, doc_ids)), fixed=False)
    encrypted_index[enc_word] = enc_doc_ids

print("\nEncrypted Index Sample (first 2 entries):")
sample = list(encrypted_index.items())[:2]
for k, v in sample:
    print(f"{k} -> {v}")

def search(query):
    enc_query = encrypt(query.lower(), fixed=True)
    results_enc = encrypted_index.get(enc_query, None)
    if results_enc is None:
        print(f"No documents found for query '{query}'.\n")
        return
    
    doc_ids_str = decrypt(results_enc)
    doc_ids = list(map(int, doc_ids_str.split(",")))
    print(f"Documents matching '{query}':")
    for doc_id in doc_ids:
        print(f"Doc {doc_id}: {documents[doc_id]}")
    print()

search("goal")
search("midfielder")
search("penalty")
search("coach")
search("referee") 
