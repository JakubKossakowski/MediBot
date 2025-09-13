from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Doctor(Base):
    __tablename__ = "doktorzy"
    id = Column(Integer, primary_key=True, index=True)
    imie = Column(String(50), nullable=False)
    nazwisko = Column(String(50), nullable=False)
    klasyfikacja = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
