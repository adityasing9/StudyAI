"""
Embedding service using chromadb's ONNX-based embeddings for low memory usage.
Uses the lightweight all-MiniLM-L6-v2 model via ONNX.
"""
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

# Load model once at module level for efficiency
_model = None


def get_model():
    """Lazy-load the embedding model."""
    global _model
    if _model is None:
        # This uses ONNX and tokenizers instead of PyTorch, saving ~1GB+ of RAM
        _model = ONNXMiniLM_L6_V2()
    return _model


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of text strings."""
    model = get_model()
    # ONNXMiniLM_L6_V2 returns list[list[float]] when called
    return model(texts)


def generate_query_embedding(query: str) -> list[float]:
    """Generate embedding for a single query string."""
    model = get_model()
    return model([query])[0]
