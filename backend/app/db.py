from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

Base = declarative_base()
engine = None
SessionLocal = None


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    intent = Column(String, nullable=True)
    flagged = Column(Boolean, default=False)
    flag_reason = Column(String, nullable=True)
    latency_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    global engine, SessionLocal
    if not DATABASE_URL:
        return
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(bind=engine)
    except Exception as e:
        print(f"[warning] Could not connect to DATABASE_URL, chat logging disabled: {e}")
        engine = None
        SessionLocal = None


def log_chat(question: str, answer: str, intent: str = "", flagged: bool = False,
             flag_reason: str = "", latency_ms: float = None):
    if SessionLocal is None:
        return
    db = SessionLocal()
    try:
        db.add(ChatLog(
            question=question, answer=answer, intent=intent,
            flagged=flagged, flag_reason=flag_reason, latency_ms=latency_ms,
        ))
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()