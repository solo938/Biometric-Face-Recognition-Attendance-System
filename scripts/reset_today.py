import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sqlite3
from datetime import datetime
from config import DB_PATH

today = datetime.now().strftime("%Y-%m-%d")
conn  = sqlite3.connect(str(DB_PATH))
rows  = conn.execute("DELETE FROM attendance WHERE date=?", (today,)).rowcount
conn.commit(); conn.close()
print(f"Deleted {rows} attendance record(s) for {today}.")
