"""
app/services/chat_service.py
──────────────────────────────
Business logic for creating chat sessions and processing questions
through the RAG pipeline.
"""

import json
import logging
from sqlalchemy.orm import Session

from app.models.chat import ChatSession, ChatMessage
from app.models.patient import Patient
from app.rag.rag_pipeline import answer_question

logger = logging.getLogger(__name__)


def _get_owned_patient(db: Session, patient_id: int, doctor_id: int) -> Patient:
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id, Patient.doctor_id == doctor_id)
        .first()
    )
    if not patient:
        raise ValueError(f"Patient {patient_id} not found.")
    return patient


# ── Session management ─────────────────────────────────────────────────────────

def create_session(
    db: Session, patient_id: int, doctor_id: int, title: str = "New Conversation"
) -> ChatSession:
    """Create (and persist) a new chat session."""
    _get_owned_patient(db, patient_id, doctor_id)

    session = ChatSession(
        doctor_id=doctor_id,
        patient_id=patient_id,
        title=title,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    logger.info("Chat session %d created for patient %d", session.id, patient_id)
    return session


def get_sessions_for_patient(
    db: Session, patient_id: int, doctor_id: int
) -> list[ChatSession]:
    """List all chat sessions for a patient, newest first."""
    _get_owned_patient(db, patient_id, doctor_id)
    return (
        db.query(ChatSession)
        .filter(
            ChatSession.patient_id == patient_id,
            ChatSession.doctor_id == doctor_id,
        )
        .order_by(ChatSession.created_at.desc())
        .all()
    )


def get_session_messages(
    db: Session, session_id: int, doctor_id: int
) -> list[ChatMessage]:
    """Return all messages in a session, chronological order."""
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.doctor_id == doctor_id)
        .first()
    )
    if not session:
        raise ValueError(f"Session {session_id} not found.")
    return session.messages


# ── Question answering ─────────────────────────────────────────────────────────

def ask_question(
    db: Session,
    session_id: int,
    question: str,
    doctor_id: int,
) -> tuple[ChatMessage, ChatMessage]:
    """
    Process a doctor's question through the RAG pipeline and persist both
    the question and the AI answer as ChatMessage records.

    Parameters
    ----------
    session_id : int
        The active chat session.
    question : str
        The doctor's question text.
    doctor_id : int
        Used to verify session ownership.

    Returns
    -------
    tuple[ChatMessage, ChatMessage]
        (user_message, assistant_message)
    """
    # Load session + verify ownership
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.doctor_id == doctor_id)
        .first()
    )
    if not session:
        raise ValueError(f"Chat session {session_id} not found.")

    patient = session.patient

    # Store the doctor's question
    user_msg = ChatMessage(
        session_id=session_id,
        role="user",
        content=question,
    )
    db.add(user_msg)
    db.flush()  # get ID without full commit

    # Run RAG pipeline
    answer_text, source_chunks = answer_question(
        patient_id=patient.id,
        patient_name=patient.name,
        question=question,
    )

    # Serialize sources for storage (first 3 chunks for brevity)
    sources_json = json.dumps(source_chunks[:3]) if source_chunks else None

    # Store the AI's answer
    ai_msg = ChatMessage(
        session_id=session_id,
        role="assistant",
        content=answer_text,
        sources=sources_json,
    )
    db.add(ai_msg)

    # Update session title from first question (if still default)
    if session.title == "New Conversation" and question:
        session.title = question[:80]  # truncate long questions

    db.commit()
    db.refresh(user_msg)
    db.refresh(ai_msg)

    logger.info(
        "Session %d: question answered (%d source chunks)", session_id, len(source_chunks)
    )
    return user_msg, ai_msg
