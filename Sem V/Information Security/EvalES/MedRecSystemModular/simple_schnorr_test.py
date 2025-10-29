"""
Simple Schnorr test with same instance
"""

from crypto_utils import SignatureEngine

# Test with SHA256
print("="*60)
print("Testing Schnorr with SHA256 hash")
print("="*60)

engine = SignatureEngine("Schnorr", "SHA256")
message = "Test message"

print(f"\nParameters:")
print(f"p = {engine.p}")
print(f"q = {engine.q}")
print(f"g = {engine.g}")
print(f"x = {engine.x}")
print(f"y = {engine.y}")

print(f"\nSigning message: '{message}'")
sig = engine.sign(message)
print(f"Signature: r={sig['r']}, s={sig['s']}, e={sig['e']}")

print(f"\nVerifying message: '{message}'")
valid = engine.verify(message, sig)
print(f"Valid: {valid}")

# Test with no hash
print("\n" + "="*60)
print("Testing Schnorr with no hash")
print("="*60)

engine2 = SignatureEngine("Schnorr", "None")
message2 = "Test message"

print(f"\nSigning message: '{message2}'")
sig2 = engine2.sign(message2)
print(f"Signature: r={sig2['r']}, s={sig2['s']}, e={sig2['e']}")

print(f"\nVerifying message: '{message2}'")
valid2 = engine2.verify(message2, sig2)
print(f"Valid: {valid2}")
