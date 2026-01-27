"""
Retrieval logic for the RAG application.
Handles querying the vector store and formatting results.
"""

from src.vectorstore import query_documents


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """
    Retrieve relevant documents for a query.
    
    Args:
        query: The search query string.
        top_k: Number of results to return.
    
    Returns:
        List of results with text, score, and metadata.
    """
    matches = query_documents(query, top_k=top_k)
    
    results = []
    for match in matches:
        result = {
            "id": match.id,
            "score": match.score,
            "text": match.metadata.get("_text", ""),
            "metadata": {k: v for k, v in match.metadata.items() if k != "_text"}
        }
        results.append(result)
    
    return results


def retrieve_as_context(query: str, top_k: int = 5) -> str:
    """
    Retrieve documents and format them as context for an LLM.
    
    Args:
        query: The search query string.
        top_k: Number of results to return.
    
    Returns:
        Formatted string containing retrieved context.
    """
    results = retrieve(query, top_k=top_k)
    
    if not results:
        return "No relevant context found."
    
    context_parts = []
    for i, result in enumerate(results, 1):
        source = result["metadata"].get("source", "unknown")
        context_parts.append(f"[{i}] (Source: {source}, Score: {result['score']:.3f})\n{result['text']}")
    
    return "\n\n---\n\n".join(context_parts)


def search_and_print(query: str, top_k: int = 5) -> None:
    """
    Search and print results in a readable format (for testing/debugging).
    
    Args:
        query: The search query string.
        top_k: Number of results to return.
    """
    print(f"\n🔍 Query: {query}")
    print("=" * 50)
    
    results = retrieve(query, top_k=top_k)
    
    if not results:
        print("No results found.")
        return
    
    for i, result in enumerate(results, 1):
        print(f"\n📄 Result {i} (Score: {result['score']:.3f})")
        print(f"   Source: {result['metadata'].get('source', 'unknown')}")
        print(f"   Text: {result['text'][:200]}{'...' if len(result['text']) > 200 else ''}")
