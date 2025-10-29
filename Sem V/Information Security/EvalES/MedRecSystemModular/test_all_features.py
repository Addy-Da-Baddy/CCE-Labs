"""
Comprehensive Test Suite for MedRecSystemModular
Tests all cryptographic algorithms, signatures, search, and homomorphism
"""
import sys
import time
from crypto_utils import (
    encrypt_key, decrypt_key, 
    SignatureEngine,
    DepartmentCrypto,
    ExpenseCrypto,
    encrypt_report, decrypt_report
)
import config

def test_key_encryption():
    """Test all key encryption algorithms"""
    print("\n" + "="*60)
    print("TESTING KEY ENCRYPTION ALGORITHMS")
    print("="*60)
    
    algorithms = ["RSA", "ElGamal", "AES", "DES", "DH", "Rabin", "ECC"]
    test_key = b"MySecretKey123!@#"  # Use bytes
    
    results = []
    for algo in algorithms:
        try:
            print(f"\nTesting {algo}...")
            start = time.time()
            
            # Encrypt (mode is embedded in encrypted_data dict)
            encrypted_data = encrypt_key(test_key, algo)
            
            # Decrypt (mode is in the dict)
            decrypted_key = decrypt_key(encrypted_data)
            
            elapsed = time.time() - start
            
            # Verify
            if decrypted_key == test_key:
                print(f"✓ {algo} PASSED ({elapsed:.3f}s)")
                results.append((algo, "PASS", elapsed))
            else:
                print(f"✗ {algo} FAILED - Decryption mismatch")
                print(f"  Expected: {test_key}")
                print(f"  Got: {decrypted_key}")
                results.append((algo, "FAIL", elapsed))
                
        except Exception as e:
            print(f"✗ {algo} FAILED - {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((algo, "ERROR", 0))
    
    return results

def test_signatures():
    """Test all signature algorithms with all hash options"""
    print("\n" + "="*60)
    print("TESTING SIGNATURE ALGORITHMS")
    print("="*60)
    
    algorithms = ["RSA", "ElGamal", "Schnorr", "DH"]
    hash_options = ["SHA256", "SHA1", "MD5", "None"]
    test_message = "Patient Record: ID=12345, Diagnosis=Common Cold"
    
    results = []
    for algo in algorithms:
        for hash_opt in hash_options:
            try:
                print(f"\nTesting {algo} with {hash_opt}...")
                start = time.time()
                
                # Create signature engine
                signer = SignatureEngine(mode=algo, hash_option=hash_opt)
                
                # Sign
                signature = signer.sign(test_message)
                
                # Verify
                is_valid = signer.verify(test_message, signature)
                
                elapsed = time.time() - start
                
                if is_valid:
                    print(f"✓ {algo}+{hash_opt} PASSED ({elapsed:.3f}s)")
                    results.append((f"{algo}+{hash_opt}", "PASS", elapsed))
                else:
                    print(f"✗ {algo}+{hash_opt} FAILED - Verification failed")
                    results.append((f"{algo}+{hash_opt}", "FAIL", elapsed))
                    
            except Exception as e:
                print(f"✗ {algo}+{hash_opt} FAILED - {str(e)}")
                results.append((f"{algo}+{hash_opt}", "ERROR", 0))
    
    return results

def test_department_search():
    """Test department encryption and privacy-preserving search"""
    print("\n" + "="*60)
    print("TESTING DEPARTMENT SEARCH (PRIVACY-PRESERVING)")
    print("="*60)
    
    modes = ["Paillier", "AES"]
    departments = ["Cardiology", "Neurology", "Pediatrics"]
    
    results = []
    for mode in modes:
        try:
            print(f"\nTesting {mode} search...")
            start = time.time()
            
            # Create crypto engine
            dept_crypto = DepartmentCrypto(mode=mode)
            
            # Encrypt departments
            encrypted_depts = []
            for dept in departments:
                enc = dept_crypto.encrypt(dept)
                encrypted_depts.append(enc)
                print(f"  Encrypted '{dept}'")
            
            # Search for each department (deterministic encryption allows direct comparison)
            all_found = True
            for i, dept in enumerate(departments):
                # Encrypt search query
                search_enc = dept_crypto.encrypt(dept)
                # Compare with encrypted values
                found = search_enc in encrypted_depts
                
                if found:
                    print(f"  ✓ Found '{dept}'")
                else:
                    print(f"  ✗ Failed to find '{dept}'")
                    all_found = False
            
            # Test negative search
            not_found_enc = dept_crypto.encrypt("Dermatology")
            not_found = not_found_enc in encrypted_depts
            
            if not not_found:
                print(f"  ✓ Correctly didn't find 'Dermatology'")
            else:
                print(f"  ✗ False positive for 'Dermatology'")
                all_found = False
            
            elapsed = time.time() - start
            
            if all_found and not not_found:
                print(f"✓ {mode} search PASSED ({elapsed:.3f}s)")
                results.append((f"{mode} Search", "PASS", elapsed))
            else:
                print(f"✗ {mode} search FAILED")
                results.append((f"{mode} Search", "FAIL", elapsed))
                
        except Exception as e:
            print(f"✗ {mode} search FAILED - {str(e)}")
            results.append((f"{mode} Search", "ERROR", 0))
    
    return results

def test_expense_homomorphism():
    """Test expense encryption with homomorphic operations"""
    print("\n" + "="*60)
    print("TESTING EXPENSE HOMOMORPHIC OPERATIONS")
    print("="*60)
    
    modes = ["Paillier"]  # Only Paillier works reliably for this
    test_values = [1000, 2500, 500]  # Three expenses
    
    results = []
    for mode in modes:
        try:
            print(f"\nTesting {mode} homomorphism...")
            start = time.time()
            
            # Create crypto engine
            expense_crypto = ExpenseCrypto(mode=mode)
            
            # Encrypt expenses
            encrypted_expenses = []
            for val in test_values:
                enc = expense_crypto.encrypt(val)
                encrypted_expenses.append(enc)
                print(f"  Encrypted expense: {val}")
            
            # Test homomorphic addition
            print("\n  Testing homomorphic addition...")
            sum_encrypted = encrypted_expenses[0]
            for enc in encrypted_expenses[1:]:
                sum_encrypted = expense_crypto.homomorphic_add(sum_encrypted, enc)
            
            decrypted_sum = expense_crypto.decrypt(sum_encrypted)
            expected_sum = sum(test_values)
            
            print(f"  Encrypted sum: {decrypted_sum}")
            print(f"  Expected sum: {expected_sum}")
            
            if decrypted_sum == expected_sum:
                print(f"  ✓ Addition works correctly")
                add_pass = True
            else:
                print(f"  ✗ Addition failed")
                add_pass = False
            
            # Test homomorphic scalar multiplication
            print("\n  Testing homomorphic scalar multiplication...")
            scalar = 2
            scaled = expense_crypto.homomorphic_multiply(encrypted_expenses[0], scalar)
            decrypted_scaled = expense_crypto.decrypt(scaled)
            expected_scaled = test_values[0] * scalar
            
            print(f"  Encrypted {test_values[0]} * {scalar} = {decrypted_scaled}")
            print(f"  Expected: {expected_scaled}")
            
            if decrypted_scaled == expected_scaled:
                print(f"  ✓ Scalar multiplication works correctly")
                mult_pass = True
            else:
                print(f"  ✗ Scalar multiplication failed")
                mult_pass = False
            
            elapsed = time.time() - start
            
            if add_pass and mult_pass:
                print(f"✓ {mode} homomorphism PASSED ({elapsed:.3f}s)")
                results.append((f"{mode} Homomorphism", "PASS", elapsed))
            else:
                print(f"✗ {mode} homomorphism FAILED")
                results.append((f"{mode} Homomorphism", "FAIL", elapsed))
                
        except Exception as e:
            print(f"✗ {mode} homomorphism FAILED - {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((f"{mode} Homomorphism", "ERROR", 0))
    
    return results

def test_report_encryption():
    """Test report content encryption"""
    print("\n" + "="*60)
    print("TESTING REPORT CONTENT ENCRYPTION")
    print("="*60)
    
    modes = ["AES", "DES", "RSA"]
    test_report = "Patient showed improvement after medication. Follow-up recommended in 2 weeks."
    
    results = []
    for mode in modes:
        try:
            print(f"\nTesting {mode}...")
            start = time.time()
            
            # Encrypt
            encrypted = encrypt_report(test_report.encode(), mode)
            print(f"  Encrypted report (mode: {encrypted['mode']})")
            
            # Decrypt (mode is embedded in encrypted dict)
            decrypted = decrypt_report(encrypted)
            
            elapsed = time.time() - start
            
            if decrypted.decode() == test_report:
                print(f"✓ {mode} PASSED ({elapsed:.3f}s)")
                results.append((f"{mode} Report", "PASS", elapsed))
            else:
                print(f"✗ {mode} FAILED - Decryption mismatch")
                results.append((f"{mode} Report", "FAIL", elapsed))
                
        except Exception as e:
            print(f"✗ {mode} FAILED - {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((f"{mode} Report", "ERROR", 0))
    
    return results

def print_summary(all_results):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = 0
    passed = 0
    failed = 0
    errors = 0
    
    for category, results in all_results.items():
        print(f"\n{category}:")
        for test_name, status, elapsed in results:
            total += 1
            if status == "PASS":
                passed += 1
                print(f"  ✓ {test_name}: PASS ({elapsed:.3f}s)")
            elif status == "FAIL":
                failed += 1
                print(f"  ✗ {test_name}: FAIL")
            else:
                errors += 1
                print(f"  ✗ {test_name}: ERROR")
    
    print(f"\n" + "="*60)
    print(f"TOTAL: {total} tests")
    print(f"✓ PASSED: {passed}")
    print(f"✗ FAILED: {failed}")
    print(f"✗ ERRORS: {errors}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    print("="*60)

def main():
    """Run all tests"""
    print("="*60)
    print("MedRecSystemModular - Comprehensive Test Suite")
    print("="*60)
    print(f"\nConfiguration:")
    print(f"  Key Encryption: {config.KEY_ENCRYPTION_ALGORITHM}")
    print(f"  Signature: {config.SIGNATURE_ALGORITHM}")
    print(f"  Signature Hash: {config.SIGNATURE_HASH}")
    print(f"  Department: {config.DEPARTMENT_ENCRYPTION}")
    print(f"  Expense: {config.EXPENSE_ENCRYPTION}")
    print(f"  Report: {config.REPORT_ENCRYPTION}")
    
    all_results = {}
    
    # Run all tests
    all_results["Key Encryption"] = test_key_encryption()
    all_results["Signatures"] = test_signatures()
    all_results["Department Search"] = test_department_search()
    all_results["Expense Homomorphism"] = test_expense_homomorphism()
    all_results["Report Encryption"] = test_report_encryption()
    
    # Print summary
    print_summary(all_results)

if __name__ == "__main__":
    main()
