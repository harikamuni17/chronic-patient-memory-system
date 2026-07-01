"""
app/api/v1/endpoints/auth.py
─────────────────────────────
Authentication routes:
  POST /auth/login     — OAuth2 password flow (returns JWT)
  POST /auth/register  — Create a new doctor account
  GET  /auth/me        — Return the current authenticated doctor
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import login_user, register_doctor

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=Token,
    summary="Doctor login",
    description="Submit email/password via the standard OAuth2 form and receive a JWT bearer token.",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """
    Accepts OAuth2 password form (username = email).
    Returns a bearer JWT on success.
    """
    try:
        token = login_user(db, email=form_data.username, password=form_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=token)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new doctor",
)
def register(data: UserCreate, db: Session = Depends(get_db)) -> User:
    """Create a new doctor account. Email must be unique."""
    try:
        user = register_doctor(db, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    return user


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current doctor profile",
)
def get_me(current_user: User = Depends(get_current_active_user)) -> User:
    """Return the profile of the currently authenticated doctor."""
    return current_user
