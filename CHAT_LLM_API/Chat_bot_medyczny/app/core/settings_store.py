from __future__ import annotations
from pydantic import BaseModel, Field
from threading import Lock
from typing import Optional

class AgentSettings(BaseModel):
    llm_model: str = Field(default="gpt-4o-mini")
    voice: str = Field(default="d4Z5Fvjohw3zxGpV8XUV")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    language: str = Field(default="pl")
    tone: str = Field(default="friendly")
    # Możesz dodać: system_prompt: Optional[str], max_tokens: Optional[int], provider: Optional[str], itp.

class SettingsStore:
    _settings: AgentSettings = AgentSettings()
    _lock: Lock = Lock()

    @classmethod
    def get(cls) -> AgentSettings:
        with cls._lock:
            # .copy() jeśli chcesz uniknąć mutacji referencyjnych
            return cls._settings

    @classmethod
    def update(cls, data: AgentSettings) -> AgentSettings:
        with cls._lock:
            cls._settings = data
            return cls._settings
