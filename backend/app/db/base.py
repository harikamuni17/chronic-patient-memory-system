"""
app/db/base.py
──────────────
This module serves as a central point to ensure all SQLAlchemy models are
registered with the metadata before database initialization or migration.

Import ALL models here (at the bottom) so that Alembic's autogenerate
can discover them when creating migration scripts.
"""

# ── Import all models so Alembic can see them ──────────────────────────────────
# Do NOT remove these imports even though they look unused.
from app.db.base_class import Base        # noqa: F401
from app.models.user import User          # noqa: F401, E402
from app.models.patient import Patient    # noqa: F401, E402
from app.models.report import Report      # noqa: F401, E402
from app.models.chat import ChatSession, ChatMessage  # noqa: F401, E402
