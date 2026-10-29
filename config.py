"""
Central configuration for the RAG pipeline.
Everything here is overridable via environment variables (see .env).
"""

import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- 1. Document loading -----------------------------------------------
# Candidate locations for the local Aventro PDF corpus
_candidates = [
    os.path.abspath(os.path.join(BASE_DIR, "..", "pdf", "pdf")),
    os.path.abspath(os.path.join(BASE_DIR, "..", "..", "pdf", "pdf")),
    os.path.abspath(os.path.join(BASE_DIR, "..", "pdf")),
    os.path.abspath(os.path.join(BASE_DIR, "..", "..", "pdf")),
]
DEFAULT_CORPUS_DIR = next((p for p in _candidates if os.path.isdir(p)), _candidates[0])

CORPUS_DIR = os.getenv("CORPUS_DIR", DEFAULT_CORPUS_DIR)
# Fall back to DEFAULT_CORPUS_DIR if configured path does not exist on disk
if not os.path.exists(CORPUS_DIR) and os.path.exists(DEFAULT_CORPUS_DIR):
    CORPUS_DIR = DEFAULT_CORPUS_DIR

# Keep this small on purpose -- this is a learning project, not a bulk ingest job.
MAX_PDF_FILES = int(os.getenv("MAX_PDF_FILES", "5"))

# --- 2. Chunking ---------------------------------------------------------
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))

# --- 3. Embeddings (local Ollama) ----------------------------------------
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "768"))

# --- 4. Local LLM used only for the final "ask a question" demo ---------
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
TOP_K = int(os.getenv("TOP_K", "4"))

# --- 5. Postgres + pgvector ------------------------------------------------
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "aventro_rag_db")
TABLE_NAME = os.getenv("TABLE_NAME", "document_chunks")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
)
