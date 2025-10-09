
# Secure Data Storage and Transmission Using GnuPG

## Introduction

This report demonstrates the process of securely storing and transmitting data using GnuPG (GNU Privacy Guard). It also details the creation of a digital signature to guarantee data authenticity and integrity, as well as verifying that signature after transmission.

---

## 1. GnuPG Overview

GnuPG is an open-source implementation of the OpenPGP standard. It provides cryptographic privacy and authentication through:

- **Encryption**: Protecting data confidentiality by encoding messages.
- **Digital Signatures**: Verifying the sender’s identity and ensuring message integrity.

---

## 2. Key Generation

To enable encryption and signing, a user must first generate a public-private key pair.

```bash
gpg --full-generate-key
````

* Select key type (usually RSA).
* Select key size (2048 or 4096 bits).
* Set expiration date (optional).
* Provide user identification (name, email).
* Protect the key with a passphrase.

The **public key** is shared with communication partners, while the **private key** remains secret.

---

## 3. Exporting the Public Key

To allow others to encrypt messages or verify signatures, export your public key:

```bash
gpg --export -a "User Name" > publickey.asc
```

The `publickey.asc` file can be distributed publicly.

---

## 4. Encrypting Data for Secure Transmission

To encrypt a file (`message.txt`) for a recipient:

```bash
gpg --encrypt --recipient "Recipient Name" message.txt
```

This produces `message.txt.gpg`, an encrypted file that only the recipient can decrypt using their private key.

---

## 5. Decrypting Received Data

The recipient decrypts the encrypted message using:

```bash
gpg --decrypt message.txt.gpg > decrypted_message.txt
```

This operation requires the recipient’s private key and passphrase.

---

## 6. Creating a Digital Signature

To sign data and ensure its authenticity, generate a detached signature:

```bash
gpg --output message.sig --detach-sig message.txt
```

This produces `message.sig`, a signature file separate from the message.

---

## 7. Verifying the Digital Signature

The receiver verifies the signature with the sender’s public key:

```bash
gpg --verify message.sig message.txt
```

If the signature is valid, GnuPG confirms that the message is unaltered and was signed by the owner of the private key.

---



