"""
Vector store operations using Pinecone with integrated embeddings.
Handles connection, upserting, and querying the vector database.
"""

from pinecone import Pinecone
from src.config import Config

# Initialize Pinecone client
pc = Pinecone(api_key=Config.PINECONE_API_KEY)

# Model used for integrated embeddings (must match your index config)
EMBEDDING_MODEL = "llama-text-embed-v2"


def get_index():
    """Get the Pinecone index instance."""
    return pc.Index(Config.PINECONE_INDEX_NAME)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings using Pinecone's inference API.
    """
    embeddings = pc.inference.embed(
        model=EMBEDDING_MODEL, inputs=texts, parameters={"input_type": "passage"}
    )
    return [e.values for e in embeddings.data]


def embed_query(query: str) -> list[float]:
    """
    Generate embedding for a query using Pinecone's inference API.
    """
    embeddings = pc.inference.embed(
        model=EMBEDDING_MODEL, inputs=[query], parameters={"input_type": "query"}
    )
    return embeddings.data[0].values


def upsert_documents(documents: list[dict]) -> dict:
    """
    Upsert documents to Pinecone.
    """
    index = get_index()

    # Extract texts for embedding
    texts = [doc["text"] for doc in documents]

    # Generate embeddings via Pinecone inference
    embeddings = embed_texts(texts)

    # Prepare vectors for upsert
    vectors = []
    for doc, embedding in zip(documents, embeddings):
        vector = {
            "id": doc["id"],
            "values": embedding,
            "metadata": {"text": doc["text"], **(doc.get("metadata", {}))},
        }
        vectors.append(vector)

    # Upsert to Pinecone
    response = index.upsert(vectors=vectors)
    return response


def query_documents(query_text: str, top_k: int = 5) -> list[dict]:
    """
    Query Pinecone.
    """
    index = get_index()

    # Embed the query
    query_embedding = embed_query(query_text)

    # Query Pinecone
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    return results.matches


def delete_all_documents(namespace: str = "") -> None:
    """Delete all documents from the index."""
    index = get_index()
    index.delete(delete_all=True, namespace=namespace)


def get_index_stats() -> dict:
    """Get statistics about the Pinecone index."""
    index = get_index()
    return index.describe_index_stats()
