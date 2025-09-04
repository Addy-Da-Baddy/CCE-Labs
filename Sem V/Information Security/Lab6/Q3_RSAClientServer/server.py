import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

HOST = '127.0.0.1'
PORT = 65432

def main():
    server_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    server_public_key = server_private_key.public_key()

    message = b"Important message from server"
    signature = server_private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    public_key_pem = server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[SERVER] Listening on {HOST}:{PORT}...")
        conn, addr = s.accept()
        with conn:
            print(f"[SERVER] Connected by {addr}")

            conn.sendall(len(public_key_pem).to_bytes(4, 'big'))
            conn.sendall(public_key_pem)

            conn.sendall(len(message).to_bytes(4, 'big'))
            conn.sendall(message)

            conn.sendall(len(signature).to_bytes(4, 'big'))
            conn.sendall(signature)

            print("[SERVER] Sent public key, message, and signature")

if __name__ == "__main__":
    main()
