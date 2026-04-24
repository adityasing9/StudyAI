"""
Exam route - generates MCQs and short answer questions from documents.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.services.chroma_service import get_all_chunks
from app.services.llm import generate_exam_questions

router = APIRouter()


class ExamRequest(BaseModel):
    document_id: int


@router.post("/exam")
async def generate_exam(request: ExamRequest, db: Session = Depends(get_db)):
    """Generate exam questions from a document."""

    doc = db.query(Document).filter(Document.id == request.document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    try:
        chunks = get_all_chunks(request.document_id)
        if not chunks:
            raise HTTPException(status_code=400, detail="No content found for this document.")

        exam = generate_exam_questions(chunks)
        return {
            "document_id": doc.id,
            "document_name": doc.name,
            "exam": exam,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating exam questions: {str(e)}")
