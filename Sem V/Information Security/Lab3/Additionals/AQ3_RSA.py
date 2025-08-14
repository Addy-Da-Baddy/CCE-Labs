from Crypto.Util.number import bytes_to_long, long_to_bytes

n = 323
e = 5
d = 173

message = b"Cryptographic Protocols"
m = bytes_to_long(message)

if m >= n:
    print("Message too large for modulus n. Try a shorter message or larger n.")
else:
    c = pow(m, e, n)

    m_dec = pow(c, d, n)
    decrypted = long_to_bytes(m_dec)

    print("Plain text:", message.decode())
    print("Ciphertext:", c)
    print("Decrypted text:", decrypted.decode())
    print("Successful" if decrypted == message else "Unsuccessful")
