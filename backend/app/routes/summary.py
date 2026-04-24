"""
Summary route - generates structured document summaries.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.services.chroma_service import get_all_chunks
from app.services.llm import generate_summary

router = APIRouter()


class SummaryRequest(BaseModel):
    document_id: int


@router.post("/summary")
async def summarize_document(request: SummaryRequest, db: Session = Depends(get_db)):
    """Generate a structured summary of a document."""

    doc = db.query(Document).filter(Document.id == request.document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    try:
        # Get all document chunks
        chunks = get_all_chunks(request.document_id)
        if not chunks:
            raise HTTPException(status_code=400, detail="No content found for this document.")

        # Generate summary via LLM
        summary = generate_summary(chunks)
        return {
            "document_id": doc.id,
            "document_name": doc.name,
            "summary": summary,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")
