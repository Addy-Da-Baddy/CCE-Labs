"""
Modular Medical Records System - Configuration
Change algorithms here to customize cryptographic operations
"""

# ========== CRYPTOGRAPHIC ALGORITHM CONFIGURATION ==========

# 1. Key Encryption (for AES session keys)
# Options: "RSA", "ElGamal", "AES", "DES", "DH", "Rabin", "ECC"
KEY_ENCRYPTION_ALGORITHM = "Rabin"

# 2. Digital Signature
# Options: "ElGamal", "Schnorr", "RSA", "DH"
SIGNATURE_ALGORITHM = "Schnorr"

# 2b. Signature Hashing (hash before signing)
# Options: "SHA256", "SHA1", "MD5", "None"
SIGNATURE_HASH = "SHA256"

# 3. Department Encryption (for privacy-preserving search)
# Options: "Paillier", "AES"
DEPARTMENT_ENCRYPTION = "Paillier"

# 4. Expense Encryption (homomorphic computation)
# Options: "Paillier", "RSA"
# IMPORTANT: Use "Paillier" for correct additive homomorphism!
# RSA gives multiplication instead of addition
EXPENSE_ENCRYPTION = "RSA"

# 5. Report Content Encryption
# Options: "AES", "RSA", "ElGamal", "DES"
REPORT_ENCRYPTION = "RSA"

# ========== SERVER CONFIGURATION ==========

SERVER_HOST = "localhost"
SERVER_PORT = 9999
DATABASE_FILE = "storage.json"

# ========== CRYPTOGRAPHIC PARAMETERS ==========

# Key sizes for various algorithms
RSA_KEY_SIZE = 2048          # RSA key size in bits
ELGAMAL_PRIME_SIZE = 256     # ElGamal prime size in bits (smaller for demo)
PAILLIER_KEY_SIZE = 512      # Paillier modulus size in bits (smaller for demo)
DH_PRIME_SIZE = 256          # Diffie-Hellman prime size in bits
RABIN_KEY_SIZE = 512         # Rabin modulus size in bits
ECC_CURVE = "P-256"          # ECC curve name

# ========== VALIDATION ==========

def validate_config():
    """Validate that all algorithm choices are valid"""
    
    valid_key_encryption = ["RSA", "ElGamal", "AES", "DES", "DH", "Rabin", "ECC"]
    valid_signatures = ["ElGamal", "Schnorr", "RSA", "DH"]
    valid_signature_hash = ["SHA256", "SHA1", "MD5", "None"]
    valid_department = ["Paillier", "AES"]
    valid_expense = ["Paillier", "RSA"]
    valid_report = ["AES", "RSA", "ElGamal", "DES"]
    
    if KEY_ENCRYPTION_ALGORITHM not in valid_key_encryption:
        raise ValueError(f"Invalid KEY_ENCRYPTION_ALGORITHM: '{KEY_ENCRYPTION_ALGORITHM}'. Choose from {valid_key_encryption}")
    
    if SIGNATURE_ALGORITHM not in valid_signatures:
        raise ValueError(f"Invalid SIGNATURE_ALGORITHM: '{SIGNATURE_ALGORITHM}'. Choose from {valid_signatures}")
    
    if SIGNATURE_HASH not in valid_signature_hash:
        raise ValueError(f"Invalid SIGNATURE_HASH: '{SIGNATURE_HASH}'. Choose from {valid_signature_hash}")
    
    if DEPARTMENT_ENCRYPTION not in valid_department:
        raise ValueError(f"Invalid DEPARTMENT_ENCRYPTION: '{DEPARTMENT_ENCRYPTION}'. Choose from {valid_department}")
    
    if EXPENSE_ENCRYPTION not in valid_expense:
        raise ValueError(f"Invalid EXPENSE_ENCRYPTION: '{EXPENSE_ENCRYPTION}'. Choose from {valid_expense}")
    
    if REPORT_ENCRYPTION not in valid_report:
        raise ValueError(f"Invalid REPORT_ENCRYPTION: '{REPORT_ENCRYPTION}'. Choose from {valid_report}")
    
    # Warnings
    if EXPENSE_ENCRYPTION == "RSA":
        print("\n⚠️  WARNING: RSA expense encryption uses multiplicative homomorphism.")
        print("   This will compute E(m1) * E(m2) = E(m1 × m2), NOT addition!")
        print("   Recommended: Use 'Paillier' for correct additive homomorphism.\n")
    
    if SIGNATURE_HASH in ["MD5", "SHA1"]:
        print(f"\n⚠️  WARNING: {SIGNATURE_HASH} is cryptographically weak and not recommended.")
        print("   Use SHA256 for better security.\n")

# Validate on import
validate_config()
