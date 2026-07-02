"""
scratch/test_rag.py
───────────────────
Unit test script verifying ChromaDB indexing and RAG query flow.
"""

import sys
import os
import shutil
from pathlib import Path

backend_path = Path(__file__).parent.parent / "backend"
sys.path.append(str(backend_path))

os.environ.setdefault("SECRET_KEY", "test_secret_key_for_rag_unit_tests")
os.environ.setdefault("GEMINI_API_KEY", "test-key")
os.environ.setdefault("CHROMA_DB_PATH", "test_chroma_db")

import logging
logging.basicConfig(level=logging.INFO)

from app.rag.rag_pipeline import index_report, answer_question
from app.rag.vector_store import delete_patient_collection


def test_chromadb_rag():
    print("=== STARTING CHROMADB RAG UNIT TEST ===")

    patient_id = 9999
    report_id = 1

    # Clean up any prior test collection
    delete_patient_collection(patient_id)
    if Path("test_chroma_db").exists():
        shutil.rmtree("test_chroma_db", ignore_errors=True)

    sample_pdf_text = (
        "Patient John Doe. Age: 45. blood group: O+.\n"
        "Allergies: Penicillin, Sulfa drugs.\n"
        "Current Medications: Metformin 500mg once daily for Type 2 Diabetes, "
        "Lisinopril 10mg once daily for Hypertension.\n"
        "Family History: Mother had Type 2 Diabetes, Father had Hypertension."
    )

    print("\n[Step 1] Indexing text into ChromaDB patient collection...")
    chunk_count = index_report(patient_id, report_id, sample_pdf_text)
    assert chunk_count > 0, f"Expected chunks to be indexed, got {chunk_count}"
    print(f"Indexed {chunk_count} chunk(s) successfully.")

    print("\n[Step 2] Querying for medications (retrieval only — no Gemini call)...")
    from app.rag.embeddings import embed_query
    from app.rag.vector_store import query_documents

    query = "What medications does John Doe take?"
    docs, distances = query_documents(patient_id, embed_query(query), n_results=3)
    assert docs, "Expected retrieved documents from ChromaDB"
    print(f"Retrieved {len(docs)} chunk(s), best distance: {distances[0]:.4f}")
    print(f"Top chunk preview: {docs[0][:120]}...")

    print("\n[Step 3] Testing out-of-context fallback (Gemini may be skipped)...")
    bad_query = "What is the patient's favorite movie?"
    fallback_answer, sources = answer_question(patient_id, "John Doe", bad_query)
    print(f"Answer: {fallback_answer}")
    print(f"Sources returned: {len(sources)}")

    delete_patient_collection(patient_id)
    shutil.rmtree("test_chroma_db", ignore_errors=True)

    print("\n=== CHROMADB RAG UNIT TEST COMPLETE ===")


if __name__ == "__main__":
    test_chromadb_rag()
