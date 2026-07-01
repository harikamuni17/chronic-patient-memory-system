"""
app/services/report_service.py
────────────────────────────────
Business logic for PDF report upload, indexing, listing, and deletion.

Workflow for a new upload
──────────────────────────
1. Save file to disk          (file_handler.py)
2. Extract text from PDF      (pdf_extractor.py)
3. Create Report DB record    (this file)
4. Index text into ChromaDB   (rag_pipeline.py)
5. Mark report as embedded    (this file)
"""

import json
import logging
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.models.report import Report
from app.models.patient import Patient
from app.utils.file_handler import save_upload_file, delete_file
from app.utils.pdf_extractor import extract_text_from_pdf
from app.rag.rag_pipeline import index_report
from app.rag.vector_store import delete_report_documents

logger = logging.getLogger(__name__)


def _assert_patient_owned(
    db: Session, patient_id: int, doctor_id: int
) -> Patient:
    """Raise ValueError if patient doesn't exist or belongs to another doctor."""
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id, Patient.doctor_id == doctor_id)
        .first()
    )
    if not patient:
        raise ValueError(f"Patient {patient_id} not found.")
    return patient


async def upload_report(
    db: Session,
    upload_file: UploadFile,
    patient_id: int,
    doctor_id: int,
    report_type: str | None = None,
    description: str | None = None,
) -> Report:
    """
    Full pipeline: validate ownership → save file → extract → index → record.

    Returns
    -------
    Report
        The persisted Report ORM object.
    """
    # 1. Guard: verify patient belongs to this doctor
    patient = _assert_patient_owned(db, patient_id, doctor_id)

    # 2. Save uploaded file to disk
    server_filename, file_path, file_size = await save_upload_file(
        upload_file, patient_id
    )

    # 3. Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)
    logger.info("Extracted %d chars from %s", len(extracted_text), server_filename)

    # 4. Create DB record (not yet embedded)
    report = Report(
        patient_id=patient_id,
        filename=server_filename,
        original_filename=upload_file.filename or server_filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=upload_file.content_type or "application/pdf",
        extracted_text=extracted_text,
        report_type=report_type,
        description=description,
        is_embedded=False,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    # 5. Index into ChromaDB (if text was extracted)
    if extracted_text.strip():
        chunks_count = index_report(
            patient_id=patient_id,
            report_id=report.id,
            extracted_text=extracted_text,
        )
        if chunks_count > 0:
            report.is_embedded = True
            db.commit()
            db.refresh(report)
    else:
        logger.warning("Report %d has no extractable text — skipping RAG indexing.", report.id)

    logger.info(
        "Report %d uploaded for patient %d (embedded=%s)",
        report.id, patient_id, report.is_embedded,
    )
    return report


def get_reports_for_patient(
    db: Session, patient_id: int, doctor_id: int
) -> list[Report]:
    """Return all reports for a patient, newest first."""
    _assert_patient_owned(db, patient_id, doctor_id)
    return (
        db.query(Report)
        .filter(Report.patient_id == patient_id)
        .order_by(Report.created_at.desc())
        .all()
    )


def delete_report(
    db: Session, report_id: int, doctor_id: int
) -> bool:
    """
    Delete a report: remove embeddings → delete file → delete DB record.

    Returns True on success, False if not found.
    """
    report = (
        db.query(Report)
        .join(Patient, Report.patient_id == Patient.id)
        .filter(Report.id == report_id, Patient.doctor_id == doctor_id)
        .first()
    )
    if not report:
        return False

    # Remove from ChromaDB
    delete_report_documents(report.patient_id, report_id)

    # Remove physical file
    delete_file(report.file_path)

    # Remove DB record
    db.delete(report)
    db.commit()
    logger.info("Report %d deleted.", report_id)
    return True
