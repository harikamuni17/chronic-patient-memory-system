"""
app/db/base.py
──────────────
Declares the SQLAlchemy DeclarativeBase that every ORM model must inherit.

Import ALL models here (at the bottom) so that Alembic's autogenerate
can discover them when creating migration scripts.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared base for every ORM model in the project."""
    pass


# ── Import all models so Alembic can see them ──────────────────────────────────
# Do NOT remove these imports even though they look unused.
from app.models.user import User          # noqa: F401, E402
from app.models.patient import Patient    # noqa: F401, E402
from app.models.report import Report      # noqa: F401, E402
from app.models.chat import ChatSession, ChatMessage  # noqa: F401, E402
