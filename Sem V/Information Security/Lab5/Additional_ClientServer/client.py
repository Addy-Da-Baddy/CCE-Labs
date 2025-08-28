import socket
import hashlib
import time

HOST = '127.0.0.1'
PORT = 65432

def compute_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main():
    message = input("Enter the message to send: ")
    message_bytes = message.encode()

    chunk_size = 10
    chunks = [message_bytes[i:i+chunk_size] for i in range(0, len(message_bytes), chunk_size)]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        for chunk in chunks:
            s.sendall(chunk)
            time.sleep(0.1)  # slight delay to simulate chunking

        s.shutdown(socket.SHUT_WR)  # indicate no more data will be sent

        hash_received = s.recv(1024).decode()
        print(f"Hash received from server: {hash_received}")

        local_hash = compute_hash(message_bytes)
        print(f"Local computed hash: {local_hash}")

        if hash_received == local_hash:
            print("Integrity check PASSED: hashes match.")
        else:
            print("Integrity check FAILED: hashes do NOT match!")

if __name__ == "__main__":
    main()
