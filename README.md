<div align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/InsightFace-ArcFace-FF4D6D?style=for-the-badge&logo=academia&logoColor=white" />
<img src="https://img.shields.io/badge/Gradio-5.50-FF7C00?style=for-the-badge&logo=gradio&logoColor=white" />
<img src="https://img.shields.io/badge/FAISS-Vector_Search-00C7B7?style=for-the-badge&logo=meta&logoColor=white" />
<img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge" />

<br /><br />

```
██████╗  █████╗ ██╗      ██████╗ ███████╗████████╗
██╔══██╗██╔══██╗██║     ██╔═══██╗██╔════╝╚══██╔══╝
██║  ██║███████║██║     ██║   ██║█████╗     ██║   
██║  ██║██╔══██║██║     ██║   ██║██╔══╝     ██║   
██████╔╝██║  ██║███████╗╚██████╔╝██║        ██║   
╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝        ╚═╝  
```

# Biometric Face Recognition Attendance System

**Production-ready AI attendance system using ArcFace + FAISS + Gradio**  
*Real-time face recognition · Auto attendance marking · Web dashboard · CSV export*

[🚀 Quick Start](#-quick-start) · [✨ Features](#-features) · [📸 How It Works](#-how-it-works) · [⚙️ Configuration](#️-configuration) · [🗂️ Project Structure](#️-project-structure) · [🤝 Contributing](#-contributing)

</div>

---

## 🎯 What Is This?

A **production-grade biometric attendance system** that uses state-of-the-art face recognition to automatically mark employee attendance in real time — no ID cards, no PINs, no manual entry.

Built for organizations that need a reliable, privacy-conscious attendance system that works out of the box on any hardware, with or without a GPU.

```
Webcam Feed  →  InsightFace (ArcFace)  →  FAISS Vector Search  →  SQLite DB
     ↓                                                                  ↓
 Live Preview  ←──────────── Gradio Web Dashboard ──────────→  CSV Export
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🧠 **ArcFace Recognition** | State-of-the-art `buffalo_l` model, >99% accuracy in real conditions |
| ⚡ **FAISS Vector Search** | Sub-millisecond similarity search, scales to 10,000+ employees |
| 🌐 **Web Dashboard** | Gradio 5 UI — works in any browser, no installation needed |
| 📋 **Auto Attendance** | One-time daily marking with duplicate prevention |
| 📊 **CSV Export** | Download full attendance history with one click |
| 🔒 **Privacy First** | Stores only face embeddings, never raw images after registration |
| 🖥️ **CPU + GPU** | Runs at 10fps on CPU; NVIDIA/Apple Silicon supported |
| ⚙️ **Zero Config** | Auto-creates DB, tables, and index — just run and go |

---

## 📸 How It Works

### Step 1 — Employee Registration
The system captures **8 face photos** from your webcam, generates 512-dimensional ArcFace embeddings, averages them for robustness, and stores only the embedding (never the photo).

### Step 2 — FAISS Index
All embeddings are L2-normalized and loaded into a FAISS `IndexFlatIP` (cosine similarity). Search time is <1ms even for thousands of employees.

### Step 3 — Real-Time Recognition
Every webcam frame goes through:
1. **RetinaFace** detection — finds and aligns all faces in the frame
2. **ArcFace** embedding — generates 512-dim feature vector per face
3. **FAISS search** — finds the nearest stored embedding
4. **Threshold check** — cosine similarity > 0.6 = match
5. **DB write** — marks attendance once per person per day

### Step 4 — Dashboard
Live annotated video feed with colour-coded results:
- 🟢 **Green** — attendance marked now
- 🟠 **Orange** — already marked today
- 🔴 **Red** — unknown face

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Webcam
- macOS / Linux / Windows

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/biometric-attendance.git
cd biometric-attendance

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Setup (run once)

```bash
# 4. Edit employee list in register_employee.py
#    Change the EMPLOYEES list at the bottom of the file
nano register_employee.py

# 5. Register employees (webcam required)
python3 register_employee.py

# 6. Build FAISS search index
python3 faiss_index.py
```

### Daily Use

```bash
# Option A — Web dashboard (recommended)
python3 dashboard.py
# Open http://127.0.0.1:7860

# Option B — OpenCV window (terminal only)
python3 attendance_system.py
```

---

## 🗂️ Project Structure

```
biometric/
│
├── 📄 dashboard.py              # Gradio web dashboard (main UI)
├── 📄 attendance_system.py      # OpenCV live window (headless option)
├── 📄 register_employee.py      # Employee registration via webcam
├── 📄 faiss_index.py            # Build / rebuild FAISS search index
├── 📄 config.py                 # Central config — reads from .env
├── 📄 .env                      # Settings: threshold, port, GPU/CPU
├── 📄 requirements.txt
│
├── 📁 core/
│   └── recognition.py           # InsightFace + FAISS + SQLite logic
│
├── 📁 scripts/
│   ├── init_db.py               # Create database schema
│   ├── view_records.py          # Print today's attendance to terminal
│   └── reset_today.py           # Clear today's records (testing)
│
├── 📁 data/                     # Auto-created · gitignored
│   ├── attendance.db            # SQLite database
│   ├── face_index.faiss         # FAISS vector index
│   ├── id_map.npy               # Employee ID lookup array
│   └── name_map.json            # ID → Name mapping
│
├── 📁 logs/                     # CSV exports land here
│
└── 📁 .vscode/
    ├── launch.json              # F5 run configs for every script
    └── settings.json            # Auto-selects venv interpreter
```

---

## ⚙️ Configuration

All settings live in `.env` — no code changes needed.

```env
# ── Recognition ───────────────────────────────────────────────
THRESHOLD=0.6      # Cosine similarity cutoff (0.5–0.7 recommended)
                   # Raise to 0.65+ to reduce false positives
                   # Lower to 0.55 if lighting is poor

# ── Hardware ──────────────────────────────────────────────────
CTX_ID=-1          # -1 = CPU  |  0 = NVIDIA GPU (CUDA)
DET_SIZE=320       # Detection grid: 320 (fast) or 640 (accurate)

# ── Server ────────────────────────────────────────────────────
HOST=127.0.0.1     # Use 0.0.0.0 to expose on local network
PORT=7860          # Dashboard port

# ── Paths ─────────────────────────────────────────────────────
DB_PATH=data/attendance.db
FAISS_INDEX=data/face_index.faiss
```

---

## 🗄️ Database Schema

```sql
-- Employees: stores only embeddings, never raw images
CREATE TABLE employees (
    emp_id     TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    department TEXT,
    embedding  BLOB NOT NULL        -- 512-dim ArcFace vector (pickled)
);

-- Attendance: one record per employee per day
CREATE TABLE attendance (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id        TEXT,
    date          TEXT,             -- YYYY-MM-DD
    check_in_time TEXT,             -- HH:MM:SS
    status        TEXT DEFAULT 'Present',
    FOREIGN KEY(emp_id) REFERENCES employees(emp_id),
    UNIQUE(emp_id, date)            -- prevents duplicate marking
);
```

---

## ⚡ Performance Optimisations

The system ships with four built-in latency fixes:

| Optimisation | Impact |
|---|---|
| **Skip-frame lock** — drops frames while GPU is busy | Eliminates queue backlog |
| **DB cooldown** — 5s window between SQLite writes | Removes DB bottleneck |
| **Frame resize** — scales to max 640px before inference | ~30% faster inference |
| **DET_SIZE=320** — smaller detection grid | ~60% faster on CPU |

For Apple Silicon (M1/M2/M3), install the optimised runtime:

```bash
pip uninstall onnxruntime -y
pip install onnxruntime-silicon
```

---

## 🔒 Privacy & Compliance

> ⚠️ Face recognition systems may be subject to local privacy laws (e.g. DPDP Act 2023 in India, GDPR in Europe).

This system is designed with privacy in mind:

- ✅ Raw images are **never stored** after registration
- ✅ Only 512-float embeddings are saved — cannot reconstruct a face
- ✅ All data stays **local** — no cloud, no third-party services
- ✅ Employee data can be deleted on request (`DELETE FROM employees WHERE emp_id=?`)
- ⚠️ Add a **consent screen** before registration in production
- ⚠️ Encrypt `attendance.db` with SQLCipher for sensitive deployments

---

## 🛠️ Utility Scripts

```bash
# View today's attendance in terminal
python3 scripts/view_records.py

# Clear today's records (testing only)
python3 scripts/reset_today.py

# Manually add/remove attendance record (admin)
# Edit ACTION, EMP_ID, DATE inside the file first
python3 scripts/manual_override.py
```

---

## 🔄 Adding New Employees

```bash
# 1. Edit the EMPLOYEES list in register_employee.py
#    Add a new dict entry:
#    {"emp_id": "EMP010", "name": "Alice Brown", "dept": "Finance"}

# 2. Re-run registration
python3 register_employee.py

# 3. Rebuild the FAISS index (required after every change)
python3 faiss_index.py
```

> 💡 **Tip:** Register employees in varied lighting conditions and with/without glasses for best accuracy.

---

## 🧩 Tech Stack

| Component | Technology | Why |
|---|---|---|
| Face Detection | RetinaFace (InsightFace) | Best accuracy + speed on CPU |
| Face Recognition | ArcFace `buffalo_l` | SOTA, >99% LFW benchmark |
| Vector Search | FAISS `IndexFlatIP` | Sub-ms search for any team size |
| Database | SQLite | Zero-config, portable, reliable |
| Dashboard | Gradio 5 | Browser UI, no frontend code needed |
| Config | python-dotenv via `.env` | Zero hardcoded values |

---

## 🤝 Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

```bash
# Fork → clone → create branch
git checkout -b feature/your-feature-name

# Make changes, then
git commit -m "feat: description of change"
git push origin feature/your-feature-name
# Open a Pull Request
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ❤️ by **Daloft Aerospace Intern**

⭐ Star this repo if it helped you · 🐛 [Report a bug](../../issues) · 💡 [Request a feature](../../issues)

</div>
