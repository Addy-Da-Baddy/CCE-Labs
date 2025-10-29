"""
Test script for signature hashing options (SHA256 vs No Hash)
Tests all signature algorithms with both hash options
"""

import sys
import config
from crypto_utils import SignatureEngine

def test_signature_with_hash(algorithm, hash_option):
    """Test a signature algorithm with specific hash option"""
    print(f"\n{'='*60}")
    print(f"Testing {algorithm} with {hash_option} hashing")
    print('='*60)
    
    # Create signature engine
    sig_engine = SignatureEngine(algorithm, hash_option)
    
    # Test message
    message = "This is a test medical report for patient ID 12345"
    
    print(f"\n1. Original Message: '{message}'")
    
    # Sign the message
    print("\n2. Signing message...")
    signature = sig_engine.sign(message)
    print(f"   • Signature generated")
    print(f"   • Algorithm: {signature.get('mode')}")
    print(f"   • Hash used: {signature.get('hash')}")
    
    # Verify the signature (should pass)
    print("\n3. Verifying original message...")
    is_valid = sig_engine.verify(message, signature)
    print(f"   • Verification result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    
    # Test with tampered message (should fail)
    tampered_message = message + " TAMPERED"
    print(f"\n4. Testing with tampered message: '{tampered_message}'")
    is_valid_tampered = sig_engine.verify(tampered_message, signature)
    print(f"   • Verification result: {'✗ INVALID (as expected)' if not is_valid_tampered else '✓ VALID (UNEXPECTED!)'}")
    
    # Show results
    if is_valid and not is_valid_tampered:
        print(f"\n✓ {algorithm} with {hash_option} hashing: PASSED")
        return True
    else:
        print(f"\n✗ {algorithm} with {hash_option} hashing: FAILED")
        return False

def main():
    print("\n" + "="*60)
    print("SIGNATURE HASHING TEST SUITE")
    print("="*60)
    print("\nTesting all signature algorithms with SHA256 and No Hash")
    
    # Test all combinations
    algorithms = ["RSA", "ElGamal", "Schnorr"]
    hash_options = ["SHA256", "None"]
    
    results = []
    
    for algo in algorithms:
        for hash_opt in hash_options:
            try:
                passed = test_signature_with_hash(algo, hash_opt)
                results.append((algo, hash_opt, passed))
            except Exception as e:
                print(f"\n✗ Error testing {algo} with {hash_opt}: {e}")
                results.append((algo, hash_opt, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for algo, hash_opt, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {algo:10s} with {hash_opt:7s} hashing")
    
    # Overall result
    all_passed = all(passed for _, _, passed in results)
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("="*60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
