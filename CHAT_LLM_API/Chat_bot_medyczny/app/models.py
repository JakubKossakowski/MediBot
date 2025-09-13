# app/models.py
from sqlmodel import SQLModel, Field
from typing import Optional, List
import json

class AgentSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    llm_model: str = Field(default="gpt-4o-mini")
    voice: str = Field(default="N0GCuK2B0qwWozQNTS8F")
    temperature: float = Field(default=0.7)
    language: str = Field(default="pl")
    tone: str = Field(default="friendly")
    clinic_address: str = Field(default="Ciepła 40E, 4 piętro, Białystok")
    available_hours_json: str = Field(default='["09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00"]')

    def available_hours(self) -> List[str]:
        try:
            return json.loads(self.available_hours_json)
        except Exception:
            return ["09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00"]
