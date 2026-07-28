# Data
DATA_DIRECTORY = "data"

# Chunking
CHUNKING_METHOD = "sentence"      # "character" or "sentence"

CHUNK_SIZE = 300
OVERLAP = 50

SENTENCES_PER_CHUNK = 2

# Models
EMBEDDING_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen3:8b"

# Vector DB
COLLECTION_NAME = "documents"

# Retrieval
TOP_K = 3