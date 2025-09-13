# app/api/routes/settings.py
from fastapi import APIRouter, HTTPException
from Chat_bot_medyczny.app.schemas import AgentSettingsSchema
from Chat_bot_medyczny.app.services.settings_store import get_settings_from_db, update_settings_in_db

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("", response_model=AgentSettingsSchema)
def get_settings():
    db_settings = get_settings_from_db()
    return AgentSettingsSchema(
        llm_model=db_settings.llm_model,
        voice=db_settings.voice,
        temperature=db_settings.temperature,
        language=db_settings.language,
        tone=db_settings.tone,
        clinic_address=db_settings.clinic_address,
        available_hours=db_settings.available_hours()
    )

@router.put("", response_model=AgentSettingsSchema)
def put_settings(payload: AgentSettingsSchema):
    updated = update_settings_in_db(payload)
    return AgentSettingsSchema(
        llm_model=updated.llm_model,
        voice=updated.voice,
        temperature=updated.temperature,
        language=updated.language,
        tone=updated.tone,
        clinic_address=updated.clinic_address,
        available_hours=updated.available_hours()
    )
