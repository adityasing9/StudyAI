"""
LLM service for interacting with OpenRouter API.
Handles all prompt engineering for chat, summary, and exam modes.
"""
import json
import re
from openai import OpenAI
from app.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODEL

_client = None


def get_llm_client() -> OpenAI:
    """Lazy-load the OpenAI-compatible client for OpenRouter."""
    global _client
    if _client is None:
        _client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=OPENROUTER_API_KEY,
        )
    return _client


# --- Confusion Detection ---
CONFUSION_KEYWORDS = [
    "i don't understand", "i dont understand", "explain again",
    "simplify", "what do you mean", "confused", "huh", "what?",
    "can you explain", "break it down", "too complex", "too hard",
    "not clear", "unclear", "lost", "elaborate", "simpler",
]


def detect_confusion(query: str) -> bool:
    """Detect if the user is confused based on keywords in their query."""
    query_lower = query.lower().strip()
    return any(keyword in query_lower for keyword in CONFUSION_KEYWORDS)


# --- Prompt Templates ---
def _get_explain_instruction(level: str) -> str:
    """Return prompt instructions based on explanation level."""
    instructions = {
        "beginner": (
            "Explain in very simple language that a high school student would understand. "
            "Use everyday analogies and examples. Break complex ideas into small steps. "
            "Avoid jargon. If you must use a technical term, define it immediately."
        ),
        "intermediate": (
            "Explain in a balanced way suitable for a college student. "
            "Use proper terminology but provide brief clarifications where needed. "
            "Include relevant examples."
        ),
        "expert": (
            "Explain with full technical depth suitable for a graduate student or professional. "
            "Use precise terminology, reference underlying principles, and provide "
            "nuanced analysis. Assume strong foundational knowledge."
        ),
    }
    return instructions.get(level, instructions["intermediate"])


def _build_chat_prompt(context: str, question: str, level: str, adaptive: bool, is_confused: bool) -> str:
    """Build the system prompt for chat/Q&A."""
    explain_instruction = _get_explain_instruction(level)

    # Override to beginner if adaptive mode detects confusion
    effective_level = level
    if adaptive and is_confused:
        effective_level = "beginner"
        explain_instruction = _get_explain_instruction("beginner")

    confusion_addon = ""
    if adaptive and is_confused:
        confusion_addon = (
            "\n\nThe user seems confused. Please:\n"
            "- Break your answer into numbered steps\n"
            "- Use a simple analogy or real-world example\n"
            "- Start with the most basic concept and build up\n"
            "- Keep sentences short and clear\n"
        )

    system_prompt = f"""You are StudyAI, an intelligent study assistant. You answer questions STRICTLY based on the provided document context. Do NOT use any external knowledge or make up information.

RULES:
1. Answer ONLY based on the document context below.
2. If the answer is not in the context, say: "I couldn't find this information in the uploaded document."
3. Be accurate and helpful.
4. {explain_instruction}
{confusion_addon}

DOCUMENT CONTEXT:
---
{context}
---"""

    return system_prompt


def chat_with_document(context_chunks: list[str], question: str, level: str = "intermediate",
                       adaptive: bool = False) -> dict:
    """Send a RAG query to the LLM and return the answer."""
    client = get_llm_client()
    context = "\n\n".join(context_chunks)
    is_confused = detect_confusion(question) if adaptive else False

    system_prompt = _build_chat_prompt(context, question, level, adaptive, is_confused)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    answer = response.choices[0].message.content
    return {
        "answer": answer,
        "confusion_detected": is_confused,
        "effective_level": "beginner" if (adaptive and is_confused) else level,
    }


def generate_summary(chunks: list[str]) -> dict:
    """Generate a structured summary from document chunks."""
    client = get_llm_client()
    context = "\n\n".join(chunks[:15])  # Use first 15 chunks for summary

    system_prompt = """You are StudyAI, a document summarization expert. Generate a comprehensive summary of the provided document content.

You MUST respond in valid JSON format with exactly this structure:
{
    "one_line": "A single concise sentence summarizing the entire document.",
    "bullet_points": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"],
    "detailed": "A detailed 2-3 paragraph explanation of the document content covering all major topics and key information."
}

RULES:
1. Base your summary STRICTLY on the provided content.
2. The bullet points should capture the 5 most important ideas.
3. The detailed summary should be comprehensive but concise.
4. Return ONLY valid JSON, no markdown code fences."""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Summarize this document:\n\n{context}"},
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content.strip()
    # Try to extract JSON from the response
    try:
        # Remove markdown code fences if present
        cleaned = re.sub(r'^```json\s*', '', raw)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "one_line": raw[:200],
            "bullet_points": [raw[:500]],
            "detailed": raw,
        }


def generate_exam_questions(chunks: list[str]) -> dict:
    """Generate exam questions from document chunks."""
    client = get_llm_client()
    context = "\n\n".join(chunks[:15])  # Use first 15 chunks

    system_prompt = """You are StudyAI, an exam question generator. Generate exam questions based STRICTLY on the provided document content.

You MUST respond in valid JSON format with exactly this structure:
{
    "mcqs": [
        {
            "question": "Question text?",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct": "A",
            "explanation": "Brief explanation of why this is correct."
        }
    ],
    "short_answers": [
        {
            "question": "Short answer question?",
            "answer": "Expected answer based on the document."
        }
    ]
}

RULES:
1. Generate exactly 5 MCQs and 3 short answer questions.
2. All questions MUST be based on the document content.
3. MCQ options should be plausible but only one correct.
4. Avoid vague or overly generic questions.
5. Return ONLY valid JSON, no markdown code fences."""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate exam questions from this document:\n\n{context}"},
        ],
        temperature=0.5,
        max_tokens=3000,
    )

    raw = response.choices[0].message.content.strip()
    try:
        cleaned = re.sub(r'^```json\s*', '', raw)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "mcqs": [],
            "short_answers": [],
            "raw_response": raw,
        }
