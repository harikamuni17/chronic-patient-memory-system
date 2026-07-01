"""
app/schemas/patient.py
──────────────────────
Pydantic schemas for Patient CRUD operations.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class PatientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120, examples=["John Doe"])
    age: int = Field(..., ge=0, le=150, examples=[45])
    gender: str = Field(..., examples=["Male"])
    date_of_birth: Optional[date] = None
    contact_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    # Medical summary
    blood_group: Optional[str] = Field(None, max_length=10, examples=["O+"])
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    current_medications: Optional[str] = None
    notes: Optional[str] = None


class PatientCreate(PatientBase):
    """All required fields must be present on creation."""
    pass


class PatientUpdate(BaseModel):
    """Every field is optional for partial updates (PATCH)."""
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    current_medications: Optional[str] = None
    notes: Optional[str] = None


class PatientResponse(PatientBase):
    """Full patient record returned by the API."""
    id: int
    doctor_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PatientListResponse(BaseModel):
    """Paginated list wrapper."""
    total: int
    patients: list[PatientResponse]
