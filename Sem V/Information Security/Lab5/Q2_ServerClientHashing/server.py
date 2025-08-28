import socket
import hashlib

HOST = '127.0.0.1'
PORT = 65432

def compute_hash(data):
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024)
            if not data:
                return

            print(f"Received data: {data}")

            # Uncomment the next line to simulate data tampering
            #data = data + b'corrupted'

            hash_value = compute_hash(data)
            print(f"Computed hash: {hash_value}")

            conn.sendall(hash_value.encode())

if __name__ == "__main__":
    main()
