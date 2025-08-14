import time
from Crypto.Util.number import getPrime, getRandomRange, inverse

KEY_SIZE = 2048 

def generate_dh_parameters():
    p = getPrime(KEY_SIZE)           
    g = 2                             
    return p, g

def generate_peer_keys(p, g):
    private_key = getRandomRange(2, p - 2)
    public_key = pow(g, private_key, p)
    return private_key, public_key

def compute_shared_secret(peer_private, other_public, p):
    return pow(other_public, peer_private, p)

def run_diffie_hellman():
    print("Starting Diffie-Hellman Key Exchange...\n")

    start = time.time()
    p, g = generate_dh_parameters()
    param_time = time.time() - start
    print(f"Global parameter generation time: {param_time:.4f} sec")

    start = time.time()
    a_private, a_public = generate_peer_keys(p, g)
    a_time = time.time() - start
    print(f"Peer A key generation time: {a_time:.4f} sec")

    start = time.time()
    b_private, b_public = generate_peer_keys(p, g)
    b_time = time.time() - start
    print(f"Peer B key generation time: {b_time:.4f} sec")

    start = time.time()
    shared_a = compute_shared_secret(a_private, b_public, p)
    shared_b = compute_shared_secret(b_private, a_public, p)
    exchange_time = time.time() - start
    print(f"Key exchange time: {exchange_time:.4f} sec")

    print("\n Shared secret match:", shared_a == shared_b)

if __name__ == "__main__":
    run_diffie_hellman()
