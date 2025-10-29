"""
Modular Medical Records Server
Supports multiple cryptographic algorithms configured in config.py
"""

import json
import threading
import socket
import time
from threading import Lock
import config
from crypto_utils import DepartmentCrypto, ExpenseCrypto

DB_FILE = config.DATABASE_FILE
lock = Lock()

# Initialize cryptographic engines based on config
dept_crypto = DepartmentCrypto(config.DEPARTMENT_ENCRYPTION)
expense_crypto = ExpenseCrypto(config.EXPENSE_ENCRYPTION)

# Persistent DB init
try:
    with open(DB_FILE) as f:
        db = json.load(f)
except:
    db = {"doctors": {}, "reports": [], "expenses": {}}

def save_db():
    """Save database to file"""
    with lock:
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=2)

def handle_client(conn):
    """Handle client requests"""
    try:
        data = conn.recv(655360).decode()
        req = json.loads(data)
        action = req["action"]

        if action == "get_crypto_config":
            # Send current crypto configuration
            response = {
                "status": "ok",
                "config": {
                    "key_encryption": config.KEY_ENCRYPTION_ALGORITHM,
                    "signature": config.SIGNATURE_ALGORITHM,
                    "signature_hash": config.SIGNATURE_HASH,
                    "department": config.DEPARTMENT_ENCRYPTION,
                    "expense": config.EXPENSE_ENCRYPTION,
                    "report": config.REPORT_ENCRYPTION
                },
                "department_public": dept_crypto.get_public_key(),
                "expense_public": expense_crypto.get_public_key()
            }
            conn.send(json.dumps(response).encode())

        elif action == "register_doctor":
            d = req["data"]
            db["doctors"][d["id"]] = d
            db["doctors"][d["id"]]["registered_at"] = time.time()
            save_db()
            conn.send(json.dumps({
                "status": "ok",
                "msg": f"Doctor registered (Dept: {config.DEPARTMENT_ENCRYPTION})"
            }).encode())

        elif action == "store_report":
            report = req["data"]
            report["timestamp"] = time.time()
            report["report_id"] = len(db["reports"])
            db["reports"].append(report)
            save_db()
            conn.send(json.dumps({
                "status": "ok",
                "report_id": report["report_id"],
                "encryption": config.REPORT_ENCRYPTION
            }).encode())

        elif action == "add_expense":
            d_id = req["id"]
            enc_amount = req["amount"]
            
            if d_id not in db["expenses"]:
                db["expenses"][d_id] = enc_amount
            else:
                # Homomorphic addition
                db["expenses"][d_id] = expense_crypto.homomorphic_add(
                    db["expenses"][d_id],
                    enc_amount
                )
            save_db()
            conn.send(json.dumps({
                "status": "ok",
                "encryption": config.EXPENSE_ENCRYPTION
            }).encode())

        elif action == "get_doctors":
            conn.send(json.dumps({"status": "ok", "doctors": db["doctors"]}).encode())

        elif action == "get_reports":
            conn.send(json.dumps({"status": "ok", "reports": db["reports"]}).encode())

        elif action == "get_expenses":
            conn.send(json.dumps({"status": "ok", "expenses": db["expenses"]}).encode())

        elif action == "search_by_dept":
            # Privacy-preserving department search
            target_dept = req["dept_enc"]
            matches = []
            
            for doc_id, doc_data in db["doctors"].items():
                if doc_data.get("dept") == target_dept:
                    matches.append({
                        "id": doc_id,
                        "dept_enc": doc_data["dept"]
                    })
            
            conn.send(json.dumps({
                "status": "ok",
                "matches": matches,
                "search_mode": config.DEPARTMENT_ENCRYPTION
            }).encode())

        elif action == "sum_all_expenses":
            # Sum all encrypted expenses (homomorphic)
            if not db["expenses"]:
                conn.send(json.dumps({
                    "status": "ok",
                    "encrypted_sum": 0,
                    "count": 0
                }).encode())
            else:
                expenses_list = list(db["expenses"].values())
                
                if len(expenses_list) == 1:
                    total_enc = expenses_list[0]
                else:
                    total_enc = expenses_list[0]
                    for enc_exp in expenses_list[1:]:
                        total_enc = expense_crypto.homomorphic_add(total_enc, enc_exp)
                
                conn.send(json.dumps({
                    "status": "ok",
                    "encrypted_sum": total_enc,
                    "count": len(db["expenses"]),
                    "encryption": config.EXPENSE_ENCRYPTION
                }).encode())

        elif action == "sum_doctor_expenses":
            # Sum expenses for specific doctor
            doc_id = req["doctor_id"]
            
            if doc_id not in db["expenses"]:
                conn.send(json.dumps({
                    "status": "ok",
                    "encrypted_sum": 0,
                    "count": 0
                }).encode())
            else:
                conn.send(json.dumps({
                    "status": "ok",
                    "encrypted_sum": db["expenses"][doc_id],
                    "count": 1,
                    "encryption": config.EXPENSE_ENCRYPTION
                }).encode())

        elif action == "multiply_expense":
            # Multiply a doctor's expense by a scalar
            doc_id = req["doctor_id"]
            scalar = req["scalar"]
            
            if doc_id not in db["expenses"]:
                conn.send(json.dumps({
                    "status": "error",
                    "msg": "Doctor has no expenses"
                }).encode())
            else:
                # Get current encrypted expense
                current_enc = db["expenses"][doc_id]
                
                # Multiply homomorphically
                multiplied_enc = expense_crypto.homomorphic_multiply(current_enc, scalar)
                
                # Update in database
                db["expenses"][doc_id] = multiplied_enc
                save_db()
                
                conn.send(json.dumps({
                    "status": "ok",
                    "msg": f"Expense multiplied by {scalar}",
                    "encrypted_result": multiplied_enc,
                    "encryption": config.EXPENSE_ENCRYPTION
                }).encode())

        elif action == "verify_report":
            # Get report for verification
            report_id = req["report_id"]
            
            if report_id >= len(db["reports"]):
                conn.send(json.dumps({
                    "status": "error",
                    "msg": "Report not found"
                }).encode())
            else:
                report = db["reports"][report_id]
                conn.send(json.dumps({
                    "status": "ok",
                    "report": report,
                    "signature_mode": config.SIGNATURE_ALGORITHM
                }).encode())

        elif action == "list_all_records":
            # List all records with metadata
            summary = {
                "doctors_count": len(db["doctors"]),
                "reports_count": len(db["reports"]),
                "doctors_with_expenses": len(db["expenses"]),
                "doctors": list(db["doctors"].keys()),
                "report_summaries": [
                    {
                        "report_id": i,
                        "doctor_id": r.get("id"),
                        "timestamp": r.get("timestamp")
                    } for i, r in enumerate(db["reports"])
                ],
                "crypto_config": {
                    "department": config.DEPARTMENT_ENCRYPTION,
                    "expense": config.EXPENSE_ENCRYPTION,
                    "signature": config.SIGNATURE_ALGORITHM,
                    "report": config.REPORT_ENCRYPTION
                }
            }
            conn.send(json.dumps({
                "status": "ok",
                "summary": summary
            }).encode())

        else:
            conn.send(json.dumps({
                "status": "error",
                "msg": "Unknown action"
            }).encode())

    except Exception as e:
        conn.send(json.dumps({
            "status": "error",
            "msg": str(e)
        }).encode())

    conn.close()

def main():
    """Start the server"""
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((config.SERVER_HOST, config.SERVER_PORT))
    s.listen(5)
    
    print("\n" + "="*60)
    print("🏥 MODULAR MEDICAL RECORDS SERVER")
    print("="*60)
    print(f"Listening on {config.SERVER_HOST}:{config.SERVER_PORT}")
    print(f"Database: {DB_FILE}")
    print("\n📋 Active Cryptographic Configuration:")
    print(f"  • Department Search : {config.DEPARTMENT_ENCRYPTION}")
    print(f"  • Expense Tracking  : {config.EXPENSE_ENCRYPTION}")
    print(f"  • Digital Signature : {config.SIGNATURE_ALGORITHM}")
    print(f"  • Signature Hashing : {config.SIGNATURE_HASH}")
    print(f"  • Report Encryption : {config.REPORT_ENCRYPTION}")
    print(f"  • Key Encryption    : {config.KEY_ENCRYPTION_ALGORITHM}")
    print("\n✓ Ready to accept connections...")
    print("="*60 + "\n")
    
    while True:
        c, addr = s.accept()
        print(f"[+] Connection from {addr}")
        threading.Thread(target=handle_client, args=(c,), daemon=True).start()

if __name__ == "__main__":
    main()
