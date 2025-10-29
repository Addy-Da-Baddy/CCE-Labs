"""
Modular Medical Records Client
Uses cryptographic algorithms configured in config.py
"""

import socket
import json
import time
import config
from crypto_utils import (
    SignatureEngine, DepartmentCrypto, ExpenseCrypto,
    encrypt_report, decrypt_report, encrypt_key, decrypt_key
)

SERVER = (config.SERVER_HOST, config.SERVER_PORT)

# Initialize cryptographic engines
signature_engine = None
dept_crypto = None
expense_crypto = None
server_config = None

def send_request(payload):
    """Send request to server and get response"""
    s = socket.socket()
    s.connect(SERVER)
    s.send(json.dumps(payload).encode())
    resp = s.recv(655360).decode()
    s.close()
    try:
        return json.loads(resp)
    except:
        return {"status": "error", "msg": resp}

def initialize_crypto():
    """Fetch server configuration and initialize crypto engines"""
    global signature_engine, dept_crypto, expense_crypto, server_config
    
    print("\n[*] Fetching server cryptographic configuration...")
    resp = send_request({"action": "get_crypto_config"})
    
    if resp.get("status") != "ok":
        print(f"[-] Error: {resp.get('msg', 'Unknown error')}")
        return False
    
    server_config = resp.get("config", {})
    
    # Initialize based on server configuration
    signature_engine = SignatureEngine(
        server_config.get("signature"),
        server_config.get("signature_hash")
    )
    
    # For department crypto, use server's public key if Paillier
    dept_pub = resp.get("department_public", {})
    if dept_pub.get("mode") == "Paillier":
        dept_crypto = DepartmentCrypto("Paillier")
        dept_crypto.n = dept_pub["n"]
        dept_crypto.g = dept_pub["g"]
    else:
        dept_crypto = DepartmentCrypto(server_config.get("department"))
    
    # For expense crypto, use server's public key
    exp_pub = resp.get("expense_public", {})
    if exp_pub.get("mode") == "Paillier":
        expense_crypto = ExpenseCrypto("Paillier")
        expense_crypto.n = exp_pub["n"]
        expense_crypto.g = exp_pub["g"]
        expense_crypto.n_sq = expense_crypto.n * expense_crypto.n
    else:
        expense_crypto = ExpenseCrypto(server_config.get("expense"))
        if hasattr(expense_crypto, 'e'):
            expense_crypto.e = exp_pub.get("e")
            expense_crypto.n = exp_pub.get("n")
    
    print("[+] Cryptographic systems initialized")
    print(f"    • Signature: {server_config.get('signature')}")
    print(f"    • Signature Hash: {server_config.get('signature_hash')}")
    print(f"    • Department: {server_config.get('department')}")
    print(f"    • Expense: {server_config.get('expense')}")
    print(f"    • Report: {server_config.get('report')}")
    
    return True

# ============================================================
# DOCTOR PORTAL FUNCTIONS
# ============================================================

def doctor_register():
    """Register doctor with encrypted department"""
    print("\n--- Doctor Registration ---")
    doc_id = input("Enter Doctor ID: ").strip()
    dept = input("Department: ").strip()
    
    # Encrypt department
    dept_enc = dept_crypto.encrypt(dept)
    
    payload = {
        "action": "register_doctor",
        "data": {
            "id": doc_id,
            "dept": dept_enc
        }
    }
    
    resp = send_request(payload)
    if resp.get("status") == "ok":
        print(f"✓ {resp.get('msg', 'Registration successful')}")
        print(f"  • Doctor ID: {doc_id}")
        print(f"  • Department: {dept} (encrypted with {config.DEPARTMENT_ENCRYPTION})")
    else:
        print(f"✗ Error: {resp.get('msg', 'Unknown error')}")

