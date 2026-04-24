"""
Embedding service using sentence-transformers for local embedding generation.
Uses the lightweight all-MiniLM-L6-v2 model for fast, free embeddings.
"""
from sentence_transformers import SentenceTransformer

# Load model once at module level for efficiency
_model = None


def get_model() -> SentenceTransformer:
    """Lazy-load the embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of text strings."""
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


def generate_query_embedding(query: str) -> list[float]:
    """Generate embedding for a single query string."""
    model = get_model()
    embedding = model.encode([query], show_progress_bar=False)
    return embedding[0].tolist()
