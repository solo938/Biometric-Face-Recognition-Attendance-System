import faiss
import sqlite3
import pickle
import json
import numpy as np
from config import DB_PATH, FAISS_INDEX, ID_MAP, NAME_MAP


def build_index() -> None:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT emp_id, name, embedding FROM employees").fetchall()
    conn.close()

    if not rows:
        print("No employees in database. Run register_employee.py first."); return

    index    = faiss.IndexFlatIP(512)   
    id_map   = []
    name_map = {}

    for emp_id, name, emb_blob in rows:
        emb = pickle.loads(emb_blob).astype(np.float32)
        emb = emb / np.linalg.norm(emb)
        index.add(emb.reshape(1, -1))
        id_map.append(emp_id)
        name_map[emp_id] = name

    faiss.write_index(index, str(FAISS_INDEX))
    np.save(str(ID_MAP), np.array(id_map))
    with open(NAME_MAP, "w") as f:
        json.dump(name_map, f, indent=2)

    print(f"FAISS index built: {len(rows)} employee(s) indexed.")
    print(f"  face_index.faiss  -> {FAISS_INDEX}")
    print(f"  id_map.npy        -> {ID_MAP}")
    print(f"  name_map.json     -> {NAME_MAP}")
    print("\nNext step: python attendance_system.py  OR  python dashboard.py")


if __name__ == "__main__":
    build_index()
