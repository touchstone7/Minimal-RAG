# Minimal RAG

A lightweight Retrieval-Augmented Generation (RAG) application built in
Python.

The project demonstrates a complete local RAG pipeline:

**Documents → Loaders → Chunking → Embeddings → ChromaDB → Retrieval →
Prompt → Ollama LLM**

It now exposes the pipeline through a **FastAPI backend** and provides a
simple **Streamlit web UI**.

------------------------------------------------------------------------

## Features

-   Load supported documents from the project data directory
-   Multiple document loaders through a loader factory
-   Multiple chunking strategies through a chunker factory
-   Generate embeddings locally using Ollama
-   Store embeddings in persistent ChromaDB
-   Retrieve relevant chunks for a user question
-   Generate grounded answers using a local Ollama LLM
-   FastAPI REST API
-   Automatic FastAPI Swagger documentation
-   Streamlit web UI
-   Configurable RAG pipeline
-   Clean separation between API, service, retrieval, ingestion, and UI
    layers

------------------------------------------------------------------------

## Architecture

``` text
                         User
                           │
                           ▼
                    ┌─────────────┐
                    │  Streamlit  │
                    │     UI      │
                    └──────┬──────┘
                           │ HTTP
                           ▼
                    ┌─────────────┐
                    │   FastAPI   │
                    │     API     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  RagService │
                    └──────┬──────┘
                           │
          ┌────────────────┼─────────────────┐
          ▼                ▼                 ▼
     Document          Chunking          Embeddings
      Loaders             │                 │
          │               │                 ▼
          │               │             Ollama
          │               │          nomic-embed-text
          │               │                 │
          └───────────────┴─────────────────┤
                                            ▼
                                      ┌───────────┐
                                      │ ChromaDB  │
                                      └─────┬─────┘
                                            │
                                         Retrieve
                                            │
                                            ▼
                                      Prompt Builder
                                            │
                                            ▼
                                         Ollama
                                          Qwen
                                            │
                                            ▼
                                         Answer
```

------------------------------------------------------------------------

## Project Structure

``` text
Minimal-RAG/
│
├── src/
│   ├── api/
│   │   ├── app.py
│   │   └── schemas.py
│   │
│   ├── chunkers/
│   │   ├── character_chunker.py
│   │   ├── sentence_chunker.py
│   │   └── chunker_factory.py
│   │
│   ├── embeddings/
│   │   └── embeddings_service.py
│   │
│   ├── llm/
│   │   └── ollama_service.py
│   │
│   ├── loaders/
│   │   ├── loader_factory.py
│   │   └── ...
│   │
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── prompt_builder.py
│   │
│   ├── services/
│   │   └── rag_service.py
│   │
│   ├── vectordb/
│   │   └── chroma_service.py
│   │
│   ├── config.py
│   ├── main.py
│   └── models.py
│
├── ui/
│   └── app.py
│
├── data/
│   └── *.txt / supported documents
│
├── chroma_db/
│   └── persistent ChromaDB data
│
├── .venv/
├── .gitignore
├── README.md
└── requirements.txt
```

------------------------------------------------------------------------

## RAG Pipeline

### 1. Document Loading

Documents are loaded from the configured data directory.

The loader factory selects the appropriate loader based on the document
type.

### 2. Chunking

Documents are split into smaller chunks before embedding.

Current chunking strategies include:

-   Character-based chunking
-   Sentence-based chunking

The chunker factory allows the strategy to be selected through
configuration.

### 3. Embeddings

Each chunk is converted into a numerical vector using the local Ollama
embedding model:

``` text
nomic-embed-text
```

### 4. Vector Database

Embeddings and their associated text/metadata are stored in a persistent
ChromaDB collection.

The database is stored locally under:

``` text
chroma_db/
```

### 5. Retrieval

When a user asks a question:

1.  The question is embedded.
2.  ChromaDB searches for semantically similar chunks.
3.  The most relevant chunks are returned.

### 6. Prompt Construction

The retrieved chunks are combined with the user's question to construct
the context-aware prompt.

### 7. LLM Generation

The prompt is sent to the locally running Ollama LLM.

The generated answer is returned to the API and displayed in the UI.

------------------------------------------------------------------------

# Local Setup

## Prerequisites

You need:

-   Python 3.10+
-   Git
-   Ollama
-   A local Ollama embedding model
-   A local Ollama generation model

The project is designed to run locally and does not require a paid LLM
API.

------------------------------------------------------------------------

## 1. Clone the Repository

``` bash
git clone https://github.com/touchstone7/Minimal-RAG
cd Minimal-RAG
```

------------------------------------------------------------------------

## 2. Create a Virtual Environment

Windows PowerShell:

``` powershell
python -m venv .venv
```

Activate it:

``` powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation because of its execution policy, you can
use the appropriate PowerShell execution-policy adjustment for your
environment or activate the environment from another supported shell.

------------------------------------------------------------------------

## 3. Install Python Dependencies

``` powershell
pip install -r requirements.txt
```

Current direct dependencies include:

``` text
chromadb
ollama
pypdf
numpy
streamlit
requests
fastapi
uvicorn
```

------------------------------------------------------------------------

# Ollama Setup

Ollama runs the local embedding model and LLM.

Make sure Ollama is installed and running.

Check:

``` powershell
ollama --version
```

Check currently available models:

``` powershell
ollama list
```

The project currently uses:

``` text
nomic-embed-text
```

for embeddings.

A generation model such as:

``` text
qwen3:8b
```

can be used for answering questions.

If the required models are not installed, pull them with Ollama.

For example:

``` powershell
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

