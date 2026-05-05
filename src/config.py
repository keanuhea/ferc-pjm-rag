"""Shared config: paths, model names, and LlamaIndex Settings wiring."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "data" / "pdfs"
CHROMA_DIR = ROOT / "chroma_db"
COLLECTION_NAME = "ferc_pjm"

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
TOP_K = 5

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
EMBEDDING_MODEL = "text-embedding-3-small"


def configure_llama_index() -> None:
    """Wire global LlamaIndex Settings. Called once before ingest or query."""
    from llama_index.core import Settings
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.anthropic import Anthropic

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY not set. Copy .env.example to .env and fill it in.")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set. Required for OpenAI embeddings.")

    Settings.llm = Anthropic(model=ANTHROPIC_MODEL)
    Settings.embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL)
    Settings.node_parser = SentenceSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )


def get_chroma_collection():
    """Return a persistent Chroma collection, creating it if needed."""
    import chromadb

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(COLLECTION_NAME)
