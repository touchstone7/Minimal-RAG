# Minimal RAG

A lightweight, fully local Retrieval-Augmented Generation (RAG) application built from the ground up.

**Documents → Loaders → Chunking → Embeddings → ChromaDB → Retrieval → Prompt → Ollama LLM → Answer**

The project currently exposes the pipeline through a **FastAPI backend** and a **React frontend**.

## Features

- Multiple document loaders
- Character-based and sentence-based chunking
- Configurable chunker factory
- Local embeddings through Ollama
- Persistent ChromaDB vector database
- Semantic retrieval
- Context-aware prompt construction
- Local LLM generation through Ollama
- FastAPI REST API + Swagger documentation
- React frontend for document ingestion and querying
- Incremental document ingestion
- Knowledge base persistence across backend restarts
- Clear separation between API, service, retrieval, vector DB, and UI layers

## Architecture

```text
User
  ↓
React Frontend
  ↓ HTTP
FastAPI
  ↓
RagService
  ├── Loaders
  ├── Chunkers
  ├── Embeddings → Ollama / nomic-embed-text
  └── ChromaDB (persistent)
          ↓
      Retrieval
          ↓
    Prompt Builder
          ↓
    Ollama / qwen3:8b
          ↓
        Answer
```

## Project Structure

```text
Minimal-RAG/
├── src/
│   ├── api/
│   │   ├── app.py
│   │   └── schemas.py
│   ├── chunkers/
│   │   ├── character_chunker.py
│   │   ├── sentence_chunker.py
│   │   └── chunker_factory.py
│   ├── embeddings/
│   │   └── embeddings_service.py
│   ├── llm/
│   │   └── ollama_service.py
│   ├── loaders/
│   │   ├── loader_factory.py
│   │   └── ...
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── prompt_builder.py
│   ├── services/
│   │   └── rag_service.py
│   ├── vectordb/
│   │   └── chroma_service.py
│   ├── config.py
│   ├── main.py
│   └── models.py
├── frontend/
│   ├── src/
│   │   ├── api/ragApi.jsx
│   │   ├── components/
│   │   │   ├── Background.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── IngestPanel.jsx
│   │   │   ├── QueryPanel.jsx
│   │   │   └── ResponsePanel.jsx
│   │   ├── App.jsx
│   │   └── styles.css
│   └── ...
├── data/
├── chroma_db/
├── .venv/
├── .gitignore
├── README.md
└── requirements.txt
```

## RAG Pipeline

### 1. Loading

The loader factory selects a loader based on document type.

Supported upload formats:

```text
TXT · Markdown · PDF · DOCX
```

### 2. Chunking

Documents are split into smaller chunks.

Current strategies:

- Character-based chunking
- Sentence-based chunking

### 3. Embeddings

Chunks are converted into vectors using:

```text
nomic-embed-text
```

### 4. Persistent ChromaDB

Embeddings, chunk text, and metadata are stored in:

```text
chroma_db/
```

The database is persistent, so restarting FastAPI does **not** remove the existing knowledge base.

### 5. Retrieval

```text
Question
   ↓
Question embedding
   ↓
ChromaDB similarity search
   ↓
Relevant chunks
```

### 6. Prompt + LLM

Retrieved context is combined with the question and sent to the local generation model:

```text
qwen3:8b
```

## Ingestion vs Query

These are separate operations.

### Ingestion

```text
Upload
  ↓
Save document
  ↓
Load
  ↓
Chunk
  ↓
Embed
  ↓
Add to ChromaDB
```

The React UI calls:

```text
POST /ingest
```

Example response:

```json
{
  "status": "success",
  "filename": "example.pdf",
  "chunks_added": 38,
  "total_chunks": 90
}
```

### Query

Once indexed:

```text
Question
  ↓
Existing ChromaDB
  ↓
Retrieve
  ↓
Prompt
  ↓
Ollama
  ↓
Answer
```

You **do not need to ingest again merely because the application restarted**. `RagService` connects to the existing persistent ChromaDB collection during startup.

```text
Ingest once
    ↓
Stop backend
    ↓
Start backend later
    ↓
Query immediately
```

## Local Setup

### Prerequisites

- Python 3.10+
- Git
- Ollama
- Node.js / npm
- Ollama embedding model
- Ollama generation model

### Clone

```powershell
git clone https://github.com/touchstone7/Minimal-RAG
cd Minimal-RAG
```

### Python environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

## Ollama Setup

Check:

```powershell
ollama --version
ollama list
```

Required models:

```text
nomic-embed-text
qwen3:8b
```

