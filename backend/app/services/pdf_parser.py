"""
PDF and TXT text extraction and chunking service.
"""
import os
from PyPDF2 import PdfReader
from app.config import CHUNK_SIZE, CHUNK_OVERLAP


def extract_text_from_file(file_path: str, file_type: str) -> str:
    """Extract raw text from a PDF or TXT file."""
    if file_type == "pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    elif file_type == "txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping chunks based on word count.
    Each chunk is approximately chunk_size words with overlap words of overlap.
    """
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk.strip())
        if end >= len(words):
            break
        start = end - overlap

    return chunks
