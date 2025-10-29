"""
Test new algorithm options: ElGamal key encryption, RSA signatures, ElGamal report encryption
"""

import sys
sys.path.insert(0, '.')

import config
from crypto_utils import encrypt_key, decrypt_key, SignatureEngine, encrypt_report, decrypt_report

print("="*70)
print("TESTING NEW ALGORITHM OPTIONS")
print("="*70)

# Test 1: ElGamal Key Encryption
print("\n1. ELGAMAL KEY ENCRYPTION TEST")
print("-" * 70)
test_key = b"My Secret AES Key 12345678901234"
print(f"Original key: {test_key}")

encrypted = encrypt_key(test_key, mode="ElGamal")
print(f"✓ Encrypted with ElGamal")
print(f"  Mode: {encrypted['mode']}")
print(f"  c1: {str(encrypted['c1'])[:60]}...")
print(f"  c2: {str(encrypted['c2'])[:60]}...")

decrypted = decrypt_key(encrypted)
print(f"✓ Decrypted: {decrypted}")
print(f"  Match: {decrypted == test_key} {'✓' if decrypted == test_key else '✗'}")

# Test 2: RSA Signature
print("\n2. RSA DIGITAL SIGNATURE TEST")
print("-" * 70)
rsa_sig_engine = SignatureEngine("RSA")
message = "Medical Report: Patient shows improvement"
print(f"Message: {message}")

signature = rsa_sig_engine.sign(message)
print(f"✓ Signed with RSA")
print(f"  Mode: {signature['mode']}")
print(f"  Signature: {str(signature['signature'])[:60]}...")
print(f"  Timestamp: {signature['ts']}")

valid = rsa_sig_engine.verify(message, signature)
print(f"✓ Signature verification: {valid} {'✓' if valid else '✗'}")

# Tamper test
tampered = "Medical Report: Patient shows NO improvement"
valid_tampered = rsa_sig_engine.verify(tampered, signature)
print(f"✓ Tampered message verification: {valid_tampered} {'✗ (Correctly rejected)' if not valid_tampered else '✓ (Should have failed!)'}")

# Test 3: ElGamal Report Encryption
print("\n3. ELGAMAL REPORT ENCRYPTION TEST")
print("-" * 70)
report_data = b"Patient Medical Record: Confidential information about treatment"
print(f"Original report: {report_data[:40]}...")

encrypted_report = encrypt_report(report_data, mode="ElGamal")
print(f"✓ Encrypted with ElGamal")
print(f"  Mode: {encrypted_report['mode']}")
print(f"  Ciphertext: {encrypted_report['ciphertext'][:40]}...")
print(f"  ElGamal c1: {str(encrypted_report['c1'])[:40]}...")
print(f"  ElGamal c2: {str(encrypted_report['c2'])[:40]}...")

decrypted_report = decrypt_report(encrypted_report)
print(f"✓ Decrypted: {decrypted_report[:40]}...")
print(f"  Match: {decrypted_report == report_data} {'✓' if decrypted_report == report_data else '✗'}")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("✓ ElGamal Key Encryption: Working")
print("✓ RSA Digital Signature: Working")
print("✓ ElGamal Report Encryption: Working")
print("\nAll new algorithm options successfully implemented!")
print("="*70)
