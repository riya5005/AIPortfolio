from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@app.on_event("startup")
def on_startup():
    init_db()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    intent: str


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
def chat(req: ChatRequest):
    answer = run_agent(req.message)
    intent_state = classify_intent({"question": req.message, "intent": "", "context": "", "answer": ""})
    intent = intent_state["intent"]

    log_chat(question=req.message, answer=answer, intent=intent)

    return ChatResponse(answer=answer, intent=intent)
