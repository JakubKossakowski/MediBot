from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
Chat_bot_medyczny.app.services.receptionist_llm import generate_receptionist_response
import uuid
Chat_bot_medyczny.app.core.settings_store import AgentSettings, SettingsStore

router = APIRouter(prefix="/api/settings", tags=["settings"])

class ChatInput(BaseModel):
    user_input: str
    session_id: Optional[str] = None

@router.post("/receptionist")
async def talk_to_receptionist(input: ChatInput):
    session_id = input.session_id or str(uuid.uuid4())
    result = generate_receptionist_response(session_id, input.user_input)
    return {"session_id": session_id, **result}

@router.get("", response_model=AgentSettings)
async def get_settings():
    return SettingsStore.get()


@router.put("", response_model=AgentSettings)
async def put_settings(payload: AgentSettings):
    return SettingsStore.update(payload)
