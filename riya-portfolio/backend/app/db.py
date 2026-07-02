"""
Optional: logs every chat exchange to PostgreSQL so you can see what visitors
ask. The app works fine without this — if DATABASE_URL isn't set, logging is
silently skipped.
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
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
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    global engine, SessionLocal
    if not DATABASE_URL:
        return
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)


def log_chat(question: str, answer: str, intent: str = ""):
    if SessionLocal is None:
        return
    db = SessionLocal()
    try:
        db.add(ChatLog(question=question, answer=answer, intent=intent))
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()
