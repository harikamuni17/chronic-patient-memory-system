"""
app/services/auth_service.py
─────────────────────────────
Business logic for authentication: login validation and registration.

Services never import from ``app.api`` — they only use models, schemas,
security helpers, and the DB session.  This keeps the logic testable
without spinning up a full HTTP server.
"""

import logging
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Validate credentials and return the User if correct.

    Returns None (not an exception) so the caller decides the HTTP status.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning("Login attempt with unknown email: %s", email)
        return None
    if not verify_password(password, user.hashed_password):
        logger.warning("Wrong password for email: %s", email)
        return None
    if not user.is_active:
        logger.warning("Disabled account login attempt: %s", email)
        return None
    return user


def login_user(db: Session, email: str, password: str) -> str:
    """
    Authenticate and return a JWT access token.

    Raises
    ------
    ValueError
        If credentials are incorrect or the account is inactive.
    """
    user = authenticate_user(db, email, password)
    if not user:
        raise ValueError("Incorrect email or password.")
    token = create_access_token(subject=str(user.id))
    logger.info("User %d (%s) logged in.", user.id, user.email)
    return token


def register_doctor(db: Session, data: UserCreate) -> User:
    """
    Create a new doctor account.

    Raises
    ------
    ValueError
        If the email is already registered.
    """
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ValueError(f"Email '{data.email}' is already registered.")

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("New doctor registered: id=%d email=%s", user.id, user.email)
    return user
