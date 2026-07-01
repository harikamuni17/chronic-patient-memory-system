"""
app/rag/rag_pipeline.py
───────────────────────
Orchestrates the Retrieval-Augmented Generation (RAG) pipeline using Cognee.
Cognee implements a hybrid Graph + Vector memory platform for AI agents.

This module dynamically maps application settings (like settings.GEMINI_API_KEY)
to the environment variables Cognee requires, ensuring seamless config injection.
"""

import os
import asyncio
import logging
from app.core.config import settings
from app.rag.gemini_client import generate_answer

logger = logging.getLogger(__name__)

# ── Dynamic Environment Configuration for Cognee ──────────────────────────────
# We inject these values programmatically from the application settings to
# save the user from duplicating configurations in their .env file.
os.environ["LLM_PROVIDER"] = "gemini"
os.environ["LLM_MODEL"] = f"gemini/{settings.GEMINI_MODEL}"
os.environ["LLM_API_KEY"] = settings.GEMINI_API_KEY

# Set default embedding matching the Gemini API suite
os.environ["EMBEDDING_PROVIDER"] = "gemini"
os.environ["EMBEDDING_MODEL"] = "models/text-embedding-004"

# Set persistent database path for Cognee's vector store (LanceDB)
os.environ["COFFEE_DB_PATH"] = os.path.join(settings.CHROMA_DB_PATH, "cognee")

try:
    import cognee
except ImportError:
    logger.warning("Cognee package not installed yet. Run pip install -r requirements.txt")


async def index_report_async(patient_id: int, extracted_text: str) -> bool:
    """
    Asynchronously index text into Cognee memory under a patient-scoped dataset.
    Cognee chunks, embeds, and extracts entity relationships automatically.
    """
    try:
        # Cognee partitions memory spaces into datasets, keeping records separate
        dataset_name = f"patient_{patient_id}"
        await cognee.remember(
            extracted_text,
            dataset_name=dataset_name
        )
        logger.info("Cognee: Indexed report text under dataset '%s'", dataset_name)
        return True
    except Exception as e:
        logger.error("Cognee indexing failed for patient %d: %s", patient_id, e)
        return False


def index_report(
    patient_id: int,
    report_id: int,
    extracted_text: str,
    chunk_size: int = 800,  # Ignored (Cognee uses its own chunker)
    overlap: int = 100,
) -> int:
    """
    Synchronous entry point called by endpoints/services.
    Runs the asynchronous indexing task in the system loop.
    """
    success = asyncio.run(index_report_async(patient_id, extracted_text))
    # Return 1 if success, 0 if failure to match signature expects chunk count
    return 1 if success else 0


async def answer_question_async(
    patient_id: int,
    patient_name: str,
    question: str,
    n_results: int = 5,
) -> tuple[str, list[str]]:
    """
    Asynchronously query Cognee's memory space and feed the graph context into Gemini.
    """
    try:
        dataset_name = f"patient_{patient_id}"
        # Retrieve context from the patient's dataset
        results = await cognee.recall(
            query_text=question,
            datasets=[dataset_name]
        )
        
        # Cognee returns structured matches; we extract text elements
        context_chunks = [res.text for res in results if hasattr(res, 'text')]
        if not context_chunks:
            # Try to grab string values directly if structure differs
            context_chunks = [str(res) for res in results]

        if not context_chunks:
            logger.info("Cognee returned empty context for patient %d", patient_id)
            return "I couldn't find that information in the patient's medical history.", []

        # Ground the Gemini assistant using the retrieved context
        answer = generate_answer(
            patient_name=patient_name,
            context_chunks=context_chunks,
            question=question
        )
        return answer, context_chunks

    except Exception as e:
        logger.error("Cognee query failed for patient %d: %s", patient_id, e)
        return "I couldn't find that information in the patient's medical history.", []


def answer_question(
    patient_id: int,
    patient_name: str,
    question: str,
    n_results: int = 5,
) -> tuple[str, list[str]]:
    """
    Synchronous entry point called by endpoints/services.
    Runs the asynchronous retrieval task in the system loop.
    """
    return asyncio.run(answer_question_async(patient_id, patient_name, question))