Check models currently loaded into memory:

``` powershell
ollama ps
```

When no models are actively loaded, this command should show an empty
process list.

------------------------------------------------------------------------

# Running the Project

The project now has two execution modes.

## CLI Mode

From the project root:

``` powershell
python -m src.main
```

This runs the RAG pipeline directly from the command line.

------------------------------------------------------------------------

## API Mode

Start FastAPI with Uvicorn:

``` powershell
uvicorn src.api.app:app --reload
```

The API will be available at:

``` text
http://127.0.0.1:8000
```

### Swagger UI

FastAPI automatically provides interactive API documentation at:

``` text
http://127.0.0.1:8000/docs
```

You can use this page to test the endpoints without needing Postman or
another API client.

------------------------------------------------------------------------

## Streamlit UI

Keep the FastAPI server running in one terminal.

Open another terminal from the project root and activate the same
virtual environment.

Then run:

``` powershell
streamlit run ui/app.py
```

The Streamlit application will normally be available at:

``` text
http://localhost:8501
```

The UI communicates with the FastAPI backend.

------------------------------------------------------------------------

# API Endpoints

## Health Check

``` http
GET /health
```

Example response:

``` json
{
  "status": "running"
}
```

------------------------------------------------------------------------

## Ingest Documents

``` http
POST /ingest
```

This triggers document ingestion and indexing using the documents
configured for the project.

Example response:

``` json
{
  "status": "success",
  "chunks_created": 52
}
```

------------------------------------------------------------------------

## Ask a Question

``` http
POST /query
```

Request:

``` json
{
  "question": "What is a database?"
}
```

Example response:

``` json
{
  "question": "What is a database?",
  "answer": "A database is a system that stores and organizes data efficiently..."
}
```

------------------------------------------------------------------------

# Typical Development Workflow

Start the backend:

``` powershell
uvicorn src.api.app:app --reload
```

Then, in another terminal:

``` powershell
streamlit run ui/app.py
```

Open:

``` text
http://localhost:8501
```

Alternatively, use the API directly through:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# Important: Ollama vs Python Dependencies

The Python package:

``` text
ollama
```

is only the Python client used by this project.

The actual Ollama application runs separately on the machine and hosts
the models.

Conceptually:

``` text
Python environment
│
├── ollama
├── fastapi
├── uvicorn
├── chromadb
└── streamlit

Operating system
│
└── Ollama
    ├── nomic-embed-text
    └── qwen3:8b
```

------------------------------------------------------------------------

# Persistent Vector Database

ChromaDB is configured as a persistent local vector database.

Vector data is stored on disk rather than existing only for the lifetime
of the Python process.

The local database directory is:

``` text
chroma_db/
```

This allows the indexed data to survive application restarts.

The size of the database depends primarily on:

-   Number of documents
-   Number of chunks
-   Embedding dimensionality
-   Metadata
-   ChromaDB storage overhead

------------------------------------------------------------------------

# Development Notes

The project deliberately separates responsibilities into different
layers.

``` text
API
 ↓
RagService
 ↓
Loaders / Chunkers / Embeddings / VectorDB / Retrieval / LLM
```

`RagService` acts as the main orchestration layer.

This keeps `main.py` and the FastAPI endpoints thin and prevents the
complete RAG pipeline from being duplicated in multiple entry points.

------------------------------------------------------------------------

# Current Status

### Completed

-   [x] Document loading
-   [x] Multiple document loaders
-   [x] Character chunking
-   [x] Sentence chunking
-   [x] Chunker factory
-   [x] Embedding generation
-   [x] Ollama integration
-   [x] Persistent ChromaDB
-   [x] Vector indexing
-   [x] Semantic retrieval
-   [x] Prompt construction
-   [x] Local LLM generation
-   [x] RAG service layer
-   [x] FastAPI backend
-   [x] Health endpoint
-   [x] Ingestion endpoint
-   [x] Query endpoint
-   [x] Swagger API documentation
-   [x] Streamlit UI
-   [x] End-to-end local UI testing

### Next Improvements

-   [ ] Upload documents directly through the UI
-   [ ] Support selecting specific files for a query
-   [ ] Improve ingestion status/progress
-   [ ] Show retrieved source documents
-   [ ] Add conversation/chat history
-   [ ] Improve error handling
-   [ ] Add automated tests
-   [ ] Add logging
-   [ ] Improve UI/UX
-   [ ] Containerize the application
-   [ ] Deploy the UI/API
-   [ ] Evaluate a cloud-hosted vector database
-   [ ] Add authentication if deployed publicly

------------------------------------------------------------------------

# Project Goal

The goal of **Minimal RAG** is to understand and build a RAG system from
the ground up rather than hiding the core pipeline behind a high-level
framework.

The project is intentionally modular so that each major component can be
understood, replaced, and improved independently.

Ultimately, the project is intended to evolve from a simple local RAG
implementation into a small production-style application with:

``` text
Document Upload
       ↓
Document Processing
       ↓
Chunking
       ↓
Embeddings
       ↓
Vector Database
       ↓
Semantic Retrieval
       ↓
LLM
       ↓
Web UI
```

------------------------------------------------------------------------

## License

Add the project's chosen license here.
