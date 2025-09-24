"""You are tasked with developing a secure healthcare data management system called "MediSecure". This system ensures that patients' medical records are stored confidentially, accessed only by authorized users, and verified for authenticity. The system supports three types of users: Patients, Doctors, and Auditors, each with specific roles and permissions.
The platform uses AES symmetric encryption for storing sensitive medical records, RSA digital signatures for authenticating users, and SHA512 hashing to verify record integrity.

User Roles & Permissions:

Patient:

Encrypts personal medical records (e.g., “BloodTest Report_2025.pdf: Confidential”) using AES before uploading.

Signs the SHA512 hash of the encrypted record using RSA private key.

Can view past uploaded records and their encrypted/hashed forms with timestamps.

Doctor:

Decrypts patient records using the shared AES key (securely exchanged).

Verifies RSA signatures of patients to ensure authenticity.

Computes SHA512 hash of decrypted records and compares with stored hash.

Stores verification results with timestamps.

Auditor:

Can view only the hashed medical records with timestamps.

Verifies RSA signatures on stored records for auditing purposes.

Access Roles:

Allow Patients to encrypt records with AES, sign using RSA, and upload securely.

Enable Doctors to decrypt with AES, verify RSA signatures, and hash the records.

Allow Auditors to view only hashes and verify signatures.

Task:
Develop a menu-driven Python program that implements these functionalities using AES symmetric encryption, RSA digital signatures, and SHA512 hashing. Ensure secure handling of medical records and proper role-based access. 
    """
    
    
#!/usr/bin/env python3
"""
MediSecure - In-memory secure healthcare data management demo
Uses PyCryptodome:
    pip install pycryptodome
Run with Python 3.8+
"""

import sys
import time
from datetime import datetime
from typing import Dict, List
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

# -------------------------
# Crypto helpers
# -------------------------
def generate_rsa_keypair(bits: int = 2048):
    key = RSA.generate(bits)
    pub = key.publickey()
    return key, pub

