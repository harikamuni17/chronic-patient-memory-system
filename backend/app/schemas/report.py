"""
app/schemas/report.py
─────────────────────
Pydantic schemas for PDF report upload and retrieval.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ReportResponse(BaseModel):
    """Full report record returned by the API after upload or retrieval."""
    id: int
    patient_id: int
    filename: str
    original_filename: str
    file_size: Optional[int]
    mime_type: str
    report_type: Optional[str]
    description: Optional[str]
    report_date: Optional[datetime]
    is_embedded: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReportUpdate(BaseModel):
    """Fields that can be updated after upload (metadata only)."""
    report_type: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    report_date: Optional[datetime] = None
