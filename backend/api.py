"""
FastAPI backend for RAG chatbot.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.retriever import retrieve_as_context
from src.generator import generate_response

app = FastAPI(title="RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str
    history: list[dict] = []


class ChatResponse(BaseModel):
    answer: str


@app.post("/api/ask", response_model=ChatResponse)
def ask(request: ChatRequest):
    # Build history string from recent messages
    history = ""
    for msg in request.history[-6:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"

    # RAG pipeline
    context = retrieve_as_context(request.query, top_k=3)
    answer = generate_response(request.query, context, history)

    return ChatResponse(answer=answer)


@app.get("/api/health")
def health():
    return {"status": "ok"}