"""
app/utils/file_handler.py
─────────────────────────
Helpers for safe file upload storage.

Files are stored as:
    uploads/<patient_id>/<uuid4>_<sanitised_original_name>

Using a UUID prefix prevents filename collisions and path-traversal attacks.
"""

import logging
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {"application/pdf"}
ALLOWED_EXTENSIONS = {".pdf"}


def _sanitise_filename(name: str) -> str:
    """Remove path components and dangerous characters from a filename."""
    # Take only the last segment (no directory traversal)
    safe = Path(name).name
    # Replace whitespace and special chars with underscores
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in safe)
    return safe or "upload"


async def save_upload_file(
    upload_file: UploadFile,
    patient_id: int,
) -> tuple[str, str, int]:
    """
    Validate and persist an uploaded file to disk.

    Parameters
    ----------
    upload_file : UploadFile
        The incoming FastAPI file object.
    patient_id : int
        Used to organise files into per-patient sub-directories.

    Returns
    -------
    tuple[str, str, int]
        (server_filename, absolute_file_path, file_size_bytes)

    Raises
    ------
    HTTPException 400 — invalid file type or file too large.
    """
    # ── Validate MIME type ─────────────────────────────────────────────────────
    if upload_file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only PDF files are allowed. Got: {upload_file.content_type}",
        )

    # ── Validate extension ─────────────────────────────────────────────────────
    original_name = upload_file.filename or "upload.pdf"
    suffix = Path(original_name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must have a .pdf extension.",
        )

    # ── Read content & check size ──────────────────────────────────────────────
    content = await upload_file.read()
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB} MB.",
        )

    # ── Build target path ──────────────────────────────────────────────────────
    patient_dir = settings.upload_path / str(patient_id)
    patient_dir.mkdir(parents=True, exist_ok=True)

    safe_name = _sanitise_filename(original_name)
    server_filename = f"{uuid.uuid4().hex}_{safe_name}"
    file_path = patient_dir / server_filename

    # ── Write to disk ──────────────────────────────────────────────────────────
    file_path.write_bytes(content)
    logger.info("Saved upload → %s (%d bytes)", file_path, len(content))

    return server_filename, str(file_path), len(content)


def delete_file(file_path: str) -> None:
    """Remove a file from disk if it exists (silent on missing)."""
    p = Path(file_path)
    if p.exists():
        p.unlink()
        logger.info("Deleted file: %s", p)
