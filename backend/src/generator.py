"""
LLM generation using Ollama.
"""

import logging
import requests

logger = logging.getLogger(__name__)


def generate_response(
    query: str, context: str, history: str = "", model: str = "llama3.2"
) -> str:
    """
    Generate a response using Ollama with retrieved context and conversation history.
    """
    prompt = f"""You are a company policy assistant that ONLY answers questions about the Acme Corporation Employee Handbook and IT Security Policy.

Rules:
- Only answer questions related to the provided context about company policies
- Keep responses concise and direct
- Always try to apply what the user is asking to the company policy documents
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

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.exceptions.Timeout:
        logger.error("Ollama request timed out")
        return "I'm sorry, but I'm having trouble processing your request right now. Please try again later."
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama request failed: {type(e).__name__}")
        return "I'm sorry, but I'm having trouble processing your request right now. Please try again later."
    except (KeyError, ValueError) as e:
        logger.error(f"Failed to parse Ollama response: {type(e).__name__}")
        return "I'm sorry, but I'm having trouble processing your request right now. Please try again later."
