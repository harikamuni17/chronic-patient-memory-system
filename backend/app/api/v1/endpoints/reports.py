"""
app/api/v1/endpoints/reports.py
─────────────────────────────────
PDF report upload and management routes.

POST   /patients/{patient_id}/reports/     — upload PDF (multipart/form-data)
GET    /patients/{patient_id}/reports/     — list reports for a patient
DELETE /reports/{report_id}               — delete a single report
"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.schemas.report import ReportResponse
from app.services import report_service

router = APIRouter(tags=["Reports"])


@router.post(
    "/patients/{patient_id}/reports/",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a PDF medical report for a patient",
    description=(
        "Accepts a multipart PDF upload. The server will:\n"
        "1. Validate file type and size\n"
        "2. Extract text from the PDF\n"
        "3. Store embeddings in ChromaDB\n"
        "4. Return the created report record"
    ),
)
async def upload_report(
    patient_id: int,
    file: UploadFile = File(..., description="PDF file to upload"),
    report_type: Optional[str] = Form(None, description="e.g. Blood Test, MRI, Prescription"),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ReportResponse:
    try:
        report = await report_service.upload_report(
            db=db,
            upload_file=file,
            patient_id=patient_id,
            doctor_id=current_user.id,
            report_type=report_type,
            description=description,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return report


@router.get(
    "/patients/{patient_id}/reports/",
    response_model=list[ReportResponse],
    summary="List all reports for a patient",
)
def list_reports(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[ReportResponse]:
    try:
        return report_service.get_reports_for_patient(
            db=db, patient_id=patient_id, doctor_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/reports/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a report and its embeddings",
)
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    deleted = report_service.delete_report(
        db=db, report_id=report_id, doctor_id=current_user.id
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found.")
