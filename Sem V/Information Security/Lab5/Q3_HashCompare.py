import hashlib
import random
import string
import time
import matplotlib.pyplot as plt

def generate_random_strings(n, min_len=5, max_len=20):
    strings = []
    for _ in range(n):
        length = random.randint(min_len, max_len)
        s = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        strings.append(s)
    return strings

def compute_hashes(strings, hash_func_name):
    hash_func = getattr(hashlib, hash_func_name)
    hashes = []
    start_time = time.time()
    for s in strings:
        h = hash_func(s.encode()).hexdigest()
        hashes.append(h)
    elapsed = time.time() - start_time
    return hashes, elapsed

def detect_collisions(hashes):
    seen = set()
    collisions = []
    for h in hashes:
        if h in seen:
            collisions.append(h)
        else:
            seen.add(h)
    return collisions

def main():
    n = random.randint(50, 100)
    print(f"Generating {n} random strings...")
    data = generate_random_strings(n)

    hash_algorithms = ['md5', 'sha1', 'sha256']
    times = []
    collision_counts = []

    for algo in hash_algorithms:
        print(f"\nAnalyzing {algo.upper()}...")
        hashes, elapsed = compute_hashes(data, algo)
        collisions = detect_collisions(hashes)
        print(f"Time taken: {elapsed:.6f} seconds")
        print(f"Collisions detected: {len(collisions)}")

        times.append(elapsed)
        collision_counts.append(len(collisions))

    # Plotting with line plots
    plt.figure(figsize=(10,5))

    # Time plot
    plt.plot(hash_algorithms, times, marker='o', linestyle='-', color='blue', label='Computation Time (s)')
    for i, t in enumerate(times):
        plt.text(i, t, f"{t:.4f}", ha='center', va='bottom')

    # Collision plot
    plt.plot(hash_algorithms, collision_counts, marker='s', linestyle='--', color='red', label='Collisions')

    plt.title('Hashing Algorithms: Computation Time & Collisions')
    plt.xlabel('Hash Algorithm')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
