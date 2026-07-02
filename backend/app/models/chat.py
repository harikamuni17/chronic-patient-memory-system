"""
app/models/chat.py
──────────────────
SQLAlchemy ORM models for the AI chat system.

ChatSession  — one conversation thread between a doctor and a patient's AI.
ChatMessage  — individual human/AI turns within a session.

Design decision: sessions are scoped to (doctor_id, patient_id) so each
doctor gets their own conversation history per patient.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base_class import Base


class MessageRole(str, enum.Enum):
    """Role of the author of a chat message."""
    USER = "user"       # the doctor's question
    ASSISTANT = "assistant"  # the AI's answer


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    # ── Primary key ────────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Foreign keys ───────────────────────────────────────────────────────────
    doctor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Session metadata ───────────────────────────────────────────────────────
    title: Mapped[str] = mapped_column(
        String(255),
        default="New Conversation",
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Timestamps ─────────────────────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    doctor: Mapped["User"] = relationship("User", back_populates="chat_sessions")  # noqa: F821
    patient: Mapped["Patient"] = relationship("Patient", back_populates="chat_sessions")  # noqa: F821
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at",
    )

    def __repr__(self) -> str:
        return f"<ChatSession id={self.id} patient_id={self.patient_id}>"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    # ── Primary key ────────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Foreign key ────────────────────────────────────────────────────────────
    session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Message content ────────────────────────────────────────────────────────
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )  # "user" | "assistant"
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # ── Optional RAG metadata ──────────────────────────────────────────────────
    # Source chunks used to generate the AI response (JSON string)
    sources: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Timestamps ─────────────────────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    session: Mapped["ChatSession"] = relationship(
        "ChatSession", back_populates="messages"
    )

    def __repr__(self) -> str:
        return f"<ChatMessage id={self.id} role={self.role!r}>"
