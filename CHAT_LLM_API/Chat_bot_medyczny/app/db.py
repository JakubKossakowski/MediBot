# app/db.py
from sqlmodel import create_engine, SQLModel, Session, select
from typing import Optional
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agent_settings.db")

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    from Chat_bot_medyczny.app.models import AgentSettings
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
