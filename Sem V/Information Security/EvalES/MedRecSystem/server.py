import json, threading, socket, time
from crypto_utils import rsa_homo_add
from threading import Lock

DB_FILE = "storage.json"
lock = Lock()

# Persistent DB init
try:
    with open(DB_FILE) as f:
        db = json.load(f)
except:
    db = {"doctors": {}, "reports": [], "expenses": {}}

def save_db():
    with lock:
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=2)

def handle_client(conn):
    try:
        data = conn.recv(65536).decode()
        req = json.loads(data)
        action = req["action"]

        if action == "register_doctor":
            d = req["data"]
            db["doctors"][d["id"]] = d
            db["doctors"][d["id"]]["registered_at"] = time.time()
            save_db()
            conn.send(json.dumps({"status": "ok", "msg": "Doctor registered successfully"}).encode())

        elif action == "store_report":
            report = req["data"]
            report["timestamp"] = time.time()
            report["report_id"] = len(db["reports"])
            db["reports"].append(report)
            save_db()
            conn.send(json.dumps({"status": "ok", "report_id": report["report_id"]}).encode())

        elif action == "add_expense":
            d_id = req["id"]
            if d_id not in db["expenses"]:
                db["expenses"][d_id] = req["amount"]
            else:
                db["expenses"][d_id] = rsa_homo_add(
                    db["expenses"][d_id],
                    req["amount"],
                    req["n"]
                )
            save_db()
            conn.send(json.dumps({"status": "ok"}).encode())

        elif action == "get_doctors":
            conn.send(json.dumps({"status": "ok", "doctors": db["doctors"]}).encode())

        elif action == "get_reports":
            conn.send(json.dumps({"status": "ok", "reports": db["reports"]}).encode())

        elif action == "get_expenses":
            conn.send(json.dumps({"status": "ok", "expenses": db["expenses"]}).encode())

        elif action == "search_by_dept":
            # Search doctors by encrypted department (exact match)
            target_dept = req["dept_enc"]
            matches = []
            for doc_id, doc_data in db["doctors"].items():
                if doc_data.get("dept") == target_dept:
                    matches.append({
                        "id": doc_id,
                        "dept_enc": doc_data["dept"]
                    })
            conn.send(json.dumps({"status": "ok", "matches": matches}).encode())

        elif action == "sum_all_expenses":
            # Sum all encrypted expenses using homomorphic property
            if not db["expenses"]:
                conn.send(json.dumps({"status": "ok", "encrypted_sum": 0, "count": 0}).encode())
            else:
                n = req["n"]
                e = req["e"]
                # Start with encryption of 0: 0^e mod n = 0
                # But we need identity for multiplication, which is 1
                # Actually, let's get the first value and multiply the rest
                expenses_list = list(db["expenses"].values())
                if len(expenses_list) == 1:
                    total_enc = expenses_list[0]
                else:
                    total_enc = expenses_list[0]
                    for enc_exp in expenses_list[1:]:
                        total_enc = rsa_homo_add(total_enc, enc_exp, n)
                conn.send(json.dumps({
                    "status": "ok",
                    "encrypted_sum": total_enc,
                    "count": len(db["expenses"])
                }).encode())

        elif action == "sum_doctor_expenses":
            # Sum encrypted expenses for specific doctor
            doc_id = req["doctor_id"]
            if doc_id not in db["expenses"]:
                conn.send(json.dumps({"status": "ok", "encrypted_sum": 0, "count": 0}).encode())
            else:
                conn.send(json.dumps({
                    "status": "ok",
                    "encrypted_sum": db["expenses"][doc_id],
                    "count": 1
                }).encode())

        elif action == "verify_report":
            # Return report data for verification
            report_id = req["report_id"]
            if report_id >= len(db["reports"]):
                conn.send(json.dumps({"status": "error", "msg": "Report not found"}).encode())
            else:
                report = db["reports"][report_id]
                conn.send(json.dumps({"status": "ok", "report": report}).encode())

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
                ]
            }
            conn.send(json.dumps({"status": "ok", "summary": summary}).encode())

        else:
            conn.send(json.dumps({"status": "error", "msg": "Unknown action"}).encode())

    except Exception as e:
        conn.send(json.dumps({"status": "error", "msg": str(e)}).encode())

    conn.close()

def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", 9999))
    s.listen(5)
    print("\n" + "="*60)
    print("🏥 MEDICAL RECORDS SERVER STARTED")
    print("="*60)
    print(f"Listening on localhost:9999")
    print(f"Database: {DB_FILE}")
    print(f"✓ Ready to accept connections...")
    print("="*60 + "\n")
    
    while True:
        c, addr = s.accept()
        print(f"[+] Connection from {addr}")
        threading.Thread(target=handle_client, args=(c,), daemon=True).start()

if __name__ == "__main__":
    main()
