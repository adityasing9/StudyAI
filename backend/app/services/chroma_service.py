"""
ChromaDB service for storing and retrieving document embeddings.
"""
import chromadb
from app.config import CHROMA_PERSIST_DIR

# Initialize ChromaDB client with persistent storage
_client = None


def get_chroma_client():
    """Lazy-load the ChromaDB client."""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    return _client


def get_or_create_collection(document_id: int):
    """Get or create a ChromaDB collection for a specific document."""
    client = get_chroma_client()
    collection_name = f"doc_{document_id}"
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )


def store_chunks(document_id: int, chunks: list[str], embeddings: list[list[float]]):
    """Store document chunks and their embeddings in ChromaDB."""
    collection = get_or_create_collection(document_id)
    ids = [f"chunk_{document_id}_{i}" for i in range(len(chunks))]
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
    )
    return len(chunks)


def query_chunks(document_id: int, query_embedding: list[float], n_results: int = 5) -> dict:
    """Query ChromaDB for the most relevant chunks to the query."""
    collection = get_or_create_collection(document_id)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
    )
    return results


def get_all_chunks(document_id: int) -> list[str]:
    """Retrieve all chunks for a document from ChromaDB."""
    collection = get_or_create_collection(document_id)
    count = collection.count()
    if count == 0:
        return []
    results = collection.get(limit=count)
    return results.get("documents", [])


def delete_collection(document_id: int):
    """Delete a document's collection from ChromaDB."""
    client = get_chroma_client()
    collection_name = f"doc_{document_id}"
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
