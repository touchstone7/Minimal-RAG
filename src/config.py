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

CHUNKING_METHOD = "sentence"

CHUNK_SIZE = 300
OVERLAP = 50

SENTENCES_PER_CHUNK = 2


# =========================================================
# MODELS
# =========================================================

EMBEDDING_MODEL = "nomic-embed-text"

CHAT_MODEL = "qwen3:8b"

GEMINI_MODEL = "gemini-3.5-flash"


# =========================================================
# LLM PROVIDER
# =========================================================

LLM_PROVIDER = "gemini"

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)


# =========================================================
# VECTOR DB
# =========================================================

COLLECTION_NAME = "documents"

# ---------------------------------------------------------
# Chroma
#
# Keep this for now because we are intentionally leaving
# the existing Chroma setup untouched during migration.
# ---------------------------------------------------------

CHROMA_DB_PATH = "chroma_db"


# ---------------------------------------------------------
# Qdrant
# ---------------------------------------------------------

QDRANT_URL = os.getenv(
    "QDRANT_URL",
    ""
)

QDRANT_API_KEY = os.getenv(
    "QDRANT_API_KEY",
    ""
)

QDRANT_COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION_NAME",
    "documents"
)

QDRANT_VECTOR_SIZE = 768


# =========================================================
# RETRIEVAL
# =========================================================

TOP_K = 3

# =========================================================
# VECTOR DATABASE PROVIDER
# =========================================================

VECTOR_DB = os.getenv(
    "VECTOR_DB",
    "chroma"
)