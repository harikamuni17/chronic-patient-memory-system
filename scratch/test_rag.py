"""
scratch/test_rag.py
───────────────────
Unit test script verifying Cognee memory integration and RAG query flow.
"""

import sys
import asyncio
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.append(str(backend_path))

import logging
logging.basicConfig(level=logging.INFO)

from app.rag.rag_pipeline import index_report_async, answer_question_async

async def test_cognee_rag():
    print("=== STARTING COGNEE RAG UNIT TEST ===")
    
    # 1. Simulating PDF Extracted Text
    sample_pdf_text = (
        "Patient John Doe. Age: 45. blood group: O+.\n"
        "Allergies: Penicillin, Sulfa drugs.\n"
        "Current Medications: Metformin 500mg once daily for Type 2 Diabetes, "
        "Lisinopril 10mg once daily for Hypertension.\n"
        "Family History: Mother had Type 2 Diabetes, Father had Hypertension."
    )
    
    patient_id = 9999
    
    # 2. Ingesting text into Cognee
    print("\n[Step 1] Ingesting text into Cognee patient dataset...")
    success = await index_report_async(patient_id, sample_pdf_text)
    if not success:
        print("Cognee indexing failed. Make sure packages and LLM_API_KEY are configured.")
        return

    # 3. Querying index
    print("\n[Step 2] Querying Cognee for medications...")
    query = "What medications does John Doe take?"
    answer, retrieved = await answer_question_async(patient_id, "John Doe", query)
    print(f"Retrieved context matches ({len(retrieved)} items)")
    print(f"Gemini Answer:\n{answer}")
        
    # 4. Testing out-of-context query
    print("\n[Step 3] Testing out-of-context fallback...")
    bad_query = "What is the patient's favorite movie?"
    fallback_answer, _ = await answer_question_async(patient_id, "John Doe", bad_query)
    print(f"Fallback Answer:\n{fallback_answer}")
        
    print("\n=== COGNEE RAG UNIT TEST COMPLETE ===")

if __name__ == "__main__":
    asyncio.run(test_cognee_rag())
