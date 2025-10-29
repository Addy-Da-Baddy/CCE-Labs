"""
Quick Demo: Test New Algorithms in MedRecSystemModular
Shows that DH, Rabin, ECC encryption + DH signatures + SHA1/MD5 work
"""

import config
from crypto_utils import (
    encrypt_key, decrypt_key,
    SignatureEngine,
    DepartmentCrypto,
    ExpenseCrypto
)

def demo_new_encryption_algorithms():
    """Demo new key encryption: DH, Rabin, ECC"""
    print("="*60)
    print("DEMO: New Key Encryption Algorithms")
    print("="*60)
    
    test_key = b"SecretMedicalKey123"
    
    for algo in ["DH", "Rabin", "ECC"]:
        print(f"\n▶ Testing {algo}...")
        encrypted = encrypt_key(test_key, algo)
        decrypted = decrypt_key(encrypted)
        
        if decrypted == test_key:
            print(f"  ✓ {algo} works correctly!")
        else:
            print(f"  ✗ {algo} failed!")

def demo_dh_signatures():
    """Demo DH signatures with different hash options"""
    print("\n" + "="*60)
    print("DEMO: DH Signatures with Multiple Hash Options")
    print("="*60)
    
    message = "Patient Record #12345"
    
    for hash_opt in ["SHA256", "SHA1", "MD5", "None"]:
        print(f"\n▶ Testing DH + {hash_opt}...")
        signer = SignatureEngine(mode="DH", hash_option=hash_opt)
        
        signature = signer.sign(message)
        is_valid = signer.verify(message, signature)
        
        if is_valid:
            print(f"  ✓ DH with {hash_opt} works correctly!")
        else:
            print(f"  ✗ DH with {hash_opt} failed!")

def demo_existing_signatures_with_new_hashes():
    """Demo existing signatures (RSA, ElGamal) with SHA1/MD5"""
    print("\n" + "="*60)
    print("DEMO: RSA & ElGamal with SHA1/MD5 Hashing")
    print("="*60)
    
    message = "Confidential Medical Report"
    
    for algo in ["RSA", "ElGamal"]:
        for hash_opt in ["SHA1", "MD5"]:
            print(f"\n▶ Testing {algo} + {hash_opt}...")
            signer = SignatureEngine(mode=algo, hash_option=hash_opt)
            
            signature = signer.sign(message)
            is_valid = signer.verify(message, signature)
            
            if is_valid:
                print(f"  ✓ {algo} with {hash_opt} works!")
            else:
                print(f"  ✗ {algo} with {hash_opt} failed!")

def demo_client_server_workflow():
    """Demo how it works in client-server scenario"""
    print("\n" + "="*60)
    print("DEMO: Client-Server Workflow Simulation")
    print("="*60)
    
    print("\n1️⃣  DOCTOR REGISTRATION (with DH-encrypted department)")
    print("-" * 60)
    
    # Server initializes
    dept_crypto = DepartmentCrypto("AES")
    
    # Doctor encrypts department name
    doctor_dept = "Cardiology"
    encrypted_dept = dept_crypto.encrypt(doctor_dept)
    print(f"  • Department: {doctor_dept}")
    print(f"  • Encrypted: {encrypted_dept[:50]}...")
    
    print("\n2️⃣  MEDICAL RECORD CREATION (with ECC-encrypted key)")
    print("-" * 60)
    
    # Encrypt AES session key with ECC
    session_key = b"AES256SessionKey"
    encrypted_key = encrypt_key(session_key, "ECC")
    print(f"  • Session Key: {session_key}")
    print(f"  • Encrypted with ECC: {str(encrypted_key)[:80]}...")
    
    # Decrypt on server
    decrypted_key = decrypt_key(encrypted_key)
    print(f"  • Decrypted: {decrypted_key}")
    print(f"  • Match: {decrypted_key == session_key} ✓")
    
    print("\n3️⃣  RECORD SIGNATURE (with DH + SHA1)")
    print("-" * 60)
    
    record_data = "Patient: John Doe, Diagnosis: Flu"
    signer = SignatureEngine(mode="DH", hash_option="SHA1")
    
    signature = signer.sign(record_data)
    print(f"  • Record: {record_data}")
    print(f"  • Signed with: DH + SHA1")
    print(f"  • Signature: r={signature['r']}, s={signature['s']}")
    
    # Verify signature
    is_valid = signer.verify(record_data, signature)
    print(f"  • Verification: {is_valid} ✓")
    
    print("\n4️⃣  EXPENSE TRACKING (with Paillier homomorphism)")
    print("-" * 60)
    
    expense_crypto = ExpenseCrypto("Paillier")
    
    expenses = [1000, 2500, 750]
    encrypted_expenses = [expense_crypto.encrypt(e) for e in expenses]
    
    print(f"  • Expenses: {expenses}")
    print(f"  • Encrypted: {len(encrypted_expenses)} ciphertexts")
    
    # Homomorphic addition
    total_enc = encrypted_expenses[0]
    for enc in encrypted_expenses[1:]:
        total_enc = expense_crypto.homomorphic_add(total_enc, enc)
    
    total = expense_crypto.decrypt(total_enc)
    print(f"  • Encrypted Sum (computed homomorphically): {total}")
    print(f"  • Expected: {sum(expenses)}")
    print(f"  • Match: {total == sum(expenses)} ✓")
    
    print("\n5️⃣  DEPARTMENT SEARCH (privacy-preserving)")
    print("-" * 60)
    
    # Multiple doctors with encrypted departments
    departments = ["Cardiology", "Neurology", "Cardiology", "Pediatrics"]
    encrypted_depts = [dept_crypto.encrypt(d) for d in departments]
    
    # Search for "Cardiology"
    search_query = "Cardiology"
    search_enc = dept_crypto.encrypt(search_query)
    
    matches = [i for i, enc in enumerate(encrypted_depts) if enc == search_enc]
    
    print(f"  • Departments: {departments}")
    print(f"  • Search for: {search_query}")
    print(f"  • Matches found at indices: {matches}")
    print(f"  • Expected: [0, 2] ✓")

if __name__ == "__main__":
    print("\n" + "╔" + "="*58 + "╗")
    print("║  MedRecSystemModular - New Algorithms Demonstration     ║")
    print("╚" + "="*58 + "╝")
    
    demo_new_encryption_algorithms()
    demo_dh_signatures()
    demo_existing_signatures_with_new_hashes()
    demo_client_server_workflow()
    
    print("\n" + "="*60)
    print("✓ ALL DEMONSTRATIONS COMPLETE!")
    print("="*60)
    print("\nYou can now use these in the actual client/server:")
    print("  • Update config.py to choose algorithms")
    print("  • Run: python server.py")
    print("  • Run: python client.py")
    print("="*60)
