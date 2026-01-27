"""
Vector store operations using Pinecone with integrated embeddings.
Handles connection, upserting, and querying the vector database.
"""

from pinecone import Pinecone
from src.config import Config


def get_pinecone_client() -> Pinecone:
    """Initialize and return Pinecone client."""
    return Pinecone(api_key=Config.PINECONE_API_KEY)


def get_index():
    """Get the Pinecone index instance."""
    pc = get_pinecone_client()
    return pc.Index(Config.PINECONE_INDEX_NAME)


def upsert_documents(documents: list[dict]) -> dict:
    """
    Upsert documents to Pinecone using integrated embeddings.
    
    Args:
        documents: List of dicts with 'id', 'text', and optional 'metadata' keys.
                   Example: [{"id": "doc1", "text": "Hello world", "metadata": {"source": "test"}}]
    
    Returns:
        Upsert response from Pinecone.
    """
    index = get_index()
    
    # Format records for Pinecone integrated embeddings
    # The index is configured to embed the "text" field automatically
    records = []
    for doc in documents:
        record = {
            "id": doc["id"],
            "_text": doc["text"],  # This field gets embedded automatically
        }
        # Add metadata if present
        if "metadata" in doc:
            record.update(doc["metadata"])
        records.append(record)
    
    # Upsert to Pinecone
    response = index.upsert_from_text(
        records=records,
        namespace=""
    )
    
    return response


def query_documents(query_text: str, top_k: int = 5) -> list[dict]:
    """
    Query Pinecone using integrated embeddings.
    
    Args:
        query_text: The search query string.
        top_k: Number of results to return.
    
    Returns:
        List of matching documents with scores.
    """
    index = get_index()
    
    # Query using integrated embeddings - Pinecone embeds the query automatically
    results = index.query_from_text(
        query=query_text,
        top_k=top_k,
        include_metadata=True
    )
    
    return results.matches


def delete_all_documents(namespace: str = "") -> None:
    """Delete all documents from the index (useful for testing)."""
    index = get_index()
    index.delete(delete_all=True, namespace=namespace)


def get_index_stats() -> dict:
    """Get statistics about the Pinecone index."""
    index = get_index()
    return index.describe_index_stats()
