"""
Comprehensive Test Suite for Transaction System Modular Crypto
Tests all encryption algorithms, signature algorithms, and hash options
"""

import sys
import json
from crypto_modular import TransactionCrypto, SignatureEngine

def test_encryption(algorithm):
    """Test transaction encryption algorithm"""
    print(f"\n{'='*60}")
    print(f"Testing {algorithm} Transaction Encryption")
    print('='*60)
    
    try:
        crypto = TransactionCrypto(algorithm)
        
        # Test basic encryption/decryption
        amounts = [100, 250, 50]
        print(f"\nTest amounts: {amounts}")
        
        encrypted = []
        for amount in amounts:
            c = crypto.encrypt(amount)
            encrypted.append(c)
            print(f"  • Encrypt({amount}) = {str(c)[:40]}...")
        
        # Decrypt
        decrypted = []
        for i, c in enumerate(encrypted):
            m = crypto.decrypt(c)
            decrypted.append(m)
            print(f"  • Decrypt(cipher_{i}) = {m}")
        
        # Verify correctness
        match = amounts == decrypted
        print(f"\n  Encryption/Decryption: {'✓ PASS' if match else '✗ FAIL'}")
        
        # Test homomorphic addition
        print(f"\nTesting Homomorphic Addition:")
        c_sum = crypto.homomorphic_add(encrypted[0], encrypted[1])
        m_sum = crypto.decrypt(c_sum)
        expected_sum = amounts[0] + amounts[1]
        print(f"  • E({amounts[0]}) + E({amounts[1]}) = E({m_sum})")
        print(f"  • Expected: {expected_sum}, Got: {m_sum}")
        add_match = (m_sum == expected_sum)
        print(f"  • Homomorphic Add: {'✓ PASS' if add_match else '✗ FAIL'}")
        
        # Test homomorphic multiplication
        print(f"\nTesting Homomorphic Scalar Multiplication:")
        scalar = 3
        c_mult = crypto.homomorphic_multiply(encrypted[2], scalar)
        m_mult = crypto.decrypt(c_mult)
        expected_mult = amounts[2] * scalar
        print(f"  • E({amounts[2]}) × {scalar} = E({m_mult})")
        print(f"  • Expected: {expected_mult}, Got: {m_mult}")
        mult_match = (m_mult == expected_mult)
        print(f"  • Homomorphic Multiply: {'✓ PASS' if mult_match else '✗ FAIL'}")
        
        overall = match and add_match and mult_match
        print(f"\n{'✓ OVERALL PASS' if overall else '✗ OVERALL FAIL'} - {algorithm}")
        return overall
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_signature(sig_algorithm, hash_algorithm):
    """Test signature algorithm with specific hash"""
    print(f"\n{'='*60}")
    print(f"Testing {sig_algorithm} Signature with {hash_algorithm} Hash")
    print('='*60)
    
    try:
        sig_engine = SignatureEngine(sig_algorithm, hash_algorithm)
        
        # Test message
        message = b"Transaction: Seller1 paid 1000 USD"
        print(f"\nMessage: {message.decode()}")
        
        # Sign
        print(f"\nSigning...")
        signature = sig_engine.sign(message)
        print(f"  • Signature generated")
        print(f"  • Algorithm: {signature.get('mode')}")
        print(f"  • Hash: {signature.get('hash')}")
        
        # Verify with correct message
        print(f"\nVerifying with original message...")
        valid = sig_engine.verify(message, signature)
        print(f"  • Verification: {'✓ VALID' if valid else '✗ INVALID'}")
        
        # Verify with tampered message
        tampered = message + b" TAMPERED"
        print(f"\nVerifying with tampered message...")
        invalid = sig_engine.verify(tampered, signature)
        print(f"  • Verification: {'✗ INVALID (expected)' if not invalid else '✓ VALID (UNEXPECTED!)'}")
        
        overall = valid and not invalid
        print(f"\n{'✓ OVERALL PASS' if overall else '✗ OVERALL FAIL'} - {sig_algorithm} with {hash_algorithm}")
        return overall
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*60)
    print("TRANSACTION SYSTEM - COMPREHENSIVE CRYPTO TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test all encryption algorithms
    print("\n" + "="*60)
    print("PART 1: TRANSACTION ENCRYPTION ALGORITHMS")
    print("="*60)
    
    encryption_algos = ["Paillier", "RSA", "DH", "Rabin", "ECC"]
    for algo in encryption_algos:
        passed = test_encryption(algo)
        results.append(("Encryption", algo, "", passed))
    
    # Test all signature algorithms with all hash options
    print("\n\n" + "="*60)
    print("PART 2: DIGITAL SIGNATURE ALGORITHMS")
    print("="*60)
    
    signature_algos = ["RSA", "ElGamal", "Schnorr", "DH"]
    hash_options = ["SHA256", "SHA1", "MD5", "None"]
    
    for sig_algo in signature_algos:
        for hash_opt in hash_options:
            passed = test_signature(sig_algo, hash_opt)
            results.append(("Signature", sig_algo, hash_opt, passed))
    
    # Summary
    print("\n\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    print("\nEncryption Algorithms:")
    for test_type, algo, hash_opt, passed in results:
        if test_type == "Encryption":
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status} - {algo}")
    
    print("\nSignature Algorithms:")
    for test_type, algo, hash_opt, passed in results:
        if test_type == "Signature":
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status} - {algo:10s} with {hash_opt:7s} hash")
    
    # Overall result
    all_passed = all(passed for _, _, _, passed in results)
    total = len(results)
    passed_count = sum(1 for _, _, _, passed in results if passed)
    
    print("\n" + "="*60)
    print(f"Results: {passed_count}/{total} tests passed")
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print(f"✗ {total - passed_count} TESTS FAILED")
    print("="*60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
