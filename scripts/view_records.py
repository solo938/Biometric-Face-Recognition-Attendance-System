import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sqlite3, pandas as pd
from datetime import datetime
from config import DB_PATH

conn = sqlite3.connect(str(DB_PATH))

print("=" * 55)
print("REGISTERED EMPLOYEES")
print("=" * 55)
df_emp = pd.read_sql("SELECT emp_id, name, department FROM employees", conn)
print(df_emp.to_string(index=False) if not df_emp.empty else "(none yet)")

print()
print("=" * 55)
print(f"TODAY'S ATTENDANCE  [{datetime.now().strftime('%Y-%m-%d')}]")
print("=" * 55)
today = datetime.now().strftime("%Y-%m-%d")
df_today = pd.read_sql("""
    SELECT a.emp_id, e.name, a.check_in_time, a.status
    FROM attendance a JOIN employees e ON a.emp_id = e.emp_id
    WHERE a.date = ?
    ORDER BY a.check_in_time
""", conn, params=(today,))

if df_today.empty:
    print("No attendance marked today.")
else:
    print(df_today.to_string(index=False))
    print(f"\nPresent: {len(df_today)} / {len(df_emp)}")

conn.close()
