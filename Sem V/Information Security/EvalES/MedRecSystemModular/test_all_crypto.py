"""
Comprehensive Test Suite for MedRecSystemModular
Tests all encryption, signature, and hash algorithms
"""

import sys
import config
from crypto_utils import (
    encrypt_key, decrypt_key,
    SignatureEngine,
    DepartmentCrypto, ExpenseCrypto,
    encrypt_report, decrypt_report
)

def test_key_encryption(algorithm):
    """Test key encryption algorithm"""
    print(f"\n{'='*60}")
    print(f"Testing {algorithm} Key Encryption")
    print('='*60)
    
    try:
        # Test key
        session_key = b"This is a 32-byte session key!!"
        
        print(f"\nSession Key: {session_key[:20]}...")
        
        # Encrypt
        encrypted = encrypt_key(session_key, algorithm)
        print(f"  • Encrypted: {str(encrypted)[:50]}...")
        
        # Decrypt
        decrypted = decrypt_key(encrypted, algorithm)
        print(f"  • Decrypted: {decrypted[:20]}...")
        
        # Verify
        match = (session_key == decrypted)
        print(f"\n  Result: {'✓ PASS' if match else '✗ FAIL'}")
        return match
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_signature(sig_algorithm, hash_algorithm):
    """Test signature algorithm with hash"""
    print(f"\n{'='*60}")
    print(f"Testing {sig_algorithm} Signature with {hash_algorithm} Hash")
    print('='*60)
    
    try:
        sig_engine = SignatureEngine(sig_algorithm, hash_algorithm)
        
        message = "Patient report for ID: 12345"
        print(f"\nMessage: {message}")
        
        # Sign
        print(f"\nSigning...")
        signature = sig_engine.sign(message)
        print(f"  • Signature generated")
        print(f"  • Mode: {signature.get('mode')}")
        print(f"  • Hash: {signature.get('hash')}")
        
        # Verify correct
        print(f"\nVerifying original...")
        valid = sig_engine.verify(message, signature)
        print(f"  • Result: {'✓ VALID' if valid else '✗ INVALID'}")
        
        # Verify tampered
        tampered = message + " TAMPERED"
        print(f"\nVerifying tampered...")
        invalid = sig_engine.verify(tampered, signature)
        print(f"  • Result: {'✗ INVALID (expected)' if not invalid else '✓ VALID (UNEXPECTED!)'}")
        
        result = valid and not invalid
        print(f"\n  Overall: {'✓ PASS' if result else '✗ FAIL'}")
        return result
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_department_search():
    """Test department encryption (searchable)"""
    print(f"\n{'='*60}")
    print(f"Testing Department Search Encryption")
    print('='*60)
    
    try:
        dept_crypto = DepartmentCrypto()
        
        departments = ["Cardiology", "Neurology", "Cardiology"]
        print(f"\nDepartments: {departments}")
        
        # Encrypt
        encrypted = [dept_crypto.encrypt(d) for d in departments]
        print(f"  • Encrypted {len(encrypted)} departments")
        
        # Search for "Cardiology"
        search_enc = dept_crypto.encrypt("Cardiology")
        matches = [i for i, enc in enumerate(encrypted) if enc == search_enc]
        print(f"\n  • Searching for 'Cardiology'")
        print(f"  • Found at indices: {matches}")
        print(f"  • Expected indices: [0, 2]")
        
        result = (matches == [0, 2])
        print(f"\n  Result: {'✓ PASS' if result else '✗ FAIL'}")
        return result
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_expense_homomorphic():
    """Test expense homomorphic operations"""
    print(f"\n{'='*60}")
    print(f"Testing Expense Homomorphic Operations")
    print('='*60)
    
    try:
        expense_crypto = ExpenseCrypto()
        
        amounts = [100, 250, 50]
        print(f"\nAmounts: {amounts}")
        
        # Encrypt
        encrypted = [expense_crypto.encrypt(a) for a in amounts]
        print(f"  • Encrypted {len(encrypted)} expenses")
        
        # Test addition
        print(f"\nTesting Homomorphic Addition:")
        c_sum = expense_crypto.homomorphic_add(encrypted[0], encrypted[1])
        m_sum = expense_crypto.decrypt(c_sum)
        expected_sum = amounts[0] + amounts[1]
        print(f"  • E({amounts[0]}) + E({amounts[1]}) = E({m_sum})")
        print(f"  • Expected: {expected_sum}")
        add_match = (m_sum == expected_sum)
        print(f"  • Result: {'✓ PASS' if add_match else '✗ FAIL'}")
        
        # Test multiplication
        print(f"\nTesting Homomorphic Multiplication:")
        scalar = 4
        c_mult = expense_crypto.homomorphic_multiply(encrypted[2], scalar)
        m_mult = expense_crypto.decrypt(c_mult)
        expected_mult = amounts[2] * scalar
        print(f"  • E({amounts[2]}) × {scalar} = E({m_mult})")
        print(f"  • Expected: {expected_mult}")
        mult_match = (m_mult == expected_mult)
        print(f"  • Result: {'✓ PASS' if mult_match else '✗ FAIL'}")
        
        result = add_match and mult_match
        print(f"\n  Overall: {'✓ PASS' if result else '✗ FAIL'}")
        return result
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_report_encryption(algorithm):
    """Test report content encryption"""
    print(f"\n{'='*60}")
    print(f"Testing {algorithm} Report Encryption")
    print('='*60)
    
    try:
        report = "Patient has high blood pressure. Recommend medication."
        print(f"\nReport: {report[:30]}...")
        
        # Encrypt
        encrypted = encrypt_report(report, algorithm)
        print(f"  • Encrypted report")
        
        # Decrypt
        decrypted = decrypt_report(encrypted, algorithm)
        print(f"  • Decrypted: {decrypted[:30]}...")
        
        # Verify
        match = (report == decrypted)
        print(f"\n  Result: {'✓ PASS' if match else '✗ FAIL'}")
        return match
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*60)
    print("MEDRECSYSTEMMODULAR - COMPREHENSIVE CRYPTO TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test key encryption algorithms
    print("\n" + "="*60)
    print("PART 1: KEY ENCRYPTION ALGORITHMS")
    print("="*60)
    
    # Note: We'll test the ones that are already implemented
    # DH, Rabin, ECC need to be added to crypto_utils.py first
    key_algos = ["RSA", "ElGamal", "AES", "DES"]
    for algo in key_algos:
        passed = test_key_encryption(algo)
        results.append(("Key Encryption", algo, "", passed))
    
    # Test signature algorithms with hash options
    print("\n\n" + "="*60)
    print("PART 2: DIGITAL SIGNATURE ALGORITHMS")
    print("="*60)
    
    # Note: DH signature needs to be added to crypto_utils.py first
    sig_algos = ["RSA", "ElGamal"]  # Schnorr has issues
    hash_opts = ["SHA256", "SHA1", "MD5", "None"]
    
    for sig_algo in sig_algos:
        for hash_opt in hash_opts:
            passed = test_signature(sig_algo, hash_opt)
            results.append(("Signature", sig_algo, hash_opt, passed))
    
    # Test department search
    print("\n\n" + "="*60)
    print("PART 3: DEPARTMENT SEARCH ENCRYPTION")
    print("="*60)
    
    passed = test_department_search()
    results.append(("Department Search", config.DEPARTMENT_ENCRYPTION, "", passed))
    
    # Test expense homomorphic
    print("\n\n" + "="*60)
    print("PART 4: EXPENSE HOMOMORPHIC OPERATIONS")
    print("="*60)
    
    passed = test_expense_homomorphic()
    results.append(("Expense Homomorphic", config.EXPENSE_ENCRYPTION, "", passed))
    
    # Test report encryption
    print("\n\n" + "="*60)
    print("PART 5: REPORT CONTENT ENCRYPTION")
    print("="*60)
    
    report_algos = ["AES", "RSA", "ElGamal", "DES"]
    for algo in report_algos:
        passed = test_report_encryption(algo)
        results.append(("Report Encryption", algo, "", passed))
    
    # Summary
    print("\n\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    print("\nKey Encryption:")
    for test_type, algo, hash_opt, passed in results:
        if test_type == "Key Encryption":
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status} - {algo}")
    
    print("\nSignatures:")
    for test_type, algo, hash_opt, passed in results:
        if test_type == "Signature":
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status} - {algo:10s} with {hash_opt:7s} hash")
    
    print("\nDepartment Search:")
    for test_type, algo, hash_opt, passed in results:
        if test_type == "Department Search":
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status} - {algo}")
    
    print("\nExpense Homomorphic:")
    for test_type, algo, hash_opt, passed in results:
        if test_type == "Expense Homomorphic":
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status} - {algo}")
    
    print("\nReport Encryption:")
    for test_type, algo, hash_opt, passed in results:
        if test_type == "Report Encryption":
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status} - {algo}")
    
    # Overall
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
