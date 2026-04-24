"""
Upload route - handles file upload, text extraction, chunking, and embedding.
"""
import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import UPLOAD_DIR
from app.models.document import Document
from app.services.pdf_parser import extract_text_from_file, chunk_text
from app.services.embedding import generate_embeddings
from app.services.chroma_service import store_chunks

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a PDF or TXT file, extract text, chunk it, and store embeddings."""

    # Validate file type
    filename = file.filename or "unknown"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ("pdf", "txt"):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")

    # Save file to disk
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        # Extract text
        text = extract_text_from_file(file_path, ext)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract any text from the file.")

        # Chunk text
        chunks = chunk_text(text)
        if not chunks:
            raise HTTPException(status_code=400, detail="No text chunks were generated from the file.")

        # Save document metadata to MySQL
        doc = Document(
            name=filename.rsplit(".", 1)[0],
            original_filename=filename,
            file_type=ext,
            chunk_count=len(chunks),
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        # Generate embeddings
        embeddings = generate_embeddings(chunks)

        # Store in ChromaDB
        store_chunks(doc.id, chunks, embeddings)

        return {
            "id": doc.id,
            "name": doc.name,
            "filename": doc.original_filename,
            "file_type": doc.file_type,
            "chunk_count": doc.chunk_count,
            "upload_date": doc.upload_date.isoformat(),
            "message": f"Document '{filename}' uploaded and processed successfully.",
        }

    except HTTPException:
        raise
    except Exception as e:
        # Clean up on failure
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
