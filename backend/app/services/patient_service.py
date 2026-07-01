"""
app/services/patient_service.py
─────────────────────────────────
CRUD business logic for Patient records.

All data access is scoped to the authenticated doctor_id so one doctor
can never see or modify another doctor's patients.
"""

import logging
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from app.rag.vector_store import delete_patient_collection

logger = logging.getLogger(__name__)


def get_patients(
    db: Session,
    doctor_id: int,
    skip: int = 0,
    limit: int = 50,
    search: str | None = None,
) -> tuple[int, list[Patient]]:
    """
    Return a paginated list of patients belonging to *doctor_id*.

    Parameters
    ----------
    search : str | None
        Optional name filter (case-insensitive partial match).

    Returns
    -------
    tuple[int, list[Patient]]
        (total_count, page_of_patients)
    """
    query = db.query(Patient).filter(Patient.doctor_id == doctor_id)

    if search:
        query = query.filter(Patient.name.ilike(f"%{search}%"))

    total = query.count()
    patients = query.order_by(Patient.name).offset(skip).limit(limit).all()
    return total, patients


def get_patient_by_id(db: Session, patient_id: int, doctor_id: int) -> Patient | None:
    """Return a single patient or None if not found / not owned by doctor."""
    return (
        db.query(Patient)
        .filter(Patient.id == patient_id, Patient.doctor_id == doctor_id)
        .first()
    )


def create_patient(db: Session, data: PatientCreate, doctor_id: int) -> Patient:
    """Persist a new patient record and return it."""
    patient = Patient(**data.model_dump(), doctor_id=doctor_id)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    logger.info("Patient created: id=%d name=%s", patient.id, patient.name)
    return patient


def update_patient(
    db: Session, patient_id: int, data: PatientUpdate, doctor_id: int
) -> Patient | None:
    """
    Partially update a patient record (PATCH semantics).

    Returns the updated patient or None if not found.
    """
    patient = get_patient_by_id(db, patient_id, doctor_id)
    if not patient:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    logger.info("Patient updated: id=%d", patient.id)
    return patient


def delete_patient(db: Session, patient_id: int, doctor_id: int) -> bool:
    """
    Delete a patient and all their associated data.

    Returns True if deleted, False if not found.
    """
    patient = get_patient_by_id(db, patient_id, doctor_id)
    if not patient:
        return False

    # Remove their ChromaDB collection (embeddings) before DB deletion
    delete_patient_collection(patient_id)

    db.delete(patient)
    db.commit()
    logger.info("Patient deleted: id=%d", patient_id)
    return True


def get_patient_stats(db: Session, doctor_id: int) -> dict:
    """Return summary statistics for the dashboard."""
    from app.models.report import Report
    from app.models.chat import ChatSession
    from sqlalchemy import func

    total_patients = (
        db.query(func.count(Patient.id))
        .filter(Patient.doctor_id == doctor_id)
        .scalar()
        or 0
    )
    total_reports = (
        db.query(func.count(Report.id))
        .join(Patient, Report.patient_id == Patient.id)
        .filter(Patient.doctor_id == doctor_id)
        .scalar()
        or 0
    )
    total_sessions = (
        db.query(func.count(ChatSession.id))
        .filter(ChatSession.doctor_id == doctor_id)
        .scalar()
        or 0
    )
    return {
        "total_patients": total_patients,
        "total_reports": total_reports,
        "total_chat_sessions": total_sessions,
    }
