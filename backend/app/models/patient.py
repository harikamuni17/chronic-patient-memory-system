"""
app/models/patient.py
─────────────────────
SQLAlchemy ORM model representing a patient record.

Relationship summary
────────────────────
Patient >── User      (belongs to one doctor)
Patient ──< Report    (has many uploaded reports)
Patient ──< ChatSession (has many AI chat sessions)
"""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"

    # ── Primary key ────────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Foreign key to the managing doctor ────────────────────────────────────
    doctor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Demographics ───────────────────────────────────────────────────────────
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)  # Male / Female / Other
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    contact_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Medical summary ────────────────────────────────────────────────────────
    blood_group: Mapped[str | None] = mapped_column(String(10), nullable=True)
    allergies: Mapped[str | None] = mapped_column(Text, nullable=True)  # comma-separated
    chronic_conditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    current_medications: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

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
    doctor: Mapped["User"] = relationship("User", back_populates="patients")  # noqa: F821
    reports: Mapped[list["Report"]] = relationship(  # noqa: F821
        "Report", back_populates="patient", cascade="all, delete-orphan"
    )
    chat_sessions: Mapped[list["ChatSession"]] = relationship(  # noqa: F821
        "ChatSession", back_populates="patient", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Patient id={self.id} name={self.name!r}>"
