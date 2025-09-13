from pydantic import BaseModel
from typing import List, Optional

class EventCreateSchema(BaseModel):
    start_datetime: str
    end_datetime: str
    summary: str
    location: Optional[str] = None
    description: Optional[str] = None
    attendees: List[str] = []

class EventUpdateSchema(BaseModel):
    start_datetime: Optional[str] = None
    end_datetime: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    attendees: Optional[List[str]] = None