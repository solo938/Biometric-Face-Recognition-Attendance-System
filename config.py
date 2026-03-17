import os
from pathlib import Path


ROOT = Path(__file__).parent.resolve()


_env_path = ROOT / '.env'
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())


def _path(key):
    return ROOT / os.environ[key]



DB_PATH      = _path('DB_PATH')
FAISS_INDEX  = _path('FAISS_INDEX')
ID_MAP       = _path('ID_MAP')
NAME_MAP     = _path('NAME_MAP')
LOG_DIR      = _path('LOG_DIR')

# Recognition settings
THRESHOLD    = float(os.environ.get('THRESHOLD', '0.6'))
CTX_ID       = int(os.environ.get('CTX_ID', '-1'))   
DET_SIZE     = int(os.environ.get('DET_SIZE', '640'))

# Server settings
HOST         = os.environ.get('HOST', '0.0.0.0')
PORT         = int(os.environ.get('PORT', '7860'))

# Ensure directories exist on import
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
