"""The FastAPI web application for SupportGenie."""

from fastapi import FastAPI

from supportgenie.schemas import ChatRequest, ChatResponse
from supportgenie.generator import answer as generate_answer

app = FastAPI(title="SupportGenie API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "SupportGenie"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = generate_answer(request.question)
    return ChatResponse(answer=reply)