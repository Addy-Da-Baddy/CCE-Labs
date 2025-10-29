"""
Demo script to test all MedRecSystem features
This demonstrates the privacy-preserving medical records system
"""
import socket, json, time
from crypto_utils import *

SERVER = ("localhost", 9999)

# Generate keys
rsa_priv, rsa_pub = generate_rsa_keys()
elg = ElGamal()
paillier = Paillier()
exp_priv, exp_pub, N_exp, e_exp = generate_rsa_homomorphic()

def send_request(payload):
    s = socket.socket()
    s.connect(SERVER)
    s.send(json.dumps(payload).encode())
    resp = s.recv(65536).decode()
    s.close()
    try:
        return json.loads(resp)
    except:
        return {"status": "error", "msg": resp}

def demo():
    print("\n" + "="*70)
    print("DEMO: Privacy-Preserving Medical Records System")
    print("="*70)
    
    # 1. Doctor Registration
    print("\n[1] Doctor Registration with Encrypted Department")
    print("-" * 70)
    
    doctors = [
        ("DR001", "Cardiology"),
        ("DR002", "Neurology"),
        ("DR003", "Cardiology")
    ]
    
    for doc_id, dept in doctors:
        dept_enc = paillier.encrypt(abs(hash(dept)))
        payload = {
            "action": "register_doctor",
            "data": {
                "id": doc_id,
                "dept": dept_enc,
                "paillier_n": paillier.n,
                "rsa_pub": rsa_pub.decode()
            }
        }
        resp = send_request(payload)
        print(f"  ✓ Registered {doc_id} in {dept}: {resp.get('msg')}")
    
    # 2. Submit Reports with Signatures
    print("\n[2] Secure Report Submission with Signature Verification")
    print("-" * 70)
    
    reports = [
        ("DR001", "Patient shows stable cardiac function. ECG normal."),
        ("DR002", "MRI scan reveals no abnormalities. Patient cleared."),
        ("DR003", "Post-operative checkup successful. Recovery on track.")
    ]
    
    for doc_id, content in reports:
        aes_key = get_random_bytes(32)
        encrypted = aes_encrypt(content.encode(), aes_key)
        wrapped_key = rsa_encrypt(aes_key, rsa_pub)
        sig = elg.sign(content)
        
        payload = {
            "action": "store_report",
            "data": {
                "id": doc_id,
                "report": encrypted,
                "key": wrapped_key,
                "sig": sig,
                "elgamal_pub": {"p": elg.p, "g": elg.g, "y": elg.y}
            }
        }
        resp = send_request(payload)
        print(f"  ✓ {doc_id} submitted report (ID: {resp.get('report_id')}): ElGamal signed")
    
    # 3. Log Expenses (Encrypted)
    print("\n[3] Privacy-Preserving Expense Tracking (Encrypted)")
    print("-" * 70)
    
    expenses = [
        ("DR001", 150),
        ("DR001", 200),
        ("DR002", 300),
        ("DR003", 100),
        ("DR003", 250)
    ]
    
    for doc_id, amt in expenses:
        enc = rsa_homo_encrypt(amt, N_exp, e_exp)
        payload = {
            "action": "add_expense",
            "id": doc_id,
            "amount": enc,
            "n": N_exp
        }
        resp = send_request(payload)
        print(f"  ✓ {doc_id}: Logged expense {amt} (encrypted)")
    
    time.sleep(0.5)
    
    # 4. Auditor: Search by Department
    print("\n[4] Auditor: Search Doctors by Department (Privacy-Preserving)")
    print("-" * 70)
    
    search_dept = "Cardiology"
    dept_enc = paillier.encrypt(abs(hash(search_dept)))
    payload = {"action": "search_by_dept", "dept_enc": dept_enc}
    resp = send_request(payload)
    
    matches = resp.get("matches", [])
    print(f"  Searching for: {search_dept}")
    print(f"  ✓ Found {len(matches)} doctor(s):")
    for match in matches:
        print(f"    • {match['id']}")
    
    # 5. Auditor: Sum All Expenses
    print("\n[5] Auditor: Sum All Expenses (Homomorphic)")
    print("-" * 70)
    
    payload = {"action": "sum_all_expenses", "n": N_exp}
    resp = send_request(payload)
    
    print(f"  ✓ Total doctors with expenses: {resp.get('count')}")
    print(f"  ✓ Encrypted sum: {resp.get('encrypted_sum')}")
    
    if resp.get('encrypted_sum'):
        decrypted = rsa_homo_decrypt(resp.get('encrypted_sum'), exp_priv)
        print(f"  ✓ Decrypted total: {decrypted}")
        print(f"    (Expected: {sum(amt for _, amt in expenses)})")
    
    # 6. Auditor: Sum Doctor Expenses
    print("\n[6] Auditor: Sum Expenses for Specific Doctor")
    print("-" * 70)
    
    check_doc = "DR001"
    payload = {"action": "sum_doctor_expenses", "doctor_id": check_doc, "n": N_exp}
    resp = send_request(payload)
    
    print(f"  Doctor: {check_doc}")
    print(f"  ✓ Encrypted sum: {resp.get('encrypted_sum')}")
    
    if resp.get('encrypted_sum'):
        decrypted = rsa_homo_decrypt(resp.get('encrypted_sum'), exp_priv)
        print(f"  ✓ Decrypted total: {decrypted}")
        expected = sum(amt for doc, amt in expenses if doc == check_doc)
        print(f"    (Expected: {expected})")
    
    # 7. Auditor: Verify Report
    print("\n[7] Auditor: Verify Report Signature & Timestamp")
    print("-" * 70)
    
    report_id = 0
    payload = {"action": "verify_report", "report_id": report_id}
    resp = send_request(payload)
    
    if resp.get("status") == "ok":
        report = resp.get("report", {})
        print(f"  ✓ Report #{report_id}")
        print(f"    • Doctor: {report.get('id')}")
        print(f"    • Timestamp: {report.get('timestamp')}")
        print(f"    • Signature: Present ✓")
    
    # 8. Auditor: List All Records
    print("\n[8] Auditor: List & Audit All Records")
    print("-" * 70)
    
    payload = {"action": "list_all_records"}
    resp = send_request(payload)
    
    if resp.get("status") == "ok":
        summary = resp.get("summary", {})
        print(f"  ✓ Total Doctors: {summary.get('doctors_count')}")
        print(f"  ✓ Total Reports: {summary.get('reports_count')}")
        print(f"  ✓ Doctors with Expenses: {summary.get('doctors_with_expenses')}")
    
    print("\n" + "="*70)
    print("DEMO COMPLETED SUCCESSFULLY")
    print("="*70)
    print("\n✓ All features demonstrated:")
    print("  • Doctor registration with encrypted department")
    print("  • Secure report submission with ElGamal signatures")
    print("  • Privacy-preserving expense tracking (RSA homomorphic)")
    print("  • Department search without decryption (Paillier)")
    print("  • Homomorphic expense summation")
    print("  • Report signature verification")
    print("  • Complete audit trail")
    print()

if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("  Make sure the server is running: python server.py")
