from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    id: int
    name: str
    email: str

class Event(BaseModel):
    start_datetime: str
    end_datetime: str
    summary: str
    location: Optional[str] = None
    description: Optional[str] = None
    attendees: List[str] = []
