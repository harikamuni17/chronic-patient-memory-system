"""
app/models/report.py
────────────────────
SQLAlchemy ORM model for uploaded medical PDF reports.

Each Report belongs to a Patient and stores:
  • The original filename and its server-side path
  • The extracted plain text (used for embedding)
  • Whether the report has been embedded into ChromaDB
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    # ── Primary key ────────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Foreign key ────────────────────────────────────────────────────────────
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── File metadata ──────────────────────────────────────────────────────────
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)  # bytes
    mime_type: Mapped[str] = mapped_column(
        String(100), default="application/pdf", nullable=False
    )

    # ── Extracted content ──────────────────────────────────────────────────────
    # Full text extracted from the PDF; None if extraction failed.
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Embedding status ───────────────────────────────────────────────────────
    # Set to True after the text has been chunked and stored in ChromaDB.
    is_embedded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Optional metadata ──────────────────────────────────────────────────────
    report_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    report_type: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # e.g. "Blood Test", "MRI", "Prescription"
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

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
    patient: Mapped["Patient"] = relationship("Patient", back_populates="reports")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Report id={self.id} patient_id={self.patient_id} file={self.original_filename!r}>"