Install if necessary:

```powershell
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

Check active models:

```powershell
ollama ps
```

## Running the Project

The current web application has two processes.

### 1. FastAPI backend

From the project root:

```powershell
uvicorn src.api.app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

### 2. React frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

Open:

```text
http://localhost:5173
```

## API Endpoints

### Health

```http
GET /health
```

```json
{
  "status": "running"
}
```

### Ingest

```http
POST /ingest
```

Accepts a multipart file upload.

Supported:

```text
.txt
.md
.pdf
.docx
```

Example:

```json
{
  "status": "success",
  "filename": "example.pdf",
  "chunks_added": 38,
  "total_chunks": 90
}
```

### Query

```http
POST /query
```

Request:

```json
{
  "question": "What does the document say about caching?"
}
```

Response:

```json
{
  "question": "What does the document say about caching?",
  "answer": "A cache is a hardware or software component that stores data so future requests for that data can be served faster."
}
```

If the persistent knowledge base is empty, the backend rejects the query rather than generating an answer without document context.

## Swagger UI

FastAPI automatically provides:

```text
http://127.0.0.1:8000/docs
```

This can be used to test the backend independently of React.

## React Frontend

The frontend handles:

```text
Backend health status
Document upload
Ingestion result
Query input
RAG response
```

Embedding, retrieval, and LLM inference remain in the Python backend.

The current UI uses a minimal dark interface with a dedicated knowledge-base section, query interface, generated-response section, backend status, and local-inference branding.

## Persistence

Documents are saved in the configured data directory.

Processed chunks and embeddings are stored in:

```text
chroma_db/
```

Therefore:

```text
Ingest document
       ↓
Restart application
       ↓
Query existing knowledge base
```

No re-embedding is required merely because FastAPI restarted.

## Development Workflow

Typical session:

**Terminal 1:** Ensure Ollama is running.

**Terminal 2:**

```powershell
uvicorn src.api.app:app --reload
```

**Terminal 3:**

```powershell
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

First-time knowledge-base setup:

1. Start backend and frontend.
2. Upload a document.
3. Wait for ingestion metadata.
4. Ask questions.
5. Restart the backend if desired.
6. Ask another question without ingesting again.

## Development Notes

`RagService` is the main orchestration layer:

```text
FastAPI
   ↓
RagService
   ↓
Loaders / Chunkers / Embeddings / ChromaDB
   ↓
Retriever
   ↓
Prompt Builder
   ↓
Ollama
```

This keeps API endpoints thin and avoids duplicating the RAG pipeline.

## Current Status

### Completed

- [x] Document loading
- [x] Multiple document loaders
- [x] Character chunking
- [x] Sentence chunking
- [x] Chunker factory
- [x] Embedding generation
- [x] Ollama integration
- [x] Persistent ChromaDB
- [x] Vector indexing
- [x] Semantic retrieval
- [x] Prompt construction
- [x] Local LLM generation
- [x] RAG service layer
- [x] FastAPI backend
- [x] Health endpoint
- [x] Incremental document ingestion
- [x] Query endpoint
- [x] Swagger API documentation
- [x] React frontend
- [x] React document upload
- [x] Ingestion metadata display
- [x] Query interface
- [x] RAG response display
- [x] Backend health status
- [x] Knowledge-base persistence across backend restarts
- [x] End-to-end local testing

### Next Improvements

- [ ] Prevent duplicate chunk IDs when repeatedly ingesting documents with the same index range
- [ ] Cleanly replace/re-index an existing document
- [ ] Show retrieved source documents
- [ ] Show retrieval scores/relevance
- [ ] Add conversation history
- [ ] Improve ingestion progress reporting
- [ ] Add document deletion/management
- [ ] Add document-specific querying
- [ ] Add automated tests
- [ ] Add structured logging
- [ ] Improve error handling
- [ ] Containerize the application
- [ ] Deploy frontend/backend
- [ ] Evaluate alternative vector databases
- [ ] Add authentication for public deployment

## Project Goal

The goal of **Minimal RAG** is to understand and build RAG from the ground up rather than hiding the core pipeline behind a high-level framework.

The project is intentionally modular so each component can be understood, replaced, tested, and improved independently.

Long-term direction:

```text
Document Upload
       ↓
Document Processing
       ↓
Chunking
       ↓
Embeddings
       ↓
Persistent ChromaDB
       ↓
Semantic Retrieval
       ↓
Prompt Construction
       ↓
Local LLM
       ↓
React Web Interface
```

## License

Add the project's chosen license here.
