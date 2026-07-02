"""
app/rag/rag_pipeline.py
───────────────────────
Orchestrates the Retrieval-Augmented Generation (RAG) pipeline:

  PDF text → chunk → Sentence Transformers embed → ChromaDB (per patient)
  Question → embed → ChromaDB retrieve → Gemini 1.5 Flash (context-confined)
"""

import logging

from app.rag.embeddings import embed_query, embed_texts
from app.rag.gemini_client import generate_answer
from app.rag.vector_store import add_documents, query_documents

logger = logging.getLogger(__name__)

FALLBACK_ANSWER = "I couldn't find that information in the patient's medical history."

# Cosine distance above this threshold is treated as irrelevant context.
MAX_COSINE_DISTANCE = 0.85


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """Split extracted PDF text into overlapping chunks for embedding."""
    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return chunks


def index_report(
    patient_id: int,
    report_id: int,
    extracted_text: str,
    chunk_size: int = 800,
    overlap: int = 100,
) -> int:
    """
    Chunk, embed, and store report text in the patient's ChromaDB collection.

    Returns the number of chunks indexed (0 on failure or empty text).
    """
    try:
        chunks = chunk_text(extracted_text, chunk_size=chunk_size, overlap=overlap)
        if not chunks:
            logger.warning("No chunks produced for report %d (patient %d)", report_id, patient_id)
            return 0

        embeddings = embed_texts(chunks)
        return add_documents(patient_id, report_id, chunks, embeddings)
    except Exception as exc:
        logger.error(
            "Indexing failed for report %d (patient %d): %s",
            report_id,
            patient_id,
            exc,
        )
        return 0


def answer_question(
    patient_id: int,
    patient_name: str,
    question: str,
    n_results: int = 5,
) -> tuple[str, list[str]]:
    """
    Retrieve relevant chunks from ChromaDB and generate a grounded Gemini answer.

    Returns (answer_text, source_chunks).
    """
    try:
        query_embedding = embed_query(question)
        documents, distances = query_documents(
            patient_id=patient_id,
            query_embedding=query_embedding,
            n_results=n_results,
        )

        context_chunks = [
            doc for doc, dist in zip(documents, distances)
            if doc and dist <= MAX_COSINE_DISTANCE
        ]

        if not context_chunks:
            logger.info("No relevant context for patient %d query", patient_id)
            return FALLBACK_ANSWER, []

        answer = generate_answer(
            patient_name=patient_name,
            context_chunks=context_chunks,
            question=question,
        )
        return answer, context_chunks

    except Exception as exc:
        logger.error("RAG query failed for patient %d: %s", patient_id, exc)
        return FALLBACK_ANSWER, []
