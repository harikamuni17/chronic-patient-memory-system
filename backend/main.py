"""
main.py
────────
FastAPI application factory and startup configuration.

Run locally:
    uvicorn main:app --reload --port 8000

Environment:
    Copy backend/.env.example → backend/.env and fill in your values.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import SessionLocal

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan (startup / shutdown) ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code inside the ``with`` block runs at startup.
    Code after ``yield`` runs at shutdown.
    """
    logger.info("Starting %s...", settings.APP_NAME)
    db = SessionLocal()
    try:
        init_db(db)          # Create tables + seed admin doctor
    finally:
        db.close()
    logger.info("Database initialised. Server ready.")
    yield
    logger.info("Shutting down %s.", settings.APP_NAME)


# ── Application factory ────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-powered medical history retrieval system using RAG.\n\n"
        "Upload patient PDFs → ask questions → get Gemini-powered answers "
        "grounded strictly in the patient's records."
    ),
    version="1.0.0",
    docs_url="/docs",          # Swagger UI
    redoc_url="/redoc",        # ReDoc UI
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────────────────────

# CORS — allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ─────────────────────────────────────────────────────────────────────
app.include_router(api_router)


# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"], summary="Health check endpoint")
def health_check() -> dict:
    """Returns 200 OK when the server is running. Used by Render health checks."""
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}


# ── Dev runner ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )
