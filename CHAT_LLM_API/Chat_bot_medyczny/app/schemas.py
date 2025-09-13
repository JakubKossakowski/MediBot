# app/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

class AgentSettingsSchema(BaseModel):
    llm_model: str = Field(default="gpt-4o-mini")
    voice: str = Field(default="N0GCuK2B0qwWozQNTS8F")
    temperature: float = Field(default=0.7)
    language: str = Field(default="pl")
    tone: str = Field(default="friendly")
    clinic_address: str = Field(default="Ciepła 40E, 4 piętro, Białystok")
    available_hours: List[str] = Field(default_factory=lambda: ["09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00"])

    class Config:
        schema_extra = {
            "example": {
                "llm_model": "gpt-4o-mini",
                "voice": "N0GCuK2B0qwWozQNTS8F",
                "temperature": 0.7,
                "language": "pl",
                "tone": "friendly",
                "clinic_address": "Ciepła 40E, 4 piętro, Białystok",
                "available_hours": ["09:00","10:00","11:00"]
            }
        }
