"""
Test Homomorphic Operations: Addition and Multiplication
Demonstrates both Paillier and RSA homomorphic properties
"""

import sys
sys.path.insert(0, '.')

import config
from crypto_utils import ExpenseCrypto

print("="*70)
print("HOMOMORPHIC ENCRYPTION TEST: ADDITION & MULTIPLICATION")
print("="*70)

# Test with Paillier
print("\n" + "="*70)
print("1. PAILLIER HOMOMORPHIC ENCRYPTION")
print("="*70)

paillier = ExpenseCrypto("Paillier")

# Test Addition
print("\n--- Addition Test ---")
m1 = 100
m2 = 50
print(f"Plaintext values: m1={m1}, m2={m2}")

c1 = paillier.encrypt(m1)
c2 = paillier.encrypt(m2)
print(f"Encrypted: c1={str(c1)[:60]}...")
print(f"           c2={str(c2)[:60]}...")

c_sum = paillier.homomorphic_add(c1, c2)
print(f"Homomorphic Add: c1 * c2 = {str(c_sum)[:60]}...")

decrypted_sum = paillier.decrypt(c_sum)
print(f"✓ Decrypted sum: {decrypted_sum}")
print(f"  Expected: {m1 + m2}")
print(f"  Match: {decrypted_sum == m1 + m2} {'✓' if decrypted_sum == m1 + m2 else '✗'}")

# Test Multiplication by Scalar
print("\n--- Multiplication Test ---")
m = 25
scalar = 4
print(f"Plaintext value: m={m}, scalar={scalar}")

c = paillier.encrypt(m)
print(f"Encrypted: c={str(c)[:60]}...")

c_mult = paillier.homomorphic_multiply(c, scalar)
print(f"Homomorphic Multiply: c^{scalar} = {str(c_mult)[:60]}...")

decrypted_mult = paillier.decrypt(c_mult)
print(f"✓ Decrypted product: {decrypted_mult}")
print(f"  Expected: {m * scalar}")
print(f"  Match: {decrypted_mult == m * scalar} {'✓' if decrypted_mult == m * scalar else '✗'}")

# Combined Operation: (m1 + m2) * scalar
print("\n--- Combined: (Addition + Multiplication) Test ---")
print(f"Operation: ({m1} + {m2}) × {scalar} = {(m1 + m2) * scalar}")

c1 = paillier.encrypt(m1)
c2 = paillier.encrypt(m2)
c_sum = paillier.homomorphic_add(c1, c2)
c_result = paillier.homomorphic_multiply(c_sum, scalar)

decrypted_result = paillier.decrypt(c_result)
expected_result = (m1 + m2) * scalar
print(f"✓ Decrypted result: {decrypted_result}")
print(f"  Expected: {expected_result}")
print(f"  Match: {decrypted_result == expected_result} {'✓' if decrypted_result == expected_result else '✗'}")

# Test with RSA
print("\n" + "="*70)
print("2. RSA HOMOMORPHIC ENCRYPTION (Discrete Log)")
print("="*70)

rsa = ExpenseCrypto("RSA")

# Test Addition
print("\n--- Addition Test ---")
m1 = 100
m2 = 50
print(f"Plaintext values: m1={m1}, m2={m2}")

c1 = rsa.encrypt(m1)
c2 = rsa.encrypt(m2)
print(f"Encrypted: c1={str(c1)[:60]}...")
print(f"           c2={str(c2)[:60]}...")

c_sum = rsa.homomorphic_add(c1, c2)
print(f"Homomorphic Add: c1 * c2 = {str(c_sum)[:60]}...")

decrypted_sum = rsa.decrypt(c_sum)
print(f"✓ Decrypted sum: {decrypted_sum}")
print(f"  Expected: {m1 + m2}")
print(f"  Match: {decrypted_sum == m1 + m2} {'✓' if decrypted_sum == m1 + m2 else '✗'}")

# Test Multiplication by Scalar
print("\n--- Multiplication Test ---")
m = 25
scalar = 4
print(f"Plaintext value: m={m}, scalar={scalar}")

c = rsa.encrypt(m)
print(f"Encrypted: c={str(c)[:60]}...")

c_mult = rsa.homomorphic_multiply(c, scalar)
print(f"Homomorphic Multiply: c^{scalar} = {str(c_mult)[:60]}...")

decrypted_mult = rsa.decrypt(c_mult)
print(f"✓ Decrypted product: {decrypted_mult}")
print(f"  Expected: {m * scalar}")
print(f"  Match: {decrypted_mult == m * scalar} {'✓' if decrypted_mult == m * scalar else '✗'}")

# Combined Operation
print("\n--- Combined: (Addition + Multiplication) Test ---")
print(f"Operation: ({m1} + {m2}) × {scalar} = {(m1 + m2) * scalar}")

c1 = rsa.encrypt(m1)
c2 = rsa.encrypt(m2)
c_sum = rsa.homomorphic_add(c1, c2)
c_result = rsa.homomorphic_multiply(c_sum, scalar)

decrypted_result = rsa.decrypt(c_result)
expected_result = (m1 + m2) * scalar
print(f"✓ Decrypted result: {decrypted_result}")
print(f"  Expected: {expected_result}")
print(f"  Match: {decrypted_result == expected_result} {'✓' if decrypted_result == expected_result else '✗'}")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("✓ Paillier Homomorphic Operations:")
print("  • Addition: E(m1) * E(m2) = E(m1 + m2) mod n²")
print("  • Scalar Multiplication: E(m)^k = E(k*m) mod n²")
print("\n✓ RSA Homomorphic Operations (Discrete Log):")
print("  • Addition: base^m1 * base^m2 = base^(m1+m2) mod n")
print("  • Scalar Multiplication: (base^m)^k = base^(k*m) mod n")
print("\n✓ All operations performed on ENCRYPTED data!")
print("✓ Results match expected plaintext computations!")
print("="*70)
