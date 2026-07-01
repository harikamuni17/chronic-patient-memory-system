"""
app/rag/gemini_client.py
────────────────────────
Thin wrapper around the Google Generative AI (Gemini) Python SDK.

Responsibilities
────────────────
• Initialise the SDK with the API key from config.
• Build the system prompt that scopes the AI to a single patient's records.
• Call the Gemini API with retry logic (tenacity).
• Return the model's text response.

The model is told to answer ONLY from the provided context so it cannot
hallucinate information about the patient.
"""

import logging
from tenacity import retry, stop_after_attempt, wait_exponential

import google.generativeai as genai

from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialise the SDK once at import time
genai.configure(api_key=settings.GEMINI_API_KEY)

# ── System prompt template ─────────────────────────────────────────────────────
SYSTEM_PROMPT_TEMPLATE = """
You are a medical AI assistant helping a doctor review a patient's medical history.

PATIENT NAME: {patient_name}

IMPORTANT INSTRUCTIONS:
1. Answer ONLY based on the medical records provided in the context below.
2. If the answer is not found in the context, say: "I couldn't find that information in the patient's medical history."
3. Be precise and professional — this is a clinical setting.
4. Do NOT make up diagnoses, medications, or test results.
5. Format structured information (medications, test results) as bullet lists.
6. Always end your answer with: "Source: Patient Medical Records"

PATIENT MEDICAL RECORDS (CONTEXT):
─────────────────────────────────
{context}
─────────────────────────────────
"""


def _build_prompt(patient_name: str, context_chunks: list[str], question: str) -> str:
    """Assemble the full prompt from the template, context, and question."""
    context = "\n\n".join(context_chunks) if context_chunks else "No records found."
    system = SYSTEM_PROMPT_TEMPLATE.format(
        patient_name=patient_name,
        context=context,
    )
    return f"{system}\n\nDOCTOR'S QUESTION: {question}"


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
def generate_answer(
    patient_name: str,
    context_chunks: list[str],
    question: str,
) -> str:
    """
    Call the Gemini API and return the model's text response.

    Parameters
    ----------
    patient_name : str
        Included in the system prompt for personalisation.
    context_chunks : list[str]
        Relevant text passages retrieved from ChromaDB.
    question : str
        The doctor's query.

    Returns
    -------
    str
        The AI-generated answer text.

    Raises
    ------
    Exception
        Re-raised after 3 retries — caller should handle gracefully.
    """
    prompt = _build_prompt(patient_name, context_chunks, question)

    model = genai.GenerativeModel(
        model_name=settings.GEMINI_MODEL,
        generation_config={
            "temperature": 0.2,   # low temperature = factual, less creative
            "max_output_tokens": 1024,
        },
        safety_settings=[
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ],
    )

    response = model.generate_content(prompt)

    if not response.text:
        logger.warning("Gemini returned an empty response.")
        return "I was unable to generate a response. Please try again."

    return response.text.strip()
