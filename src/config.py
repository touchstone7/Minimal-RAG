import os

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# =========================================================
# DATA
# =========================================================

DATA_DIRECTORY = "data"


# =========================================================
# CHUNKING
# =========================================================

CHUNKING_METHOD = "sentence"      # "character" or "sentence"

CHUNK_SIZE = 300
OVERLAP = 50

SENTENCES_PER_CHUNK = 2


# =========================================================
# MODELS
# =========================================================

EMBEDDING_MODEL = "nomic-embed-text"

# Local Ollama model
CHAT_MODEL = "qwen3:8b"

# Gemini model
GEMINI_MODEL = "gemini-3.5-flash"


# =========================================================
# LLM PROVIDER
# =========================================================

# Supported:
#   "ollama"
#   "gemini"

LLM_PROVIDER = "ollama"


# Gemini API key.
#
# The actual key is stored in .env and must never
# be committed to source control.

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)


# =========================================================
# VECTOR DB
# =========================================================

COLLECTION_NAME = "documents"

CHROMA_DB_PATH = "chroma_db"


# =========================================================
# RETRIEVAL
# =========================================================

TOP_K = 3