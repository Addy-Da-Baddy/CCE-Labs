from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify

keypair = RSA.generate(2048)
private_key = keypair
public_key = keypair.publickey()

data = "Super Secret Message".encode('utf-8')

rsa_cipher_enc = PKCS1_OAEP.new(public_key)
ct = rsa_cipher_enc.encrypt(data)

rsa_cipher_dec = PKCS1_OAEP.new(private_key)
pt = rsa_cipher_dec.decrypt(ct)

print("Original Data: ", data.decode("utf-8"))
print("Cipher Text: ", hexlify(ct).decode("utf-8"))
print("Decrypted Text: ", pt.decode("utf-8"))

print("Successful") if pt.decode("utf-8") == data.decode("utf-8") else print("Unsuccessful")
