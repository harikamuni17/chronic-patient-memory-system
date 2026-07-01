"""
app/db/session.py
─────────────────
Creates the SQLAlchemy engine and session factory.

Design notes
────────────
• SQLite connect_args: {"check_same_thread": False} is required because
  FastAPI runs in a thread-pool; without it SQLite raises a threading error.
• When migrating to PostgreSQL just change DATABASE_URL in .env — everything
  else stays the same.
• SessionLocal is used ONLY inside get_db() (see core/dependencies.py).
  Never create a Session directly in business logic.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# ── Engine ─────────────────────────────────────────────────────────────────────
_connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
    # pool_pre_ping checks the connection is alive before handing it out —
    # prevents "server has gone away" errors after idle periods.
    pool_pre_ping=True,
)

# Enable WAL mode for SQLite — much better concurrent read performance
if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, _connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# ── Session factory ────────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,  # explicit transaction control
    autoflush=False,   # flush only on commit — avoids surprise DB hits
)
