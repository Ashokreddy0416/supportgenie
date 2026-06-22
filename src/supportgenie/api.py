"""The FastAPI web application for SupportGenie."""

import logging

from fastapi import FastAPI, HTTPException

from supportgenie.schemas import ChatRequest, ChatResponse
from supportgenie.generator import answer as generate_answer
from supportgenie.auth.routes import router as auth_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger("supportgenie.api")

app = FastAPI(title="SupportGenie API", version="0.1.0")

app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "SupportGenie"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info("Received chat request: %s", request.question[:80])
    try:
        reply = generate_answer(request.question)
    except Exception:
        logger.exception("Failed to generate answer")
        raise HTTPException(
            status_code=503,
            detail="SupportGenie is temporarily unavailable. Please try again shortly.",
        )
    logger.info("Answer generated successfully")
    return ChatResponse(answer=reply)