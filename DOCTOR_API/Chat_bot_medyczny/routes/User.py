from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from models.User import Doctor
from schemas.User import DoctorCreate, DoctorUpdate
from dependencies import get_db
from services.availability import is_doctor_busy

router = APIRouter()

@router.post("/", response_model=DoctorCreate)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = Doctor(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return doctor

@router.put("/{doctor_id}")
def update_doctor(doctor_id: int, doctor: DoctorUpdate, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doktor nie znaleziony")
    for key, value in doctor.dict(exclude_unset=True).items():
        setattr(db_doctor, key, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doktor nie znaleziony")
    db.delete(db_doctor)
    db.commit()
    return {"detail": "Doktor usunięty"}

@router.get("/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doktor nie znaleziony")
    return db_doctor

@router.get("/{email}/dostepnosc")
def check_doctor_availability(email: str, datetime_str: str = Query(..., alias="datetime")):
    try:
        dt = datetime.fromisoformat(datetime_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Niepoprawny format daty. Użyj ISO 8601.")
    available = not is_doctor_busy(email, dt.strftime("%Y-%m-%d"), dt.hour)
    return {"dostepnosc": available}

@router.get("/{email}/najblizszy_termin")
def get_next_available_slot(email: str):
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    for offset in range(24):
        dt = now + timedelta(hours=offset)
        if not is_doctor_busy(email, dt.strftime("%Y-%m-%d"), dt.hour):
            return {"najblizszy_termin": dt.isoformat()}
    return {"detail": "Brak dostępnych terminów w ciągu najbliższych 24 godzin."}
