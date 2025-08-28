import socket
import hashlib

HOST = '127.0.0.1'
PORT = 65432

def compute_hash(data):
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()

def main():
    data = input("Enter data to send: ").encode()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data)

        hash_from_server = s.recv(1024).decode()
        print(f"Hash received from server: {hash_from_server}")

    local_hash = compute_hash(data)
    print(f"Local hash: {local_hash}")

    if local_hash == hash_from_server:
        print("Data integrity verified: hashes match!")
    else:
        print("Data integrity check failed: hashes do NOT match!")

if __name__ == "__main__":
    main()
