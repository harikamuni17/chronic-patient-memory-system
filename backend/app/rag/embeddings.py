"""
app/rag/embeddings.py
─────────────────────
Lazy-loading wrapper for Sentence Transformers.
Prevents import errors if sentence-transformers is uninstalled in Cognee mode.
"""

import logging

logger = logging.getLogger(__name__)

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def get_embedding_model():
    """Lazily load the SentenceTransformer model only when invoked."""
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer(EMBEDDING_MODEL_NAME)
    except ImportError:
        logger.warning(
            "sentence-transformers not installed. "
            "Using Cognee under the hood? If so, this module is bypassed."
        )
        return None


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate dummy or real embeddings depending on package presence."""
    model = get_embedding_model()
    if model is None:
        # Fallback to zero-vectors for compatibility checks
        return [[0.0] * 384 for _ in texts]
    
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    """Generate a single embedding query vector."""
    model = get_embedding_model()
    if model is None:
        # Fallback to zero-vector
        return [0.0] * 384
        
    vector = model.encode([query], convert_to_numpy=True)
    return vector[0].tolist()
