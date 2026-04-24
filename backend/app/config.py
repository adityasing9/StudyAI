import os
from dotenv import load_dotenv

load_dotenv()

# --- Database Configuration ---
# Use SQLite by default for zero-config setup. Set USE_MYSQL=true in .env to use MySQL.
USE_MYSQL = os.getenv("USE_MYSQL", "false").lower() == "true"

if USE_MYSQL:
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "studyai")
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
else:
    _db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "studyai.db")
    DATABASE_URL = f"sqlite:///{_db_path}"

# --- OpenRouter Configuration ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "openrouter/free"

# --- ChromaDB Configuration ---
# --- Storage Configuration ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "chroma_data")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

if not USE_MYSQL:
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'studyai.db')}"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)

# --- Chunking Configuration ---
CHUNK_SIZE = 400  # words
CHUNK_OVERLAP = 50  # words
