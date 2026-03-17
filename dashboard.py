import cv2
import sqlite3
import pandas as pd
import gradio as gr
from datetime import datetime
from config import DB_PATH, HOST, PORT
import os
import numpy as np
import threading


# ── CSS ────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --red:       #C8102E;
    --red-dark:  #A00D24;
    --red-light: #FFE8EC;
    --white:     #FFFFFF;
    --off-white: #F7F7F8;
    --slate:     #1A1A2E;
    --slate-mid: #4A4A6A;
    --border:    #E8E8F0;
    --shadow:    0 2px 16px rgba(200,16,46,0.08);
    --radius:    10px;
}
body, .gradio-container {
    background: var(--off-white) !important;
    font-family: 'DM Sans', sans-serif !important;
}
#header {
    background: linear-gradient(135deg, #1A1A2E 0%, #2D1B4E 100%);
    border-radius: var(--radius);
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
#header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, var(--red) 0%, #FF4D6D 100%);
}
#header::after {
    content: 'DA';
    position: absolute;
    right: 32px; top: 50%;
    transform: translateY(-50%);
    font-family: 'Bebas Neue', sans-serif;
    font-size: 96px;
    color: rgba(255,255,255,0.04);
    pointer-events: none;
}
#header h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 38px !important;
    letter-spacing: 3px !important;
    color: white !important;
    margin: 0 0 4px 0 !important;
    line-height: 1 !important;
}
#header p {
    color: rgba(255,255,255,0.5) !important;
    font-size: 12px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    margin: 0 !important;
}
.tabs > .tab-nav {
    background: var(--white) !important;
    border-bottom: 2px solid var(--border) !important;
    border-radius: var(--radius) var(--radius) 0 0 !important;
    padding: 0 16px !important;
}
.tabs > .tab-nav button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    color: #8888AA !important;
    padding: 14px 20px !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    background: transparent !important;
    border-radius: 0 !important;
    transition: all 0.2s !important;
}
.tabs > .tab-nav button:hover { color: var(--red) !important; }
.tabs > .tab-nav button.selected {
    color: var(--red) !important;
    border-bottom-color: var(--red) !important;
    font-weight: 600 !important;
}
.tabitem {
    background: var(--white) !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
    padding: 28px !important;
    box-shadow: var(--shadow) !important;
}
.section-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 22px !important;
    letter-spacing: 2px !important;
    color: var(--slate) !important;
    margin-bottom: 16px !important;
    padding-bottom: 10px !important;
    border-bottom: 2px solid var(--red-light) !important;
}
.date-chip {
    display: inline-block;
    background: var(--red-light);
    color: var(--red);
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 20px;
}
button.primary {
    background: linear-gradient(135deg, var(--red) 0%, var(--red-dark) 100%) !important;
    border: none !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 16px rgba(200,16,46,0.25) !important;
    transition: all 0.2s !important;
}
button.primary:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(200,16,46,0.35) !important;
}
button.secondary {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--slate) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}
button.secondary:hover {
    border-color: var(--red) !important;
    color: var(--red) !important;
}
label span {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    color: var(--slate-mid) !important;
}
.label-container .label-text {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 48px !important;
    color: var(--red) !important;
    letter-spacing: 2px !important;
}
table { font-family: 'DM Sans', sans-serif !important; font-size: 13px !important; }
thead th {
    background: var(--off-white) !important;
    color: var(--slate-mid) !important;
    font-weight: 600 !important;
    font-size: 11px !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    padding: 10px 14px !important;
    border-bottom: 2px solid var(--border) !important;
}
tbody td { padding: 10px 14px !important; border-bottom: 1px solid var(--border) !important; }
tbody tr:hover td { background: var(--red-light) !important; }
"""



def _ensure_db():
    os.makedirs(os.path.dirname(str(DB_PATH)), exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""CREATE TABLE IF NOT EXISTS employees (
        emp_id TEXT PRIMARY KEY, name TEXT NOT NULL,
        department TEXT, embedding BLOB NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT, emp_id TEXT,
        date TEXT, check_in_time TEXT, status TEXT DEFAULT 'Present',
        FOREIGN KEY(emp_id) REFERENCES employees(emp_id),
        UNIQUE(emp_id, date))""")
    conn.commit(); conn.close()

_ensure_db()



_ready           = False
_recognize_faces = None
_mark_attendance = None

def _load_recognition():
    global _ready, _recognize_faces, _mark_attendance
    if _ready:
        return True
    from config import FAISS_INDEX
    if not os.path.exists(str(FAISS_INDEX)):
        return False
    try:
        from core.recognition import recognize_faces, mark_attendance
        _recognize_faces = recognize_faces
        _mark_attendance = mark_attendance
        _ready = True
        return True
    except Exception as e:
        print(f"Recognition load error: {e}"); return False



_processing = False
_lock        = threading.Lock()


_last_seen: dict = {}   
DB_COOLDOWN_SECS = 5



