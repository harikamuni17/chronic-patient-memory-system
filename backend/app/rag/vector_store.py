"""
app/rag/vector_store.py
───────────────────────
ChromaDB interface with one isolated collection per patient.

Multi-tenancy rule: collection name = "patient_{patient_id}" so embeddings
from one patient can never appear in another patient's queries.
"""

import logging
from functools import lru_cache

import chromadb
from chromadb.config import Settings

from app.core.config import settings

logger = logging.getLogger(__name__)

COLLECTION_PREFIX = "patient_"
COSINE_SPACE = "cosine"


@lru_cache(maxsize=1)
def get_chroma_client() -> chromadb.PersistentClient:
    """Return a process-wide persistent ChromaDB client."""
    return chromadb.PersistentClient(
        path=settings.CHROMA_DB_PATH,
        settings=Settings(anonymized_telemetry=False),
    )


def _collection_name(patient_id: int) -> str:
    return f"{COLLECTION_PREFIX}{patient_id}"


def get_patient_collection(patient_id: int):
    """Get or create the vector collection scoped to a single patient."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=_collection_name(patient_id),
        metadata={"patient_id": patient_id, "hnsw:space": COSINE_SPACE},
    )


def add_documents(
    patient_id: int,
    report_id: int,
    chunks: list[str],
    embeddings: list[list[float]],
) -> int:
    """
    Upsert text chunks for a report into the patient's collection.

    Returns the number of chunks stored.
    """
    if not chunks:
        return 0

    collection = get_patient_collection(patient_id)
    ids = [f"report_{report_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {"patient_id": patient_id, "report_id": report_id, "chunk_index": i}
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    logger.info(
        "ChromaDB: upserted %d chunks for report %d (patient %d)",
        len(chunks),
        report_id,
        patient_id,
    )
    return len(chunks)


def query_documents(
    patient_id: int,
    query_embedding: list[float],
    n_results: int = 5,
) -> tuple[list[str], list[float]]:
    """
    Query the patient's collection for the most relevant chunks.

    Returns (document_texts, distances).
    """
    collection = get_patient_collection(patient_id)
    if collection.count() == 0:
        return [], []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
        include=["documents", "distances"],
    )

    documents = results.get("documents", [[]])[0] or []
    distances = results.get("distances", [[]])[0] or []
    return documents, distances


def delete_report_documents(patient_id: int, report_id: int) -> None:
    """Remove all vector chunks belonging to a single report."""
    try:
        collection = get_patient_collection(patient_id)
        collection.delete(where={"report_id": report_id})
        logger.info(
            "ChromaDB: deleted chunks for report %d (patient %d)",
            report_id,
            patient_id,
        )
    except Exception as exc:
        logger.error(
            "ChromaDB: failed to delete report %d for patient %d: %s",
            report_id,
            patient_id,
            exc,
        )


def delete_patient_collection(patient_id: int) -> None:
    """Drop the entire collection when a patient is deleted."""
    try:
        client = get_chroma_client()
        client.delete_collection(_collection_name(patient_id))
        logger.info("ChromaDB: deleted collection for patient %d", patient_id)
    except Exception as exc:
        # Collection may not exist if patient had no indexed reports
        logger.warning(
            "ChromaDB: could not delete collection for patient %d: %s",
            patient_id,
            exc,
        )
