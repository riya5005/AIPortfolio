import time
from collections import defaultdict, deque
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional

from app.config import FRONTEND_ORIGIN
from app.agent.graph import run_agent, classify_intent
from app.db import init_db, log_chat

app = FastAPI(title="Riya Portfolio Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


RATE_LIMIT = 10
WINDOW_SECONDS = 60
_request_log: dict[str, deque] = defaultdict(deque)


def check_rate_limit(ip: str):
    now = time.time()
    window = _request_log[ip]
    while window and now - window[0] > WINDOW_SECONDS:
        window.popleft()
    if len(window) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests — please slow down.")
    window.append(now)


@app.on_event("startup")
def on_startup():
    init_db()


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None


class ChatResponse(BaseModel):
    answer: str
    intent: str
    flagged: bool


SUGGESTED_PROMPTS = [
    "What are Riya's qualifications?",
    "Which tech stack does Riya know?",
    "Tell me about her ML projects",
    "Give me her LinkedIn and GitHub links",
]


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/suggested-prompts")
def suggested_prompts():
    return {"prompts": SUGGESTED_PROMPTS}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request):
    check_rate_limit(request.client.host)

    history = (req.history or [])[-6:]
    start = time.time()

    result = run_agent(req.message, history=history)
    latency_ms = (time.time() - start) * 1000

    log_chat(
        question=req.message,
        answer=result["answer"],
        intent=result.get("intent", ""),
        flagged=result.get("flagged", False),
        flag_reason=result.get("flag_reason", ""),
        latency_ms=latency_ms,
    )

    return ChatResponse(
        answer=result["answer"],
        intent=result.get("intent", ""),
        flagged=result.get("flagged", False),
    )