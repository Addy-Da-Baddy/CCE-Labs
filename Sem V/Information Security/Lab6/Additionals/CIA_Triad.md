

---

# CIA Triad

The **CIA Triad** is a foundational model in information security. It defines three core principles that guide the protection of data and systems: **Confidentiality**, **Integrity**, and **Availability**.

## Overview Table

| Principle       | Definition                                                                 | Objective                                             |
|-----------------|-----------------------------------------------------------------------------|-------------------------------------------------------|
| Confidentiality | Ensuring information is accessible only to authorized individuals          | Prevent unauthorized disclosure of sensitive data    |
| Integrity       | Maintaining accuracy, consistency, and trustworthiness of data             | Prevent unauthorized modification or corruption      |
| Availability    | Ensuring reliable and timely access to information and resources           | Prevent downtime and ensure operational continuity   |

---

## 1. Confidentiality

**Definition**  
Confidentiality ensures that sensitive information is not disclosed to unauthorized parties.

**Common Methods**
| Method              | Description                                      |
|---------------------|--------------------------------------------------|
| Encryption          | Encoding data so only authorized parties can read |
| Access Control      | Restricting access based on roles or permissions  |
| Authentication      | Verifying identity before granting access         |

**Example Code: AES Encryption in Python**
```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
data = b"Sensitive Information"
nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(data)

print("Ciphertext:", ciphertext)
```

---

## 2. Integrity

**Definition**  
Integrity ensures that data remains accurate and unaltered except by authorized actions.

**Common Methods**
| Method             | Description                                       |
|--------------------|---------------------------------------------------|
| Hashing            | Producing a fixed-size digest to detect changes   |
| Digital Signatures | Verifying authenticity and integrity of data      |
| Checksums          | Detecting accidental corruption                   |

**Example Code: SHA-256 Hashing**
```python
import hashlib

data = b"Transaction Record"
hash_value = hashlib.sha256(data).hexdigest()
print("SHA-256 Hash:", hash_value)
```

---

## 3. Availability

**Definition**  
Availability ensures that authorized users have access to information and systems when needed.

**Common Methods**
| Method                  | Description                                   |
|-------------------------|-----------------------------------------------|
| Redundancy              | Backup systems to prevent single points of failure |
| Load Balancing          | Distributing workload to maintain performance |
| Disaster Recovery Plans | Procedures to restore operations after failure |

**Example Code: Simple Availability Check**
```python
import requests

url = "https://example.com"
try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        print("Service is available")
    else:
        print("Service returned an error")
except requests.exceptions.RequestException:
    print("Service is unavailable")
```

---



---

