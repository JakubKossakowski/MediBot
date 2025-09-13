from fastapi import FastAPI
from models.User import Base  # jeśli plik zostanie zmieniony na doctor.py: from models.doctor import Base
from database import engine
from routes import User  # jeśli zmienisz plik: from routes import doctor

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DoctorAPI",
    description="API do zarządzania informacjami o lekarzach oraz sprawdzania ich dostępności",
    version="1.0.0"
)

app.include_router(User.router, prefix="/doktor", tags=["Doktorzy"])
