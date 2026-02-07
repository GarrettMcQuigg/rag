"""
FastAPI backend for RAG chatbot.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field, constr
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from src.retriever import retrieve_as_context
from src.generator import generate_response

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="RAG Chatbot API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


class ChatRequest(BaseModel):
    query: constr(max_length=1000)
    history: list[dict] = Field(default=[], max_length=20)


class ChatResponse(BaseModel):
    answer: str


@app.post("/api/ask", response_model=ChatResponse)
@limiter.limit("10/minute")
def ask(request: Request, chat_request: ChatRequest):
    # Build history string from recent messages
    history = ""
    for msg in chat_request.history[-6:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"

    # RAG pipeline
    context = retrieve_as_context(chat_request.query, top_k=3)
    answer = generate_response(chat_request.query, context, history)

    return ChatResponse(answer=answer)


@app.get("/api/health")
def health():
    return {"status": "ok"}
