import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

HOST = '127.0.0.1'
PORT = 65432

def recv_exact(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise ConnectionError("Connection closed unexpectedly")
        data += packet
    return data

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        public_key_len = int.from_bytes(recv_exact(s, 4), 'big')
        public_key_pem = recv_exact(s, public_key_len)
        public_key = serialization.load_pem_public_key(public_key_pem)

        message_len = int.from_bytes(recv_exact(s, 4), 'big')
        message = recv_exact(s, message_len)

        signature_len = int.from_bytes(recv_exact(s, 4), 'big')
        signature = recv_exact(s, signature_len)

        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            verified = True
        except InvalidSignature:
            verified = False

        print(f"message: {message.decode()}")
        print(f"signature (hex): {signature.hex()[:64]}...")
        print(f"verified: {'verified' if verified else 'berofoed'}")

if __name__ == "__main__":
    main()
