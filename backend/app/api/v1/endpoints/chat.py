"""
app/api/v1/endpoints/chat.py
──────────────────────────────
AI Chat routes powered by the RAG pipeline.

POST   /patients/{patient_id}/sessions/           — create chat session
GET    /patients/{patient_id}/sessions/           — list sessions
GET    /sessions/{session_id}/messages/           — get full message history
POST   /sessions/{session_id}/ask                 — ask a question (RAG answer)
DELETE /sessions/{session_id}                     — delete a session
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.schemas.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatResponse,
)
from app.services import chat_service

router = APIRouter(tags=["Chat"])


@router.post(
    "/patients/{patient_id}/sessions/",
    response_model=ChatSessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start a new chat session for a patient",
)
def create_session(
    patient_id: int,
    data: ChatSessionCreate | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ChatSessionResponse:
    title = (data.title if data else None) or "New Conversation"
    try:
        session = chat_service.create_session(
            db, patient_id=patient_id, doctor_id=current_user.id, title=title
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return session


@router.get(
    "/patients/{patient_id}/sessions/",
    response_model=list[ChatSessionResponse],
    summary="List all chat sessions for a patient",
)
def list_sessions(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[ChatSessionResponse]:
    try:
        return chat_service.get_sessions_for_patient(
            db, patient_id=patient_id, doctor_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/sessions/{session_id}/messages/",
    response_model=list[ChatMessageResponse],
    summary="Get the full message history of a session",
)
def get_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[ChatMessageResponse]:
    try:
        return chat_service.get_session_messages(
            db, session_id=session_id, doctor_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/sessions/{session_id}/ask",
    response_model=ChatResponse,
    summary="Ask the AI a question about the patient's records",
    description=(
        "Runs the RAG pipeline:\n"
        "1. Embeds the question\n"
        "2. Retrieves relevant document chunks from ChromaDB\n"
        "3. Sends context + question to Gemini\n"
        "4. Persists and returns the answer"
    ),
)
def ask_question(
    session_id: int,
    body: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ChatResponse:
    try:
        user_msg, ai_msg = chat_service.ask_question(
            db,
            session_id=session_id,
            question=body.question,
            doctor_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service error: {str(e)}",
        )
    return ChatResponse(
        question_message=user_msg,
        answer_message=ai_msg,
        session_id=session_id,
    )
