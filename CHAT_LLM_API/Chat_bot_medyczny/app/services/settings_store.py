# app/services/settings_store.py
from Chat_bot_medyczny.app.db import get_session
from Chat_bot_medyczny.app.models import AgentSettings
from Chat_bot_medyczny.app.schemas import AgentSettingsSchema
from sqlmodel import select
from typing import Optional

def get_settings_from_db() -> AgentSettings:
    session = get_session()
    try:
        stmt = select(AgentSettings).limit(1)
        result = session.exec(stmt).first()
        if not result:
            defaults = AgentSettings()
            session.add(defaults)
            session.commit()
            session.refresh(defaults)
            return defaults
        return result
    finally:
        session.close()

def update_settings_in_db(new: AgentSettingsSchema) -> AgentSettings:
    session = get_session()
    try:
        stmt = select(AgentSettings).limit(1)
        existing = session.exec(stmt).first()
        if not existing:
            existing = AgentSettings()
            session.add(existing)
        # update fields
        existing.llm_model = new.llm_model
        existing.voice = new.voice
        existing.temperature = new.temperature
        existing.language = new.language
        existing.tone = new.tone
        existing.clinic_address = new.clinic_address
        import json
        existing.available_hours_json = json.dumps(new.available_hours)
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    finally:
        session.close()
