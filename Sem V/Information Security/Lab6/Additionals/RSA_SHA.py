from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pss
from Crypto.Hash import SHA256

message = b"Confidential and authentic message"

key = RSA.generate(2048)
private_key = key
public_key = key.publickey()


cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
ciphertext = cipher.encrypt(message)

decipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
decrypted_message = decipher.decrypt(ciphertext)


h = SHA256.new(message)

signer = pss.new(private_key)
signature = signer.sign(h)

verifier = pss.new(public_key)
try:
    verifier.verify(h, signature)
    verified = True
except (ValueError, TypeError):
    verified = False

print("Original message:", message)
print("Decrypted message:", decrypted_message)
print("Confidentiality:", "Success" if decrypted_message == message else "Failed")
print("Signature Verified:", "Yes" if verified else "No")
