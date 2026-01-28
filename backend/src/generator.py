"""
LLM generation using Ollama.
"""

import requests


def generate_response(query: str, context: str, model: str = "llama3.2") -> str:
    """
    Generate a response using Ollama with retrieved context.
    """
    prompt = f"""You are a helpful assistant. Answer the user's question based on the provided context. 
If the context doesn't contain relevant information, say so.

Context:
{context}

Question: {query}

Answer:"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    
    return response.json()["response"].strip()