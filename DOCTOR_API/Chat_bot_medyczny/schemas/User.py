from pydantic import BaseModel, EmailStr
from typing import Optional

class DoctorCreate(BaseModel):
    imie: str
    nazwisko: str
    klasyfikacja: str
    email: EmailStr

class DoctorUpdate(BaseModel):
    imie: Optional[str]
    nazwisko: Optional[str]
    klasyfikacja: Optional[str]
    email: Optional[EmailStr]
