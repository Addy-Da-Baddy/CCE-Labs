"""
Test Homomorphic Encryption for Both Paillier and RSA
"""

import sys
sys.path.insert(0, '.')

import config
from crypto_utils import ExpenseCrypto

def test_paillier():
    print("\n" + "="*60)
    print("TESTING PAILLIER HOMOMORPHIC ENCRYPTION")
    print("="*60)
    
    expense_crypto = ExpenseCrypto("Paillier")
    
    # Test values
    m1 = 100
    m2 = 50
    m3 = 25
    
    print(f"\nOriginal values: {m1}, {m2}, {m3}")
    print(f"Expected sum: {m1 + m2 + m3} = {sum([m1, m2, m3])}")
    
    # Encrypt
    c1 = expense_crypto.encrypt(m1)
    c2 = expense_crypto.encrypt(m2)
    c3 = expense_crypto.encrypt(m3)
    
    print(f"\nEncrypted values:")
    print(f"  E({m1}) = {str(c1)[:60]}...")
    print(f"  E({m2}) = {str(c2)[:60]}...")
    print(f"  E({m3}) = {str(c3)[:60]}...")
    
    # Homomorphic addition
    c_sum = expense_crypto.homomorphic_add(c1, c2)
    c_sum = expense_crypto.homomorphic_add(c_sum, c3)
    
    print(f"\nHomomorphic sum: {str(c_sum)[:60]}...")
    
    # Decrypt
    result = expense_crypto.decrypt(c_sum)
    print(f"\nDecrypted sum: {result}")
    
    if result == m1 + m2 + m3:
        print("✅ PAILLIER TEST PASSED!")
    else:
        print(f"❌ PAILLIER TEST FAILED! Expected {m1 + m2 + m3}, got {result}")
    
    return result == m1 + m2 + m3

def test_rsa():
    print("\n" + "="*60)
    print("TESTING RSA HOMOMORPHIC ENCRYPTION (Discrete Log)")
    print("="*60)
    
    expense_crypto = ExpenseCrypto("RSA")
    
    # Test values (smaller for RSA discrete log)
    m1 = 100
    m2 = 50
    m3 = 25
    
    print(f"\nOriginal values: {m1}, {m2}, {m3}")
    print(f"Expected sum: {m1 + m2 + m3} = {sum([m1, m2, m3])}")
    
    # Encrypt
    c1 = expense_crypto.encrypt(m1)
    c2 = expense_crypto.encrypt(m2)
    c3 = expense_crypto.encrypt(m3)
    
    print(f"\nEncrypted values (base^amount):")
    print(f"  E({m1}) = 3^{m1} mod n = {str(c1)[:60]}...")
    print(f"  E({m2}) = 3^{m2} mod n = {str(c2)[:60]}...")
    print(f"  E({m3}) = 3^{m3} mod n = {str(c3)[:60]}...")
    
    # Homomorphic addition (multiplication in exponent)
    c_sum = expense_crypto.homomorphic_add(c1, c2)
    c_sum = expense_crypto.homomorphic_add(c_sum, c3)
    
    print(f"\nHomomorphic sum: {str(c_sum)[:60]}...")
    print("  (This is 3^({m1}+{m2}+{m3}) mod n = 3^{sum} mod n)")
    
    # Decrypt (compute discrete log)
    print("\nComputing discrete log (this may take a moment)...")
    result = expense_crypto.decrypt(c_sum)
    print(f"Decrypted sum: {result}")
    
    if result == m1 + m2 + m3:
        print("✅ RSA TEST PASSED!")
    else:
        print(f"❌ RSA TEST FAILED! Expected {m1 + m2 + m3}, got {result}")
    
    return result == m1 + m2 + m3

if __name__ == "__main__":
    print("\n🔬 HOMOMORPHIC ENCRYPTION TEST SUITE")
    print("Testing both Paillier and RSA implementations")
    
    paillier_ok = test_paillier()
    rsa_ok = test_rsa()
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    print(f"Paillier: {'✅ PASS' if paillier_ok else '❌ FAIL'}")
    print(f"RSA:      {'✅ PASS' if rsa_ok else '❌ FAIL'}")
    
    if paillier_ok and rsa_ok:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n⚠️  Some tests failed. Check implementation.")
