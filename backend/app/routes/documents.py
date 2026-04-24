"""
Documents route - list and manage uploaded documents.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.services.chroma_service import delete_collection

router = APIRouter()


@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    """List all uploaded documents."""
    docs = db.query(Document).order_by(Document.upload_date.desc()).all()
    return [
        {
            "id": doc.id,
            "name": doc.name,
            "filename": doc.original_filename,
            "file_type": doc.file_type,
            "chunk_count": doc.chunk_count,
            "upload_date": doc.upload_date.isoformat(),
        }
        for doc in docs
    ]


@router.delete("/documents/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document and its embeddings."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    # Delete ChromaDB collection
    delete_collection(document_id)

    # Delete from MySQL
    db.delete(doc)
    db.commit()

    return {"message": f"Document '{doc.name}' deleted successfully."}
