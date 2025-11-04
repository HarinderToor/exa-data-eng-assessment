from database import Base
from sqlalchemy import Column, String, Date, ForeignKey, Index
from sqlalchemy import Float, Text
from sqlalchemy.orm import relationship


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

    encounters = relationship("Encounter", back_populates="patient")
    conditions = relationship("Condition", back_populates="patient")
    observations = relationship("Observation", back_populates="patient")


class Encounter(Base):
    __tablename__ = "encounters"
    id = Column(String(64), primary_key=True)
    patient_id = Column(String(64), ForeignKey("patients.id"))
    encounter_class = Column(String(50))
    encounter_type = Column(String(100))
    start_time = Column(String(30))
    end_time = Column(String(30))
    location = Column(String(100))

    patient = relationship("Patient", back_populates="encounters")

    __table_args__ = (Index("ix_encounters_patient_id", "patient_id"),)


class Condition(Base):
    __tablename__ = "conditions"
    id = Column(String(64), primary_key=True)
    patient_id = Column(String(64), ForeignKey("patients.id"))
    code = Column(String(100))
    description = Column(Text)
    onset_date = Column(String(30))
    verification_status = Column(String(50))

    patient = relationship("Patient", back_populates="conditions")

    __table_args__ = (Index("ix_conditions_patient_id", "patient_id"),)


class Observation(Base):
    __tablename__ = "observations"
    id = Column(String(64), primary_key=True)
    patient_id = Column(String(64), ForeignKey("patients.id"))
    code = Column(String(100))
    description = Column(Text)
    value = Column(Float)
    unit = Column(String(20))
    effective_datetime = Column(String(30))

    patient = relationship("Patient", back_populates="observations")

    __table_args__ = (Index("ix_observations_patient_id", "patient_id"),)
