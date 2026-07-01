"""
app/db/init_db.py
─────────────────
One-time database initialisation helper.

Called at application startup (in main.py) to:
  1. Create all tables defined on Base that don't exist yet.
  2. Seed a default admin doctor account if the users table is empty.

In production with Alembic, table creation is handled by migrations.
For the hackathon / SQLite workflow this script is sufficient.
"""

import logging

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.base import Base          # noqa: F401 — triggers model imports
from app.db.session import engine
from app.models.user import User

logger = logging.getLogger(__name__)

# ── Default seed credentials ───────────────────────────────────────────────────
# Change these immediately in production!
DEFAULT_DOCTOR_EMAIL = "admin@hospital.com"
DEFAULT_DOCTOR_PASSWORD = "Admin@12345"
DEFAULT_DOCTOR_NAME = "Dr. Admin"


def create_tables() -> None:
    """Create all ORM-mapped tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified / created.")


def seed_default_doctor(db: Session) -> None:
    """
    Insert a seed doctor account so the application is usable immediately
    after first launch.  Does nothing if the users table is not empty.
    """
    existing = db.query(User).first()
    if existing:
        return  # already seeded

    doctor = User(
        name=DEFAULT_DOCTOR_NAME,
        email=DEFAULT_DOCTOR_EMAIL,
        hashed_password=hash_password(DEFAULT_DOCTOR_PASSWORD),
        is_active=True,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    logger.info(
        "Seed doctor created → email: %s  password: %s",
        DEFAULT_DOCTOR_EMAIL,
        DEFAULT_DOCTOR_PASSWORD,
    )


def init_db(db: Session) -> None:
    """Entry-point called from main.py on startup."""
    create_tables()
    seed_default_doctor(db)
