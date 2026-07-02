"""
app/rag/embeddings.py
─────────────────────
Lazy-loading wrapper for Sentence Transformers (all-MiniLM-L6-v2).
The model is loaded once per process and reused for all embed calls.
"""

import logging

logger = logging.getLogger(__name__)

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

_model = None


def get_embedding_model():
    """Lazily load and cache the SentenceTransformer model."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        logger.info("Loading embedding model: %s", EMBEDDING_MODEL_NAME)
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of text chunks."""
    if not texts:
        return []

    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    """Generate a single embedding vector for a search query."""
    vectors = embed_texts([query])
    return vectors[0]
