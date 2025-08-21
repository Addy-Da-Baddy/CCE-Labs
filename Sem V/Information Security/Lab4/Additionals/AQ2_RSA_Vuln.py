from Crypto.Util.number import inverse, isPrime, long_to_bytes
import math

# Vulnerable RSA key generation example with small primes
def generate_weak_rsa_keys():
    # small primes (insecure)
    p = 2851  # should be large prime in real RSA
    q = 3253
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = inverse(e, phi)
    return (n, e, d, p, q)

# Attack: Factor n by simple trial division (because p,q are small)
def factor_n(n):
    # Try dividing n by all integers up to sqrt(n)
    limit = int(math.isqrt(n)) + 1
    for i in range(2, limit):
        if n % i == 0:
            return i, n // i
    return None, None

def recover_private_key(n, e):
    print(f"Attempting to factor n={n}...")
    p, q = factor_n(n)
    if p is None or q is None:
        print("Failed to factor n.")
        return None
    print(f"Found factors p={p}, q={q}")

    phi = (p - 1) * (q - 1)
    try:
        d = inverse(e, phi)
    except ValueError:
        print("Modular inverse does not exist, failed to compute d.")
        return None

    print(f"Recovered private exponent d={d}")
    return (p, q, d)

def demo_attack():
    n, e, d, p_real, q_real = generate_weak_rsa_keys()
    print(f"Original private exponent d={d}")
    print(f"Public key (n={n}, e={e})")

    recovered = recover_private_key(n, e)
    if recovered:
        p, q, d_recovered = recovered
        assert p == p_real and q == q_real, "Recovered primes do not match original!"
        assert d == d_recovered, "Recovered private exponent does not match original!"
        print("Attack successful: private key recovered from weak RSA modulus.")

if __name__ == "__main__":
    demo_attack()
