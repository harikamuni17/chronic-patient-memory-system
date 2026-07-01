"""
app/schemas/user.py
───────────────────
Pydantic schemas for User (Doctor) create / read / update operations.

Pattern used throughout:
  UserBase      — shared fields
  UserCreate    — fields required on registration (includes plain password)
  UserUpdate    — all optional, for PATCH
  UserResponse  — what the API returns (NO password)
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120, examples=["Dr. Jane Smith"])
    email: EmailStr = Field(..., examples=["jane.smith@hospital.com"])


class UserCreate(UserBase):
    """Used for doctor registration."""
    password: str = Field(..., min_length=8, examples=["Str0ng#Pass"])


class UserUpdate(BaseModel):
    """All fields optional — used for PATCH /users/me."""
    name: str | None = Field(None, min_length=2, max_length=120)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8)


class UserResponse(UserBase):
    """Returned by every API endpoint — password is excluded."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
