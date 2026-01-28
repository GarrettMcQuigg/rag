"""
LLM generation using Ollama.
"""

import requests


def generate_response(query: str, context: str, history: str = "", model: str = "llama3.2") -> str:
    """
    Generate a response using Ollama with retrieved context and conversation history.
    """
    prompt = f"""You are a company policy assistant that ONLY answers questions about the Acme Corporation Employee Handbook and IT Security Policy.

Rules:
- Only answer questions related to the provided context about company policies
- Keep responses concise and direct
- Always try to apply what the user is asking to the company policies documents
- If the user asks about ANYTHING else (casual chat, general questions, off-topic requests), respond with:
  "I can only answer questions about the Acme Corporation Employee Handbook and IT Security Policy. Here are some things you can ask me:
  - How much PTO do I get?
  - What are the password requirements?
  - Can I work from home?
  - What's the dress code?
  - How do I report a security incident?"

Context:
{context}

{f"Conversation History:{chr(10)}{history}" if history else ""}

User: {query}

Response:"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()