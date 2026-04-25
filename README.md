# 🧠 StudyAI — Mini NotebookLM for Students

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> An AI-powered study assistant that lets you upload documents and interact with them intelligently using RAG (Retrieval-Augmented Generation). Get answers, summaries, and exam questions — all grounded in your uploaded content.

---

## 🌐 Live Demo

[![Frontend Live](https://img.shields.io/badge/Frontend-Live-blue?logo=vercel)](https://studyai-frontend-deploy.vercel.app)
[![Backend API](https://img.shields.io/badge/Backend-API-green?logo=render)](https://studyai-hxwr.onrender.com/)

- 🔗 Frontend: https://studyai-frontend-deploy.vercel.app  
- 🔗 Backend: https://studyai-hxwr.onrender.com/

---

## 📖 Project Overview

**StudyAI** is a full-stack web application that transforms static documents into interactive study companions. Upload any PDF or TXT file, and the AI will answer your questions strictly based on the document content — no hallucination, no external knowledge.

### Key Capabilities
- 💬 **Chat with Documents** — Ask questions and get grounded answers with source proof
- 📊 **Smart Summaries** — One-line, bullet points, and detailed explanations
- 🎯 **Exam Mode** — Auto-generate MCQs and short answer questions
- 📌 **Source Highlighting** — See exactly which document chunks were used
- 🧠 **Adaptive AI** — Detects confusion and simplifies explanations automatically

---

## 🔄 How It Works — RAG Workflow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Upload PDF  │────▶│ Extract Text │────▶│  Chunk Text  │
│   or TXT     │     │              │     │ (400 words)  │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                     ┌──────────────┐     ┌───────▼───────┐
                     │ Store in     │◀────│  Generate     │
                     │ ChromaDB     │     │  Embeddings   │
                     └──────┬───────┘     └───────────────┘
                            │
        ┌───────────────────▼───────────────────┐
        │         User Asks a Question          │
        └───────────────────┬───────────────────┘
                            │
                     ┌──────▼───────┐
                     │ Embed Query  │
                     │ & Search     │
                     │ ChromaDB     │
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐     ┌──────────────┐
                     │ Top-K Chunks │────▶│  LLM (via    │
                     │ Retrieved    │     │ OpenRouter)  │
                     └──────────────┘     └──────┬───────┘
                                                  │
                     ┌──────────────┐     ┌───────▼───────┐
                     │  Display     │◀────│  Answer +     │
                     │  in Chat UI  │     │  Source Proof  │
                     └──────────────┘     └───────────────┘
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📂 Document Upload | Upload PDF/TXT, auto-extract and embed |
| 💬 RAG Chat | Context-aware Q&A with source grounding |
| 📊 Smart Summary | 1-line, bullet points, detailed breakdown |
| 🎯 Exam Mode | MCQs (4 options) + short answer questions |
| 📌 Source Proof | Highlighted document chunks per answer |
| 🧠 Adaptive AI | Auto-detects confusion, simplifies response |
| 🎚️ Explain Levels | Beginner / Intermediate / Expert toggle |
| 📜 Chat History | Persistent conversation per document |

---

## 🏗️ System Architecture

```
Frontend (React + Vite)          Backend (FastAPI)
┌─────────────────────┐          ┌─────────────────────┐
│  Sidebar             │          │  /api/upload         │
│  TopBar              │  HTTP    │  /api/chat           │
│  ChatPanel           │◀────────▶│  /api/summary        │
│  ResultModal         │          │  /api/exam           │
│                      │          │  /api/documents      │
└─────────────────────┘          └──────────┬──────────┘
                                            │
                           ┌────────────────┼────────────────┐
                           │                │                │
                    ┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐
                    │   MySQL     │  │  ChromaDB   │  │ OpenRouter │
                    │  (metadata) │  │ (embeddings)│  │   (LLM)    │
                    └─────────────┘  └─────────────┘  └────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vanilla CSS, Vite |
| Backend | Python 3.10+, FastAPI, Uvicorn |
| SQL Database | MySQL 8.0+ |
| Vector Database | ChromaDB (persistent, local) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | OpenRouter API (Gemini Flash) |
| Text Extraction | PyPDF2 |

---

## 📁 Project Structure

```
NoteBook/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Environment configuration
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models/
│   │   │   ├── document.py      # Document model
│   │   │   └── chat.py          # Chat history model
│   │   ├── routes/
│   │   │   ├── upload.py        # File upload endpoint
│   │   │   ├── chat.py          # RAG chat endpoint
│   │   │   ├── summary.py       # Summary endpoint
│   │   │   ├── exam.py          # Exam generation endpoint
│   │   │   └── documents.py     # Document management
│   │   └── services/
│   │       ├── pdf_parser.py    # Text extraction & chunking
│   │       ├── embedding.py     # Sentence-transformers embeddings
│   │       ├── chroma_service.py# ChromaDB operations
│   │       └── llm.py           # OpenRouter LLM integration
│   ├── .env                     # Environment variables
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main application
│   │   ├── api.js               # API service layer
│   │   └── components/
│   │       ├── Sidebar.jsx/css  # Document sidebar
│   │       ├── TopBar.jsx/css   # Action bar
│   │       ├── ChatPanel.jsx/css# Chat interface
│   │       └── ResultModal.jsx/css # Summary/Exam display
│   ├── index.html
│   └── package.json
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload and process a document |
| `POST` | `/api/chat` | Ask a question (RAG) |
| `GET` | `/api/chat/history/{id}` | Get chat history for a document |
| `POST` | `/api/summary` | Generate document summary |
| `POST` | `/api/exam` | Generate exam questions |
| `GET` | `/api/documents` | List all documents |
| `DELETE` | `/api/documents/{id}` | Delete a document |

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL 8.0+ (running locally)
- OpenRouter API key

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/StudyAI.git
cd StudyAI
```

### 2. Setup MySQL Database
```sql
CREATE DATABASE studyai;
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 4. Configure Environment
Edit `backend/.env`:
```env
OPENROUTER_API_KEY=your_key_here
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=studyai
```

### 5. Start Backend
```bash
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```

### 6. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 7. Open App
Visit `http://localhost:5173` in your browser.

---

## 📘 Usage Guide

1. **Upload** — Click "Upload Document" in the sidebar and select a PDF or TXT file
2. **Select** — Click on the document in the sidebar to activate it
3. **Chat** — Type questions in the chat input to get AI answers with source proof
4. **Summarize** — Click "Summarize" in the top bar for structured summaries
5. **Exam Mode** — Click "Exam Mode" to generate MCQs and short answer questions
6. **Explain Level** — Use the dropdown to switch between Beginner/Intermediate/Expert
7. **Adaptive Mode** — Toggle ON to let AI auto-detect confusion and simplify

---

## 💡 Unique Value

- **Zero Hallucination** — All answers are strictly grounded in uploaded content
- **Source Transparency** — Every answer shows the exact document chunks used
- **Adaptive Intelligence** — Automatically adjusts complexity based on user confusion
- **Study-Optimized** — Purpose-built for students with summaries and exam generation

---

## 📝 Final Note

StudyAI demonstrates a production-grade RAG architecture combining modern frontend design with a robust AI backend. The system ensures factual accuracy through retrieval-augmented generation while providing an intuitive, premium user experience.

Built with ❤️ for students who want to study smarter.
