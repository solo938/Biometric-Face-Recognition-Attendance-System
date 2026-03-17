import cv2
import numpy as np
import pickle
import sqlite3
from insightface.app import FaceAnalysis
from config import DB_PATH, CTX_ID, DET_SIZE
from scripts.init_db import init_db


app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=CTX_ID, det_size=(DET_SIZE, DET_SIZE))


def register_employee(emp_id: str, name: str, dept: str) -> None:
    init_db()
    cap = cv2.VideoCapture(0)
    embeddings = []
    print(f"\nRegistering {name} ({emp_id})")
    print("Look at the camera. Press 'k' to capture (need 8 total), 'q' to quit early.\n")

    while len(embeddings) < 4:
        ret, frame = cap.read()
        if not ret:
            print("Camera read failed."); break

        frame = cv2.flip(frame, 1)
        faces = app.get(frame)

        
        for face in faces:
            box = face.bbox.astype(int)
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

        cv2.putText(
            frame,
            f"Captured: {len(embeddings)}/4  |  Press 'k' to capture",
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2,
        )
        cv2.imshow("Register Employee — Press Q to quit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("k") and len(faces) == 1:
            embeddings.append(faces[0].normed_embedding)
            print(f"  Captured {len(embeddings)}/4")
        elif key == ord("q"):
            print("  Quit early."); break

    cap.release()
    cv2.destroyAllWindows()

    if len(embeddings) < 4:
        print(f"Not enough captures ({len(embeddings)}). Need at least 4. Try again.")
        return

    avg_embedding = np.mean(embeddings, axis=0).astype(np.float32)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO employees VALUES (?,?,?,?)",
        (emp_id, name, dept, pickle.dumps(avg_embedding)),
    )
    conn.commit(); conn.close()
    print(f"\n{name} ({emp_id}) registered successfully with {len(embeddings)} captures!")



EMPLOYEES = [
    {"emp_id": "DA-INT-007", "name": "SAHARIAR HASAN",    "dept": "AI intern"},
    
    
]

if __name__ == "__main__":
    for emp in EMPLOYEES:
        register_employee(emp["emp_id"], emp["name"], emp["dept"])
    print("\nAll employees registered. Now run: python faiss_index.py")
