import socket
import hashlib

HOST = '127.0.0.1'  # localhost
PORT = 65432

def compute_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            full_message = b''
            while True:
                data = conn.recv(1024)
                if not data:  # client closed sending
                    break
                full_message += data

            print(f"Received full message: {full_message.decode()}")
            hash_value = compute_hash(full_message)
            print(f"Computed hash: {hash_value}")

            # Send hash back to client
            conn.sendall(hash_value.encode())

if __name__ == "__main__":
    main()
