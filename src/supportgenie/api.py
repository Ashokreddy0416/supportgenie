"""The FastAPI web application for SupportGenie."""

import logging

from fastapi import FastAPI, HTTPException, Depends

from supportgenie.schemas import ChatRequest, ChatResponse
from supportgenie.cached_answer import answer_with_cache
from supportgenie.auth.routes import router as auth_router
from supportgenie.auth.dependencies import get_current_user, require_role
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger("supportgenie.api")

app = FastAPI(title="SupportGenie API", version="0.1.0")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "SupportGenie"}


@app.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
def chat(request: Request, chat_request: ChatRequest, user=Depends(get_current_user)):
    logger.info("Chat request from user '%s': %s", user["username"], chat_request.question[:80])
    try:
        result = answer_with_cache(chat_request.question)
        reply = result["answer"]
    except Exception:
        logger.exception("Failed to generate answer")
        raise HTTPException(
            status_code=503,
            detail="SupportGenie is temporarily unavailable. Please try again shortly.",
        )
    logger.info("Answer generated successfully")
    return ChatResponse(answer=reply)

@app.get("/admin/stats")
def admin_stats(user=Depends(require_role("admin"))):
    return {"message": f"Welcome admin {user['username']}", "total_users": "stats would go here"}