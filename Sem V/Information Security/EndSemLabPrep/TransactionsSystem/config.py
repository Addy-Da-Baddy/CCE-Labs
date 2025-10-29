"""
Transaction System Configuration
Configure cryptographic algorithms here
"""

# ========== CRYPTOGRAPHIC ALGORITHM CONFIGURATION ==========

# 1. Transaction Encryption (Homomorphic)
# Options: "Paillier", "RSA", "DH", "Rabin", "ECC"
# Paillier: True additive homomorphism E(a) + E(b) = E(a+b)
# RSA: Exponent trick for additive properties base^a * base^b = base^(a+b)
# DH: Diffie-Hellman based encryption
# Rabin: Rabin cryptosystem (similar to RSA)
# ECC: Elliptic Curve Cryptography
TRANSACTION_ENCRYPTION = "Paillier"

# 2. Digital Signature Algorithm
# Options: "RSA", "ElGamal", "Schnorr", "DH"
# DH: Diffie-Hellman based signature
SIGNATURE_ALGORITHM = "ElGamal"

# 3. Hash Algorithm for Signatures
# Options: "SHA256", "SHA1", "MD5", "None"
# SHA256: Use SHA-256 hashing before signing (recommended)
# SHA1: Use SHA-1 hashing before signing
# MD5: Use MD5 hashing before signing (weak, not recommended)
# None: Sign the raw data directly (not recommended for large data)
SIGNATURE_HASH = "SHA256"

# ========== SERVER CONFIGURATION ==========

SERVER_HOST = "localhost"
SERVER_PORT = 10000

# ========== CRYPTOGRAPHIC PARAMETERS ==========

# Key sizes for various algorithms
RSA_KEY_SIZE = 2048          # RSA key size in bits
PAILLIER_KEY_SIZE = 512      # Paillier modulus size in bits (smaller for demo)
ELGAMAL_PRIME_SIZE = 256     # ElGamal prime size in bits
RABIN_KEY_SIZE = 512         # Rabin modulus size in bits (smaller for demo)
DH_PRIME_SIZE = 256          # Diffie-Hellman prime size in bits
ECC_CURVE = "P-256"          # ECC curve name

# ========== VALIDATION ==========

def validate_config():
    """Validate that all algorithm choices are valid"""
    
    valid_transaction_encryption = ["Paillier", "RSA", "DH", "Rabin", "ECC"]
    valid_signature = ["RSA", "ElGamal", "Schnorr", "DH"]
    valid_hash = ["SHA256", "SHA1", "MD5", "None"]
    
    if TRANSACTION_ENCRYPTION not in valid_transaction_encryption:
        raise ValueError(f"Invalid TRANSACTION_ENCRYPTION: '{TRANSACTION_ENCRYPTION}'. Choose from {valid_transaction_encryption}")
    
    if SIGNATURE_ALGORITHM not in valid_signature:
        raise ValueError(f"Invalid SIGNATURE_ALGORITHM: '{SIGNATURE_ALGORITHM}'. Choose from {valid_signature}")
    
    if SIGNATURE_HASH not in valid_hash:
        raise ValueError(f"Invalid SIGNATURE_HASH: '{SIGNATURE_HASH}'. Choose from {valid_hash}")
    
    # Warnings
    if TRANSACTION_ENCRYPTION == "RSA":
        print("\n⚠️  NOTE: RSA uses exponent trick (base^amount) for additive homomorphism.")
        print("   This works but Paillier is mathematically more elegant.\n")
    
    if SIGNATURE_HASH in ["MD5", "SHA1"]:
        print(f"\n⚠️  WARNING: {SIGNATURE_HASH} is cryptographically weak and not recommended.")
        print("   Use SHA256 for better security.\n")

# Validate on import
validate_config()