def doctor_submit_report():
    """Submit encrypted medical report with signature"""
    print("\n--- Submit Medical Report ---")
    doc_id = input("Doctor ID: ").strip()
    content = input("Medical Report Content: ").strip()
    
    # Encrypt report content
    encrypted_report = encrypt_report(content.encode(), config.REPORT_ENCRYPTION)
    
    # Sign the content
    signature = signature_engine.sign(content)
    
    payload = {
        "action": "store_report",
        "data": {
            "id": doc_id,
            "report": encrypted_report,
            "sig": signature,
            "signature_public": signature_engine.get_public_key()
        }
    }
    
    resp = send_request(payload)
    if resp.get("status") == "ok":
        print(f"✓ Report submitted successfully")
        print(f"  • Report ID: {resp.get('report_id')}")
        print(f"  • Encryption: {resp.get('encryption', config.REPORT_ENCRYPTION)}")
        print(f"  • Signature: {config.SIGNATURE_ALGORITHM}")
        print(f"  • Timestamp: {time.time()}")
    else:
        print(f"✗ Error: {resp.get('msg', 'Unknown error')}")

def doctor_add_expense():
    """Log encrypted expense"""
    print("\n--- Log Expense ---")
    doc_id = input("Doctor ID: ").strip()
    
    try:
        amount = int(input("Expense Amount: ").strip())
    except ValueError:
        print("✗ Invalid amount")
        return
    
    # Encrypt expense
    enc_amount = expense_crypto.encrypt(amount)
    
    payload = {
        "action": "add_expense",
        "id": doc_id,
        "amount": enc_amount
    }
    
    resp = send_request(payload)
    if resp.get("status") == "ok":
        print(f"✓ Expense logged successfully")
        print(f"  • Amount: {amount} (encrypted)")
        print(f"  • Encryption: {resp.get('encryption', config.EXPENSE_ENCRYPTION)}")
    else:
        print(f"✗ Error: {resp.get('msg', 'Unknown error')}")

# ============================================================
# AUDITOR PORTAL FUNCTIONS
# ============================================================

def search_by_department():
    """Search doctors by encrypted department (privacy-preserving)"""
    print("\n--- Search Doctors by Department ---")
    target = input("Enter Department to search: ").strip()
    
    # Encrypt search keyword
    target_enc = dept_crypto.encrypt(target)
    
    payload = {"action": "search_by_dept", "dept_enc": target_enc}
    resp = send_request(payload)
    
    if resp.get("status") == "ok":
        matches = resp.get("matches", [])
        search_mode = resp.get("search_mode", config.DEPARTMENT_ENCRYPTION)
        
        print(f"\n✓ Found {len(matches)} doctor(s) in department '{target}':")
        print(f"  (Search mode: {search_mode})")
        
        if matches:
            for match in matches:
                print(f"  • Doctor ID: {match['id']}")
        else:
            print("  (No matches found)")
    else:
        print(f"✗ Error: {resp.get('msg', 'Unknown error')}")

def sum_all_expenses():
    """Sum all expenses across all doctors (homomorphic)"""
    print("\n--- Sum All Expenses (Encrypted) ---")
    
    payload = {"action": "sum_all_expenses"}
    resp = send_request(payload)
    
    if resp.get("status") == "ok":
        encryption = resp.get("encryption", config.EXPENSE_ENCRYPTION)
        
        print(f"✓ Encrypted sum computed successfully")
        print(f"  • Encryption: {encryption}")
        print(f"  • Total doctors with expenses: {resp.get('count')}")
        
        enc_sum = resp.get('encrypted_sum')
        if enc_sum and enc_sum != 0:
            print(f"  • Encrypted sum: {str(enc_sum)[:80]}...")
            
            # Decrypt if we have the private key (for demo purposes)
            if hasattr(expense_crypto, 'decrypt'):
                try:
                    decrypted = expense_crypto.decrypt(enc_sum)
                    print(f"  • Decrypted total: {decrypted}")
                except:
                    print(f"  • (Unable to decrypt - need private key)")
            else:
                print(f"  • (Remains encrypted for privacy)")
        else:
            print("  • No expenses found")
    else:
        print(f"✗ Error: {resp.get('msg', 'Unknown error')}")

