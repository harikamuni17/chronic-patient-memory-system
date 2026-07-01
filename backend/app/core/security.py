"""
app/core/security.py
────────────────────
All cryptographic helpers live here:
  • Password hashing with bcrypt (via passlib)
  • JWT creation and verification (via python-jose)

Nothing in this module imports from the database layer — it is pure
cryptography so it can be tested in isolation.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ── Password hashing ───────────────────────────────────────────────────────────
# CryptContext manages multiple schemes; bcrypt is the active one.
# Deprecated entries are auto-rehashed on next login — safe for migrations.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Return a bcrypt hash of *plain_password*."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if *plain_password* matches *hashed_password*."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT helpers ────────────────────────────────────────────────────────────────

def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.

    Parameters
    ----------
    subject:
        Typically the user's ID (stored in the ``sub`` claim).
    expires_delta:
        Custom TTL; falls back to ``ACCESS_TOKEN_EXPIRE_MINUTES`` from config.

    Returns
    -------
    str
        The encoded JWT string.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """
    Decode and validate a JWT token.

    Returns the payload dict on success, or ``None`` if the token is
    expired / malformed / has a bad signature.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None
