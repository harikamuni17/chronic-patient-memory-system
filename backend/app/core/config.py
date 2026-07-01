"""
app/core/config.py
──────────────────
Centralised application settings loaded from environment variables.
Uses Pydantic-Settings so every value is validated at startup.
Swap DATABASE_URL to a PostgreSQL URL without touching any other code.
"""

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, field_validator


class Settings(BaseSettings):
    # ── Application ────────────────────────────────────────────────────────────
    APP_NAME: str = "Chronic Patient Memory System"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # ── Security ───────────────────────────────────────────────────────────────
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── Database ───────────────────────────────────────────────────────────────
    # SQLite default; swap to postgresql://... for production
    DATABASE_URL: str = "sqlite:///./chronic_patients.db"

    # ── Gemini AI ──────────────────────────────────────────────────────────────
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # ── File Uploads ───────────────────────────────────────────────────────────
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 20

    # ── ChromaDB ───────────────────────────────────────────────────────────────
    CHROMA_DB_PATH: str = "chroma_db"

    # ── CORS ───────────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def allowed_origins_list(self) -> list[str]:
        """Split the comma-separated ALLOWED_ORIGINS string into a list."""
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    @property
    def upload_path(self) -> Path:
        """Resolved absolute path to the uploads directory."""
        p = Path(self.UPLOAD_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def max_upload_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    The cache means .env is only parsed once per process lifetime,
    keeping startup fast.
    """
    return Settings()


# Convenient module-level alias used across the codebase
settings = get_settings()