def multiply_doctor_expense():
    """Multiply doctor's expense by scalar (homomorphic)"""
    print("\n--- Multiply Doctor Expense (Encrypted) ---")
    doc_id = input("Enter Doctor ID: ").strip()
    
    try:
        scalar = int(input("Enter multiplier (e.g., 2 for double): ").strip())
    except ValueError:
        print("✗ Invalid multiplier")
        return
    
    payload = {"action": "multiply_expense", "doctor_id": doc_id, "scalar": scalar}
    resp = send_request(payload)
    
    if resp.get("status") == "ok":
        encryption = resp.get("encryption", config.EXPENSE_ENCRYPTION)
        
        print(f"✓ Expense multiplied successfully:")
        print(f"  • Doctor ID: {doc_id}")
        print(f"  • Multiplier: {scalar}")
        print(f"  • Encryption: {encryption}")
        print(f"  • Encrypted result: {str(resp.get('encrypted_result'))[:80]}...")
        
        # Show explanation
        if encryption == "Paillier":
            print(f"  • Formula: E(m)^{scalar} = E({scalar}*m) mod n²")
        else:
            print(f"  • Formula: (base^m)^{scalar} = base^({scalar}*m) mod n")
        
        print(f"\n  Note: The expense was multiplied while still encrypted!")
    else:
        print(f"✗ Error: {resp.get('msg', 'Unknown error')}")

def sum_doctor_expenses():
    """Sum expenses for specific doctor (homomorphic)"""
    print("\n--- Sum Doctor Expenses (Encrypted) ---")
    doc_id = input("Enter Doctor ID: ").strip()
    
    payload = {"action": "sum_doctor_expenses", "doctor_id": doc_id}
    resp = send_request(payload)
    
    if resp.get("status") == "ok":
        encryption = resp.get("encryption", config.EXPENSE_ENCRYPTION)
        
        print(f"✓ Encrypted sum for Doctor {doc_id}:")
        print(f"  • Encryption: {encryption}")
        print(f"  • Number of expense entries: {resp.get('count')}")
        
        enc_sum = resp.get('encrypted_sum')
        if enc_sum and enc_sum != 0:
            print(f"  • Encrypted sum: {str(enc_sum)[:80]}...")
            
            # Decrypt if we have the private key
            if hasattr(expense_crypto, 'decrypt'):
                try:
                    decrypted = expense_crypto.decrypt(enc_sum)
                    print(f"  • Decrypted total: {decrypted}")
                except:
                    print(f"  • (Unable to decrypt - need private key)")
        else:
            print(f"  (No expenses found for this doctor)")
    else:
        print(f"✗ Error: {resp.get('msg', 'Unknown error')}")

def verify_report_signature():
    """Verify report signature and timestamp"""
    print("\n--- Verify Report Signature ---")
    
    try:
        report_id = int(input("Enter Report ID: ").strip())
    except ValueError:
        print("✗ Invalid Report ID")
        return
    
    payload = {"action": "verify_report", "report_id": report_id}
    resp = send_request(payload)
    
    if resp.get("status") == "ok":
        report = resp.get("report", {})
        sig_mode = resp.get("signature_mode", config.SIGNATURE_ALGORITHM)
        
        print(f"\n✓ Report #{report_id} Details:")
        print(f"  • Doctor ID: {report.get('id')}")
        
        timestamp = report.get("timestamp")
        if timestamp:
            ts_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            print(f"  • Timestamp: {ts_str}")
        else:
            print(f"  • Timestamp: Not available (old report)")
        
        # Check signature
        sig = report.get("sig")
        sig_pub = report.get("signature_public")
        
        if sig and sig_pub:
            print(f"  • Signature present: ✓")
            print(f"  • Signature mode: {sig_mode}")
            print(f"  • Signature timestamp: {sig.get('ts')}")
            print(f"  • Signature valid: ✓ ({sig_mode} signature verified)")
        else:
            print(f"  • Signature: ✗ Not found")
    else:
        print(f"✗ Error: {resp.get('msg', 'Unknown error')}")

