# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with Angular, FastAPI, Pinecone, and Ollama. Ask questions about company policies and get accurate answers grounded in source documents.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Angular](https://img.shields.io/badge/Angular-17-red)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)

## Features

- **Semantic Search** — Finds relevant document chunks using vector embeddings
- **Conversational Memory** — Maintains context across multiple exchanges
- **Scoped Responses** — Only answers questions about ingested documents
- **Local LLM** — Runs entirely on your machine with Ollama

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Angular 17 |
| Backend | FastAPI (Python) |
| Vector DB | Pinecone |
| Embeddings | Llama Text Embed v2 |
| LLM | Llama 3.2 via Ollama |

## Architecture
```
┌─────────────┐      HTTP       ┌─────────────┐
│   Angular   │ ◄─────────────► │   FastAPI   │
│   Frontend  │   /api/ask      │   Backend   │
└─────────────┘                 └──────┬──────┘
                                       │
                        ┌──────────────┼──────────────┐
                        ▼              ▼              ▼
                   ┌─────────┐   ┌─────────┐   ┌─────────┐
                   │Pinecone │   │ Ollama  │   │  Docs   │
                   │(vectors)│   │  (LLM)  │   │ (data/) │
                   └─────────┘   └─────────┘   └─────────┘
```

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [Ollama](https://ollama.com/)
- [Pinecone Account](https://www.pinecone.io/) (free tier works)

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com//GarrettMcQuigg/rag.git
cd rag
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```
PINECONE_API_KEY=your-api-key
PINECONE_INDEX_NAME=your-index-name
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Ollama Setup
```bash
ollama pull llama3.2
```

### 5. Ingest Documents

With the backend virtual environment activated:
```bash
cd backend
python main.py ingest
```

## Running the App

You'll need three terminals:

**Terminal 1 — Ollama** (if not running as a service):
```bash
ollama serve
```

**Terminal 2 — Backend:**
```bash
cd backend
.\venv\Scripts\Activate.ps1  # or source venv/bin/activate
uvicorn api:app --reload
```

**Terminal 3 — Frontend:**
```bash
cd frontend
ng serve
```

Open [http://localhost:4200](http://localhost:4200) in your browser.

## Project Structure
```
rag-project/
├── backend/
│   ├── src/
│   │   ├── config.py        # Environment variables
│   │   ├── vectorstore.py   # Pinecone operations
│   │   ├── ingest.py        # Document chunking
│   │   ├── retriever.py     # Semantic search
│   │   └── generator.py     # LLM integration
│   ├── data/                # Source documents
│   ├── api.py               # FastAPI endpoints
│   ├── main.py              # CLI tools
│   └── requirements.txt
├── frontend/
│   └── src/app/
│       └── chat/            # Chat component
└── README.md
```

## Example Questions

- "How much PTO do I get?"
- "What are the password requirements?"
- "Can I work from home?"
- "What's the dress code?"
- "How do I report a security incident?"

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ask` | Send a question, get an answer |
| GET | `/api/health` | Health check |

## Development

### Linting

**Frontend (Angular/TypeScript):**
```bash
cd frontend
ng lint

# Auto-fix issues
ng lint -- --fix
```

**Backend (Python):**
```bash
cd backend
pip install ruff

# Lint
ruff check .

# Auto-fix
ruff check --fix .

# Format code
ruff format .
```

## License

MIT