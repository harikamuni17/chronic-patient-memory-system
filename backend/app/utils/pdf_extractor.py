"""
app/utils/pdf_extractor.py
──────────────────────────
Production-grade PDF text extraction with:
  • Two-engine fallback: PyPDF2 → pdfminer.six
  • Per-page text tagging for provenance tracking
  • Aggressive text cleaning (ligatures, control chars, excess whitespace)
  • Sentence-aware chunking that never breaks mid-sentence
  • Overlap preserved at sentence boundaries
"""

import logging
import re
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


# ── Dataclass: a labelled page of text ────────────────────────────────────────
@dataclass
class PageText:
    page_number: int
    text: str


# ── Engine 1: PyPDF2 ──────────────────────────────────────────────────────────

def _extract_with_pypdf2(file_path: Path) -> list[PageText]:
    """Extract text page-by-page using PyPDF2."""
    try:
        import PyPDF2
        pages: list[PageText] = []
        with open(file_path, "rb") as fh:
            reader = PyPDF2.PdfReader(fh)
            for i, page in enumerate(reader.pages):
                raw = page.extract_text() or ""
                if raw.strip():
                    pages.append(PageText(page_number=i + 1, text=raw))
        return pages
    except Exception as exc:
        logger.warning("PyPDF2 extraction failed (%s): %s", file_path.name, exc)
        return []


# ── Engine 2: pdfminer.six ────────────────────────────────────────────────────

def _extract_with_pdfminer(file_path: Path) -> list[PageText]:
    """
    Extract text using pdfminer.six page-by-page.
    Handles complex layouts, multi-column PDFs, and scanned overlays.
    """
    try:
        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer

        pages: list[PageText] = []
        for page_num, layout in enumerate(extract_pages(str(file_path)), start=1):
            parts = []
            for element in layout:
                if isinstance(element, LTTextContainer):
                    parts.append(element.get_text())
            text = "".join(parts)
            if text.strip():
                pages.append(PageText(page_number=page_num, text=text))
        return pages
    except Exception as exc:
        logger.warning("pdfminer extraction failed (%s): %s", file_path.name, exc)
        return []


# ── Text cleaning ─────────────────────────────────────────────────────────────

# Common PDF ligatures → ASCII equivalents
_LIGATURE_MAP = str.maketrans({
    "\ufb00": "ff",  "\ufb01": "fi",  "\ufb02": "fl",
    "\ufb03": "ffi", "\ufb04": "ffl", "\ufb06": "st",
    "\u2019": "'",   "\u2018": "'",   "\u201c": '"',
    "\u201d": '"',   "\u2013": "-",   "\u2014": "-",
    "\u00a0": " ",   "\u2022": "•",
})


def _clean_text(text: str) -> str:
    """
    Normalise PDF text:
      1. Translate ligatures & smart quotes to ASCII
      2. Strip non-printable control characters (keep \\n and \\t)
      3. Collapse runs of 3+ newlines → double newline (paragraph break)
      4. Collapse runs of whitespace within a line → single space
    """
    text = text.translate(_LIGATURE_MAP)
    # Remove control chars except newline/tab
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    # Normalize paragraph breaks
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse intra-line whitespace
    text = re.sub(r"[ \t]+", " ", text)
    # Strip leading/trailing whitespace on each line
    text = "\n".join(line.strip() for line in text.splitlines())
    return text.strip()


# ── Public API: extract full text ─────────────────────────────────────────────

def extract_text_from_pdf(file_path: str | Path) -> str:
    """
    Extract and clean all text from a PDF.

    Strategy:
      1. Try PyPDF2 (fast, handles most PDFs).
      2. Fall back to pdfminer.six (slower, handles complex layouts).

    Returns
    -------
    str
        Full cleaned text with per-page markers, or '' on total failure.
    """
    path = Path(file_path)
    if not path.exists():
        logger.error("PDF not found: %s", path)
        return ""

    # Engine 1 — PyPDF2
    pages = _extract_with_pypdf2(path)

    # Engine 2 — pdfminer fallback
    if not pages:
        logger.info("Falling back to pdfminer for %s", path.name)
        pages = _extract_with_pdfminer(path)

    if not pages:
        logger.error("All extraction engines failed for %s", path.name)
        return ""

    # Combine pages with markers for provenance
    parts = []
    for p in pages:
        cleaned = _clean_text(p.text)
        if cleaned:
            parts.append(f"[Page {p.page_number}]\n{cleaned}")

    full_text = "\n\n".join(parts)
    logger.info("Extracted %d chars from %d pages of %s", len(full_text), len(pages), path.name)
    return full_text


# ── Sentence-aware chunking ───────────────────────────────────────────────────

# Sentence-ending punctuation followed by whitespace and a capital letter
_SENTENCE_END = re.compile(r'(?<=[.!?])\s+(?=[A-Z\["])')


def _split_into_sentences(text: str) -> list[str]:
    """Split *text* into individual sentences (rough NLP-free approach)."""
    # Split on sentence boundaries
    parts = _SENTENCE_END.split(text)
    # Further split on newlines (each paragraph line may be a logical unit)
    sentences = []
    for part in parts:
        for line in part.strip().splitlines():
            line = line.strip()
            if line:
                sentences.append(line)
    return sentences


def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[str]:
    """
    Split *text* into overlapping chunks suitable for embedding.

    Unlike a naive character-split, this approach:
      • Builds chunks sentence by sentence so no sentence is broken mid-way.
      • Carries the last ``overlap`` characters of each chunk into the next,
        preserving cross-boundary context for the retriever.

    Parameters
    ----------
    text : str
        Full document text (from extract_text_from_pdf).
    chunk_size : int
        Target character count per chunk (soft limit — never breaks a sentence).
    overlap : int
        Characters of trailing context carried into the next chunk.

    Returns
    -------
    list[str]
        Deduplicated, non-empty text chunks ready for embedding.
    """
    if not text.strip():
        return []

    sentences = _split_into_sentences(text)
    chunks: list[str] = []
    current_parts: list[str] = []
    current_len: int = 0

    for sentence in sentences:
        sentence_len = len(sentence)

        # If adding this sentence would exceed the chunk size, flush
        if current_len + sentence_len > chunk_size and current_parts:
            chunk = " ".join(current_parts).strip()
            if chunk:
                chunks.append(chunk)

            # Keep overlap: walk back from the end until we have ~overlap chars
            overlap_parts: list[str] = []
            overlap_len = 0
            for part in reversed(current_parts):
                if overlap_len + len(part) > overlap:
                    break
                overlap_parts.insert(0, part)
                overlap_len += len(part)

            current_parts = overlap_parts
            current_len = overlap_len

        current_parts.append(sentence)
        current_len += sentence_len

    # Final chunk
    if current_parts:
        chunk = " ".join(current_parts).strip()
        if chunk:
            chunks.append(chunk)

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for c in chunks:
        if c not in seen:
            seen.add(c)
            unique.append(c)

    logger.debug("Produced %d chunks from %d chars", len(unique), len(text))
    return unique
