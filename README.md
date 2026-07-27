# Minimal RAG

A minimal Retrieval-Augmented Generation (RAG) system built completely from scratch using Python, Ollama, and ChromaDB.

The purpose of this project is educational: understanding every component of a RAG pipeline without relying on high-level frameworks such as LangChain or LlamaIndex.

---

## Features

- Load text documents
- Chunk documents
- Generate embeddings using Ollama
- Store embeddings in ChromaDB
- Retrieve relevant chunks using vector similarity search
- Generate answers using Qwen

---

## Tech Stack

- Python 3.14+
- Ollama
- ChromaDB
- Qwen 3 8B
- nomic-embed-text

---

## Project Structure

```
Minimal-RAG/
│
├── data/
│   └── operating_systems.txt
│
├── src/
│   ├── main.py
│   ├── documents.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vectordb.py
│   ├── retriever.py
│   ├── prompt_builder.py
│   └── llm.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Prerequisites

Install the following before running the project.

### 1. Python

Install Python 3.14 or newer.

Verify installation

```powershell
python --version
pip --version
```

---

### 2. Ollama

Download and install Ollama.

Verify

```powershell
ollama --version
```

---

### 3. Download the required models

Embedding model

```powershell
ollama pull nomic-embed-text
```

LLM

```powershell
ollama pull qwen3:8b
```

Verify

```powershell
ollama list
```

Expected output

```
nomic-embed-text
qwen3:8b
```

---

## Clone the Repository

```powershell
git clone https://github.com/touchstone7/Minimal-RAG.git
```

```powershell
cd Minimal-RAG
```

---

## Create a Virtual Environment

Windows PowerShell

```powershell
python -m venv .venv
```

Activate

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks execution

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## Running the Project

From the project root

```powershell
python src/main.py
```

Example

```
Collection contains 4 chunk(s)

Ask a question:
What does an operating system do?

Answer

An operating system manages hardware resources,
schedules CPU time,
manages memory,
and provides an interface between hardware and applications.
```

---

## How It Works

```
                 INDEXING

Documents
    │
    ▼
Load Documents
    │
    ▼
Chunk Documents
    │
    ▼
Generate Embeddings
    │
    ▼
Store in ChromaDB

-------------------------------

                 QUERY

User Question
    │
    ▼
Generate Question Embedding
    │
    ▼
Similarity Search
    │
    ▼
Retrieve Top Chunks
    │
    ▼
Build Prompt
    │
    ▼
Qwen
    │
    ▼
Answer
```

---

## Current Limitations

- Uses in-memory ChromaDB
- Single text document
- Character-based chunking
- No streaming responses
- No conversation memory
- No PDF support

---

## Future Improvements

- Persistent ChromaDB
- Recursive chunking
- PDF ingestion
- Multi-document support
- Hybrid search
- Metadata filtering
- Streaming responses
- FastAPI REST API
- Docker support
- React frontend

---

## License

MIT License