def rsa_encrypt_with_pub(pubkey: RSA.RsaKey, data: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(pubkey)
    return cipher.encrypt(data)

def rsa_decrypt_with_priv(privkey: RSA.RsaKey, data: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(privkey)
    return cipher.decrypt(data)

def rsa_sign(privkey: RSA.RsaKey, data: bytes) -> bytes:
    h = SHA512.new(data)
    signer = pkcs1_15.new(privkey)
    return signer.sign(h)

def rsa_verify(pubkey: RSA.RsaKey, data: bytes, signature: bytes) -> bool:
    h = SHA512.new(data)
    verifier = pkcs1_15.new(pubkey)
    try:
        verifier.verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

def sha512_digest(data: bytes) -> bytes:
    return SHA512.new(data).digest()

def aes_encrypt(plaintext: bytes, key: bytes):
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(plaintext)
    return {'ciphertext': ct, 'nonce': nonce, 'tag': tag}

def aes_decrypt(ct: bytes, key: bytes, nonce: bytes, tag: bytes):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ct, tag)

# -------------------------
# Data models (in-memory)
# -------------------------
class UserAccount:
    def __init__(self, user_id: str, role: str):
        self.user_id = user_id
        self.role = role  # 'patient' / 'doctor' / 'auditor'
        self.privkey, self.pubkey = generate_rsa_keypair(2048)

class MedicalRecord:
    def __init__(self, record_id: int, patient_id: str, ciphertext: bytes, nonce: bytes, tag: bytes,
                 hash_hex: str, signature: bytes, timestamp: str):
        self.record_id = record_id
        self.patient_id = patient_id
        self.ciphertext = ciphertext
        self.nonce = nonce
        self.tag = tag
        self.hash_hex = hash_hex  # hex of SHA512 of plaintext
        self.signature = signature  # RSA signature bytes on hash
        self.timestamp = timestamp
        self.verifications = []  # list of dicts {doctor_id, time, signature_ok, hash_match, notes}

class PatientAccount(UserAccount):
    def __init__(self, user_id: str):
        super().__init__(user_id, 'patient')
        self.aes_key = get_random_bytes(32)  # AES-256
        # mapping doctor_id -> encrypted AES key bytes (RSA-encrypted by patient with doctor's pubkey)
        self.shared_keys: Dict[str, bytes] = {}
        self.records: List[MedicalRecord] = []

class DoctorAccount(UserAccount):
    def __init__(self, user_id: str):
        super().__init__(user_id, 'doctor')
        # stores decrypted AES keys for patients after access granted: patient_id -> aes_key bytes
        self.decrypted_patient_keys: Dict[str, bytes] = {}

class AuditorAccount(UserAccount):
    def __init__(self, user_id: str):
        super().__init__(user_id, 'auditor')

# -------------------------
# System store
# -------------------------
patients: Dict[str, PatientAccount] = {}
doctors: Dict[str, DoctorAccount] = {}
auditors: Dict[str, AuditorAccount] = {}
record_counter = 0

# Pre-create a sample doctor and auditor
doctors['dr_alex'] = DoctorAccount('dr_alex')
auditors['audit_1'] = AuditorAccount('audit_1')

# -------------------------
# Role operations
# -------------------------
def register_patient():
    uid = input("Enter new patient ID: ").strip()
    if uid == "":
        print("Invalid ID.")
        return
    if uid in patients:
        print("Patient already exists.")
        return
    p = PatientAccount(uid)
    patients[uid] = p
    print(f"Patient '{uid}' registered. AES key generated and stored securely (in-memory).")
    print("Share AES key with doctors via 'Share AES key with Doctor' option.")

def list_patients_brief():
    if not patients:
        print("No patients registered.")
        return
    for pid, p in patients.items():
        print(f"- {pid} (records: {len(p.records)})")

def list_doctors_brief():
    if not doctors:
        print("No doctors registered.")
        return
    for did in doctors:
        print(f"- {did}")

def patient_menu(patient: PatientAccount):
    global record_counter
    while True:
        print("\n--- PATIENT MENU ---")
        print("1) Upload (encrypt + sign) medical record")
        print("2) View my uploaded records (encrypted + hash + timestamps)")
        print("3) Share AES key with a doctor")
        print("4) Show my RSA public key (for doctors/auditors)")
        print("0) Back")
        c = input("> ").strip()
        if c == '1':
            text = input("Enter medical record content (short text simulating file): ").strip()
            if text == "":
                print("Empty record aborted.")
                continue
            plaintext = text.encode()
            # AES encrypt plaintext
            aes_out = aes_encrypt(plaintext, patient.aes_key)
            ct = aes_out['ciphertext']
            nonce = aes_out['nonce']
            tag = aes_out['tag']
            # compute SHA512 over plaintext (so doctor can validate after decrypt)
            digest = sha512_digest(plaintext)
            digest_hex = digest.hex()
            # sign the digest with patient's RSA private key
            signature = rsa_sign(patient.privkey, digest)
            # store record
            record_counter += 1
            rec = MedicalRecord(record_counter, patient.user_id, ct, nonce, tag, digest_hex, signature, datetime.utcnow().isoformat() + "Z")
            patient.records.append(rec)
            print(f"Record uploaded (ID {rec.record_id}). Encrypted and signed.")
        elif c == '2':
            if not patient.records:
                print("No records.")
                continue
            for r in patient.records:
                print(f"\nRecord ID: {r.record_id}")
                print("Timestamp:", r.timestamp)
                print("Ciphertext (hex, truncated):", r.ciphertext.hex()[:80] + "...")
                print("Nonce:", r.nonce.hex())
                print("Tag:", r.tag.hex())
                print("Stored SHA512 hash (plaintext):", r.hash_hex)
                print("Signature (hex, truncated):", r.signature.hex()[:160] + "...")
        elif c == '3':
            list_doctors_brief()
            did = input("Enter doctor ID to share AES key with: ").strip()
            if did not in doctors:
                print("Doctor not found.")
                continue
            doctor = doctors[did]
            # encrypt AES key with doctor's RSA public key
            enc_key = rsa_encrypt_with_pub(doctor.pubkey, patient.aes_key)
            patient.shared_keys[did] = enc_key
            print(f"AES key encrypted with doctor's public key and stored for doctor '{did}'.")
        elif c == '4':
            pub = patient.pubkey.export_key().decode()
            print("Your RSA public key (PEM):\n", pub)
        elif c == '0':
            return
        else:
            print("Invalid choice")

def doctor_menu(doctor: DoctorAccount):
    while True:
        print("\n--- DOCTOR MENU ---")
        print("1) List patients")
        print("2) Request AES key for a patient (decrypt shared key)")
        print("3) List records for a patient")
        print("4) Decrypt & verify a patient's record (compute hash & verify signature)")
        print("5) Show my RSA public key")
        print("0) Back")
        c = input("> ").strip()
        if c == '1':
            list_patients_brief()
        elif c == '2':
            pid = input("Enter patient ID to request AES key for: ").strip()
            if pid not in patients:
                print("Patient not found.")
                continue
            patient = patients[pid]
            if doctor.user_id not in patient.shared_keys:
                print("AES key not shared by patient with you.")
                continue
            enc_key = patient.shared_keys[doctor.user_id]
            try:
                aes_key = rsa_decrypt_with_priv(doctor.privkey, enc_key)
            except Exception as e:
                print("Failed to decrypt AES key:", e)
                continue
            doctor.decrypted_patient_keys[pid] = aes_key
            print(f"AES key for patient '{pid}' decrypted and stored in your session (in-memory).")
        elif c == '3':
            pid = input("Enter patient ID to list records: ").strip()
            if pid not in patients:
                print("Patient not found.")
                continue
            patient = patients[pid]
            if not patient.records:
                print("No records for this patient.")
                continue
            for r in patient.records:
                print(f"- Record ID {r.record_id}, timestamp {r.timestamp}, stored hash {r.hash_hex}")
        elif c == '4':
            pid = input("Enter patient ID: ").strip()
            if pid not in patients:
                print("Patient not found.")
                continue
            patient = patients[pid]
            if pid not in doctor.decrypted_patient_keys:
                print("You don't have the AES key for this patient. Use option 2 to request it.")
                continue
            key = doctor.decrypted_patient_keys[pid]
            rid_s = input("Enter record ID to decrypt & verify: ").strip()
            if not rid_s.isdigit():
                print("Invalid record ID.")
                continue
            rid = int(rid_s)
            rec = next((x for x in patient.records if x.record_id == rid), None)
            if not rec:
                print("Record not found.")
                continue
            try:
                plaintext = aes_decrypt(rec.ciphertext, key, rec.nonce, rec.tag)
            except Exception as e:
                print("AES decryption/authentication failed:", e)
                verified = False
                notes = "decryption_failed"
                rec.verifications.append({'doctor_id': doctor.user_id, 'time': datetime.utcnow().isoformat() + "Z",
                                          'signature_ok': False, 'hash_match': False, 'notes': notes})
                continue
            # compute SHA512 of plaintext and compare with stored hash
            computed_digest = sha512_digest(plaintext)
            computed_hex = computed_digest.hex()
            hash_match = (computed_hex == rec.hash_hex)
            # verify patient's signature (signature was over plaintext hash)
            patient_pub = patient.pubkey
            sig_ok = rsa_verify(patient_pub, computed_digest, rec.signature)
            notes = "ok" if (hash_match and sig_ok) else "mismatch"
            rec.verifications.append({'doctor_id': doctor.user_id, 'time': datetime.utcnow().isoformat() + "Z",
                                      'signature_ok': sig_ok, 'hash_match': hash_match, 'notes': notes})
            print("\nDecryption successful.")
            print("Plaintext (simulated file content):", plaintext.decode(errors='replace'))
            print("Stored hash:", rec.hash_hex)
            print("Computed hash:", computed_hex)
            print("Hash match:", hash_match)
            print("Signature valid:", sig_ok)
        elif c == '5':
            print("Your RSA public key (PEM):\n", doctor.pubkey.export_key().decode())
        elif c == '0':
            return
        else:
            print("Invalid choice")

def auditor_menu(auditor: AuditorAccount):
    while True:
        print("\n--- AUDITOR MENU ---")
        print("1) List all patients' records (hashes & timestamps only)")
        print("2) Verify signature on a stored record (without plaintext)")
        print("0) Back")
        c = input("> ").strip()
        if c == '1':
            any_rec = False
            for pid, patient in patients.items():
                for r in patient.records:
                    any_rec = True
                    print(f"Patient:{pid} RecordID:{r.record_id} Timestamp:{r.timestamp} Hash:{r.hash_hex}")
            if not any_rec:
                print("No records available.")
        elif c == '2':
            pid = input("Enter patient ID: ").strip()
            if pid not in patients:
                print("Patient not found.")
                continue
            patient = patients[pid]
            rid_s = input("Enter record ID: ").strip()
            if not rid_s.isdigit():
                print("Invalid record ID.")
                continue
            rid = int(rid_s)
            rec = next((x for x in patient.records if x.record_id == rid), None)
            if not rec:
                print("Record not found.")
                continue
            # Auditor has only the stored hash and signature; verify signature over hash
            hash_bytes = bytes.fromhex(rec.hash_hex)
            sig_ok = rsa_verify(patient.pubkey, hash_bytes, rec.signature)
            print("Signature valid on stored hash:", sig_ok)
        elif c == '0':
            return
        else:
            print("Invalid choice")

# -------------------------
# Top-level menu
# -------------------------
def main_menu():
    print("MediSecure - Secure Healthcare Data Management (in-memory demo)")
    while True:
        print("\nMain Menu:")
        print("1) Register patient")
        print("2) Patient login")
        print("3) Doctor login")
        print("4) Auditor login")
        print("5) List doctors & auditors (debug)")
        print("0) Exit")
        c = input("> ").strip()
        if c == '1':
            register_patient()
        elif c == '2':
            pid = input("Enter patient ID: ").strip()
            if pid not in patients:
                print("Patient not found.")
                continue
            patient_menu(patients[pid])
        elif c == '3':
            did = input("Enter doctor ID (existing or new): ").strip()
            if did == "":
                print("Invalid ID."); continue
            if did not in doctors:
                # create new doctor account
                doctors[did] = DoctorAccount(did)
                print(f"Doctor '{did}' created.")
            doctor_menu(doctors[did])
        elif c == '4':
            aid = input("Enter auditor ID (existing or new): ").strip()
            if aid == "":
                print("Invalid ID."); continue
            if aid not in auditors:
                auditors[aid] = AuditorAccount(aid)
                print(f"Auditor '{aid}' created.")
            auditor_menu(auditors[aid])
        elif c == '5':
            print("\nDoctors:")
            for did, d in doctors.items():
                print(f"- {did}")
            print("\nAuditors:")
            for aid in auditors:
                print(f"- {aid}")
        elif c == '0':
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main_menu()
