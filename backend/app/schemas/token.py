"""
app/schemas/token.py
────────────────────
Pydantic schemas for JWT token request/response payloads.
"""

from pydantic import BaseModel


class Token(BaseModel):
    """Returned by POST /auth/login on success."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Claims decoded from a JWT (the ``sub`` field holds the user ID)."""
    sub: str | None = None