def process_frame(frame):
    global _processing

    if frame is None:
        return None, "Waiting for camera..."

    
    with _lock:
        if _processing:
            return frame, "Processing..."
        _processing = True

    try:
        
        h, w = frame.shape[:2]
        scale = 640 / max(h, w)
        if scale < 1.0:
            small = cv2.resize(frame, (int(w * scale), int(h * scale)))
        else:
            small = frame.copy()

        
        frame_bgr = small[:, :, ::-1].copy()

        if not _load_recognition():
            cv2.putText(frame_bgr,
                        "Run register_employee.py then faiss_index.py",
                        (10, 36), cv2.FONT_HERSHEY_DUPLEX, 0.65, (200, 16, 46), 2)
            return frame_bgr[:, :, ::-1], (
                "FAISS index not found.\n"
                "Run: python3 register_employee.py\n"
                "Then: python3 faiss_index.py"
            )

        results = _recognize_faces(frame_bgr)
        lines   = []
        now     = datetime.now()

        for emp_id, name, similarity, box in results:

            
            last = _last_seen.get(emp_id)
            if emp_id and last and (now - last).seconds < DB_COOLDOWN_SECS:
                
                msg   = "Present"
                color = (0, 200, 80)
            else:
                msg, color = _mark_attendance(emp_id)
                if emp_id:
                    _last_seen[emp_id] = now

            
            cv2.rectangle(frame_bgr,
                          (box[0], box[1]), (box[2], box[3]), color, 2)
            cv2.rectangle(frame_bgr,
                          (box[0], box[1] - 32), (box[2], box[1]), color, cv2.FILLED)
            cv2.putText(frame_bgr,
                        f"  {name}  |  {msg}",
                        (box[0], box[1] - 9),
                        cv2.FONT_HERSHEY_DUPLEX, 0.52, (255, 255, 255), 1)
            lines.append(f"{name}  —  {msg}")

        status = "\n".join(lines) if lines else "No face detected"

        
        return frame_bgr[:, :, ::-1], status

    finally:
        
        with _lock:
            _processing = False



def load_today():
    _ensure_db()
    today = datetime.now().strftime("%Y-%m-%d")
    conn  = sqlite3.connect(str(DB_PATH))
    df = pd.read_sql("""
        SELECT a.emp_id "ID", e.name "Name", e.department "Department",
               a.check_in_time "Check-In", a.status "Status"
        FROM attendance a JOIN employees e ON a.emp_id=e.emp_id
        WHERE a.date=? ORDER BY a.check_in_time
    """, conn, params=(today,))
    conn.close()
    return {str(len(df)): 1.0}, df


def export_csv():
    _ensure_db()
    conn = sqlite3.connect(str(DB_PATH))
    df = pd.read_sql("""
        SELECT a.date "Date", a.emp_id "ID", e.name "Name",
               e.department "Dept", a.check_in_time "Check-In", a.status "Status"
        FROM attendance a JOIN employees e ON a.emp_id=e.emp_id
        ORDER BY a.date DESC, a.check_in_time
    """, conn); conn.close()
    os.makedirs("logs", exist_ok=True)
    path = "logs/attendance_export.csv"
    df.to_csv(path, index=False)
    return path, df.head(100)



with gr.Blocks(title="Daloft Aerospace — Biometric Attendance", css=CSS) as demo:

    gr.HTML("""
    <div id="header">
        <h1>DALOFT AEROSPACE</h1>
        <p>Biometric Face Recognition &nbsp;·&nbsp; Attendance System</p>
    </div>
    """)

    with gr.Tabs():

        
        with gr.TabItem("  Live Attendance"):
            with gr.Row(equal_height=True):

                with gr.Column(scale=3):
                    cam_in = gr.Image(
                        sources=["webcam"],
                        streaming=True,
                        type="numpy",
                        label="Camera Feed",
                        height=440,
                        webcam_options=gr.WebcamOptions(mirror=True),
                    )

                with gr.Column(scale=2):
                    gr.HTML('<div class="section-title">RECOGNITION STATUS</div>')
                    cam_out = gr.Image(
                        label="Processed Output",
                        height=300,
                        interactive=False,
                        show_label=False,
                    )
                    status_box = gr.Textbox(
                        label="Last Event",
                        lines=4,
                        interactive=False,
                        placeholder="Start the camera to begin scanning...",
                    )
                    gr.HTML("""
                    <div style="display:flex;gap:16px;padding:10px 14px;
                                background:#F7F7F8;border-radius:8px;
                                border:1px solid #E8E8F0;margin-top:8px;">
                        <span style="font-size:12px;font-weight:600;color:#1A1A2E">
                            🟢 Marked &nbsp;·&nbsp; 🟠 Already in &nbsp;·&nbsp; 🔴 Unknown
                        </span>
                    </div>
                    """)

            cam_in.stream(
                fn=process_frame,
                inputs=[cam_in],
                outputs=[cam_out, status_box],
                stream_every=0.1,       
                time_limit=3600,
                show_progress=False,
            )

        # ── Tab 2: Today's Attendance ──────────────────────────────
        with gr.TabItem("  Today's Attendance"):
            gr.HTML(f"""
            <div class="section-title">ATTENDANCE REGISTER</div>
            <div class="date-chip"> {datetime.now().strftime('%A, %d %B %Y')}</div>
            """)
            with gr.Row():
                with gr.Column(scale=1):
                    count_lbl = gr.Label(label="Present Today")
                with gr.Column(scale=5):
                    refresh_btn = gr.Button("↻  Refresh", variant="secondary", size="sm")
            today_tbl = gr.Dataframe(interactive=False, show_label=False)
            refresh_btn.click(fn=load_today, outputs=[count_lbl, today_tbl])
            demo.load(fn=load_today, outputs=[count_lbl, today_tbl])

        # ── Tab 3: Export ──────────────────────────────────────────
        with gr.TabItem("⬇  Export CSV"):
            gr.HTML('<div class="section-title">EXPORT RECORDS</div>')
            with gr.Row():
                with gr.Column(scale=1):
                    export_btn  = gr.Button("⬇  Generate CSV", variant="primary")
                    export_file = gr.File(label="Download")
                with gr.Column(scale=3):
                    preview_tbl = gr.Dataframe(
                        label="Preview — Last 100 Records",
                        interactive=False,
                    )
            export_btn.click(fn=export_csv, outputs=[export_file, preview_tbl])


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=PORT,
    )