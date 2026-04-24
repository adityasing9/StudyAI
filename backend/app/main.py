"""
StudyAI Backend - FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router
from app.routes.summary import router as summary_router
from app.routes.exam import router as exam_router
from app.routes.documents import router as documents_router

app = FastAPI(
    title="StudyAI API",
    description="AI-powered study assistant with RAG-based document Q&A",
    version="1.0.0",
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all route modules
app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(summary_router, prefix="/api", tags=["Summary"])
app.include_router(exam_router, prefix="/api", tags=["Exam"])
app.include_router(documents_router, prefix="/api", tags=["Documents"])


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    init_db()
    print("[OK] StudyAI Backend started successfully!")
    print("[OK] Database tables initialized.")


@app.get("/")
async def root():
    return {
        "name": "StudyAI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }
