"""The FastAPI web application for SupportGenie."""

from fastapi import FastAPI

app = FastAPI(title="SupportGenie API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "SupportGenie"}