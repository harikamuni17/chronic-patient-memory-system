"""
app/schemas/chat.py
───────────────────
Pydantic schemas for chat sessions and messages.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


# ── Chat Session schemas ───────────────────────────────────────────────────────

class ChatSessionCreate(BaseModel):
    """Body to create a new chat session for a patient."""
    patient_id: int
    title: str = Field(default="New Conversation", max_length=255)


class ChatSessionResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    title: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Chat Message schemas ───────────────────────────────────────────────────────

class ChatMessageCreate(BaseModel):
    """Body sent by the frontend when the doctor asks a question."""
    question: str = Field(..., min_length=1, max_length=2000)


class ChatMessageResponse(BaseModel):
    id: int
    session_id: int
    role: str   # "user" | "assistant"
    content: str
    sources: Optional[str] = None   # JSON string of source chunks
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatResponse(BaseModel):
    """Returned by the /chat endpoint — the question + AI answer pair."""
    question_message: ChatMessageResponse
    answer_message: ChatMessageResponse
    session_id: int
