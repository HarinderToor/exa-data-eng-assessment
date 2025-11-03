from src.database import Base
from sqlalchemy import Column, String, Date


class Patient(Base):
    __tablename__ = "patients"
    id = Column(String(64), primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(String(10))
    birth_date = Column(Date)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    phone = Column(String(50))