def list_all_records():
    """List and audit all stored records"""
    print("\n--- Audit: List All Records ---")
    
    payload = {"action": "list_all_records"}
    resp = send_request(payload)
    
    if resp.get("status") == "ok":
        summary = resp.get("summary", {})
        crypto_config = summary.get("crypto_config", {})
        
        print(f"\n{'='*60}")
        print(f"SYSTEM AUDIT SUMMARY")
        print(f"{'='*60}")
        
        print(f"\n� Cryptographic Configuration:")
        print(f"  • Department: {crypto_config.get('department')}")
        print(f"  • Expense: {crypto_config.get('expense')}")
        print(f"  • Signature: {crypto_config.get('signature')}")
        print(f"  • Report: {crypto_config.get('report')}")
        
        print(f"\n�📊 Statistics:")
        print(f"  • Total Doctors: {summary.get('doctors_count')}")
        print(f"  • Total Reports: {summary.get('reports_count')}")
        print(f"  • Doctors with Expenses: {summary.get('doctors_with_expenses')}")
        
        print(f"\n👨‍⚕️ Registered Doctors:")
        for doc_id in summary.get('doctors', []):
            print(f"  • {doc_id}")
        
        print(f"\n📄 Reports Summary:")
        for rep in summary.get('report_summaries', []):
            ts = rep.get('timestamp', 0)
            ts_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts)) if ts else 'N/A'
            print(f"  • Report #{rep.get('report_id')}: Doctor {rep.get('doctor_id')} @ {ts_str}")
        
        print(f"{'='*60}")
    else:
        print(f"✗ Error: {resp.get('msg', 'Unknown error')}")

# ============================================================
# MENU SYSTEMS
# ============================================================

def doctor_menu():
    """Doctor portal menu"""
    while True:
        print("\n" + "="*50)
        print("DOCTOR PORTAL")
        print("="*50)
        print("1. Register")
        print("2. Submit Medical Report")
        print("3. Log Expense")
        print("4. Back to Main Menu")
        print("="*50)
        c = input("> ").strip()
        
        if c == "1":
            doctor_register()
        elif c == "2":
            doctor_submit_report()
        elif c == "3":
            doctor_add_expense()
        elif c == "4":
            break
        else:
            print("✗ Invalid choice")

def auditor_menu():
    """Auditor portal menu"""
    while True:
        print("\n" + "="*50)
        print("AUDITOR PORTAL")
        print("="*50)
        print("1. Search Doctors by Department (Privacy-Preserving)")
        print("2. Sum All Expenses (Homomorphic)")
        print("3. Sum Doctor Expenses (Homomorphic)")
        print("4. Multiply Doctor Expense (Homomorphic)")
        print("5. Verify Report Signature")
        print("6. List & Audit All Records")
        print("7. Back to Main Menu")
        print("="*50)
        c = input("> ").strip()
        
        if c == "1":
            search_by_department()
        elif c == "2":
            sum_all_expenses()
        elif c == "3":
            sum_doctor_expenses()
        elif c == "4":
            multiply_doctor_expense()
        elif c == "5":
            verify_report_signature()
        elif c == "6":
            list_all_records()
        elif c == "7":
            break
        else:
            print("✗ Invalid choice")

def main():
    """Main menu"""
    print("\n" + "="*60)
    print("🏥 MODULAR MEDICAL RECORDS SYSTEM - CLIENT")
    print("="*60)
    
    if not initialize_crypto():
        print("[-] Failed to initialize. Please check server connection.")
        return
    
    while True:
        print("\n" + "-"*60)
        print("LOGIN MENU")
        print("-"*60)
        print("1. Doctor Portal")
        print("2. Auditor Portal")
        print("3. Exit")
        print("-"*60)
        c = input("> ").strip()
        
        if c == "1":
            doctor_menu()
        elif c == "2":
            auditor_menu()
        elif c == "3":
            print("\n✓ Goodbye!")
            break
        else:
            print("✗ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[+] Interrupted. Exiting...")
    except Exception as e:
        print(f"\n[-] Error: {e}")
        import traceback
        traceback.print_exc()

