"""
Chat route - handles RAG-based Q&A with document context.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.models.chat import Chat
from app.services.embedding import generate_query_embedding
from app.services.chroma_service import query_chunks
from app.services.llm import chat_with_document, detect_confusion

router = APIRouter()


class ChatRequest(BaseModel):
    document_id: int
    question: str
    explain_level: str = "intermediate"
    adaptive_mode: bool = False


@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Process a chat question using RAG architecture."""

    # Validate document exists
    doc = db.query(Document).filter(Document.id == request.document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        # Generate query embedding
        query_embedding = generate_query_embedding(request.question)

        # Retrieve relevant chunks from ChromaDB
        results = query_chunks(request.document_id, query_embedding, n_results=5)

        documents = results.get("documents", [[]])[0]
        if not documents:
            return {
                "answer": "I couldn't find relevant information in the uploaded document for your question.",
                "sources": [],
                "confusion_detected": False,
                "effective_level": request.explain_level,
            }

        # Send to LLM with context
        llm_response = chat_with_document(
            context_chunks=documents,
            question=request.question,
            level=request.explain_level,
            adaptive=request.adaptive_mode,
        )

        # Save chat to MySQL
        chat_record = Chat(
            document_id=request.document_id,
            question=request.question,
            answer=llm_response["answer"],
            explain_level=llm_response["effective_level"],
        )
        db.add(chat_record)
        db.commit()

        return {
            "answer": llm_response["answer"],
            "sources": documents,
            "confusion_detected": llm_response["confusion_detected"],
            "effective_level": llm_response["effective_level"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@router.get("/chat/history/{document_id}")
async def get_chat_history(document_id: int, db: Session = Depends(get_db)):
    """Get chat history for a specific document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    chats = db.query(Chat).filter(Chat.document_id == document_id).order_by(Chat.timestamp.asc()).all()
    return [
        {
            "id": chat.id,
            "question": chat.question,
            "answer": chat.answer,
            "explain_level": chat.explain_level,
            "timestamp": chat.timestamp.isoformat(),
        }
        for chat in chats
    ]
