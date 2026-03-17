import faiss
import json
import pickle
import sqlite3
import numpy as np
from datetime import datetime
from insightface.app import FaceAnalysis
from config import DB_PATH, FAISS_INDEX, ID_MAP, NAME_MAP, CTX_ID, DET_SIZE, THRESHOLD



face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=CTX_ID, det_size=(DET_SIZE, DET_SIZE))


def load_index():
    """Load FAISS index + maps from disk. Call after build_index()."""
    index   = faiss.read_index(str(FAISS_INDEX))
    id_map  = np.load(str(ID_MAP), allow_pickle=True)
    with open(NAME_MAP) as f:
        name_map = json.load(f)
    return index, id_map, name_map



try:
    _index, _id_map, _name_map = load_index()
    print(f"FAISS index loaded: {_index.ntotal} employee(s)")
except FileNotFoundError:
    _index = _id_map = _name_map = None
    print("WARNING: face_index.faiss not found. Run faiss_index.py first.")


def recognize_faces(frame_bgr: np.ndarray) -> list:
    """
    Run InsightFace on a BGR frame.
    Returns list of (emp_id | None, name, similarity, bbox_array).
    """
    if _index is None:
        raise RuntimeError("FAISS index not loaded. Run faiss_index.py first.")

    results = []
    for face in face_app.get(frame_bgr):
        emb = face.normed_embedding.astype(np.float32)
        emb = emb / np.linalg.norm(emb)
        D, I = _index.search(emb.reshape(1, -1), 1)
        sim    = float(D[0][0])
        emp_id = _id_map[I[0][0]] if sim > THRESHOLD else None
        name   = _name_map.get(emp_id, f"Unknown ({sim:.2f})") if emp_id else f"Unknown ({sim:.2f})"
        results.append((emp_id, name, sim, face.bbox.astype(int)))
    return results



_db = sqlite3.connect(str(DB_PATH), check_same_thread=False)


def mark_attendance(emp_id: str | None) -> tuple[str, tuple]:
    """
    Mark attendance for emp_id if not already marked today.
    Returns (status_message, BGR_color).
    """
    if emp_id is None:
        return "Unknown person", (0, 0, 255)           # red

    today = datetime.now().strftime("%Y-%m-%d")
    exists = _db.execute(
        "SELECT id FROM attendance WHERE emp_id=? AND date=?", (emp_id, today)
    ).fetchone()

    if exists:
        return "Already marked today", (255, 165, 0)   

    time_now = datetime.now().strftime("%H:%M:%S")
    _db.execute(
        "INSERT INTO attendance (emp_id, date, check_in_time) VALUES (?,?,?)",
        (emp_id, today, time_now),
    )
    _db.commit()
    return f"Marked at {time_now}", (0, 255, 0)        
