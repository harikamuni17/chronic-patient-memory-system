"""
app/api/v1/endpoints/patients.py
──────────────────────────────────
Patient CRUD routes — all require authentication.

GET    /patients/           — paginated list (+ search)
POST   /patients/           — create
GET    /patients/stats       — dashboard statistics
GET    /patients/{id}        — single patient
PUT    /patients/{id}        — full update
PATCH  /patients/{id}        — partial update
DELETE /patients/{id}        — delete (cascades reports + embeddings)
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse, PatientListResponse
from app.services import patient_service

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/stats", summary="Dashboard statistics for current doctor")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    return patient_service.get_patient_stats(db, doctor_id=current_user.id)


@router.get(
    "/",
    response_model=PatientListResponse,
    summary="List patients (paginated + searchable)",
)
def list_patients(
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    search: str | None = Query(None, description="Search by patient name"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PatientListResponse:
    total, patients = patient_service.get_patients(
        db,
        doctor_id=current_user.id,
        skip=skip,
        limit=limit,
        search=search,
    )
    return PatientListResponse(total=total, patients=patients)


@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new patient",
)
def create_patient(
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PatientResponse:
    patient = patient_service.create_patient(db, data, doctor_id=current_user.id)
    return patient


@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
    summary="Get a single patient by ID",
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PatientResponse:
    patient = patient_service.get_patient_by_id(db, patient_id, doctor_id=current_user.id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    return patient


@router.patch(
    "/{patient_id}",
    response_model=PatientResponse,
    summary="Partially update a patient (PATCH)",
)
def update_patient(
    patient_id: int,
    data: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PatientResponse:
    patient = patient_service.update_patient(db, patient_id, data, doctor_id=current_user.id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    return patient


@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a patient and all their data",
)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    deleted = patient_service.delete_patient(db, patient_id, doctor_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
