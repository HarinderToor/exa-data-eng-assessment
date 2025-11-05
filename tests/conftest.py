import json
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base


@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def fhir_bundle_file(tmp_path: Path):
    """
    Creates a temporary FHIR Patient JSON file that simulates a /data file.
    Returns the file path for extractors.
    """
    fake_fhir_data = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "resource": {
                    "resourceType": "Patient",
                    "id": "test-patient-1",
                    "name": [{"given": ["John"], "family": "Doe"}],
                    "gender": "male",
                    "birthDate": "2000-01-11",
                    "address": [{"city": "Bristol", "state": "BRI", "country": "UK"}],
                    "telecom": [{"system": "phone", "value": "12345"}],
                }
            }
        ],
    }
    file_path = tmp_path / "fake_fhir_patient.json"
    file_path.write_text(json.dumps(fake_fhir_data))
    return str(file_path)


@pytest.fixture
def sample_bundle_data():
    """
    Creates a temporary bundle of FHIR Patient data
    """
    return {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "resource": {
                    "resourceType": "Patient",
                    "id": "test-patient-1",
                    "name": [{"given": ["John"], "family": "Doe"}],
                    "gender": "male",
                    "birthDate": "2000-01-11",
                    "address": [{"city": "Bristol", "state": "BRI", "country": "UK"}],
                    "telecom": [{"system": "phone", "value": "12345"}],
                }
            },
            {
                "resource": {
                    "resourceType": "Encounter",
                    "id": "enc-1",
                    "subject": {"reference": "Patient/patient-1"},
                    "class": {"code": "AMB"},
                    "type": [{"text": "Outpatient visit"}],
                    "period": {
                        "start": "2020-01-01T10:00:00+00:00",
                        "end": "2020-01-01T10:30:00+00:00",
                    },
                    "location": [{"location": {"display": "Clinic Room 2"}}],
                }
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "id": "obs-1",
                    "subject": {"reference": "Patient/patient-1"},
                    "code": {"coding": [{"code": "12345"}], "text": "Body temperature"},
                    "valueQuantity": {"value": 37.2, "unit": "C"},
                    "effectiveDateTime": "2020-01-01T10:15:00+00:00",
                }
            },
            {
                "resource": {
                    "resourceType": "Condition",
                    "id": "cond-1",
                    "subject": {"reference": "Patient/patient-1"},
                    "code": {"coding": [{"code": "A01"}], "text": "Typhoid fever"},
                    "onsetDateTime": "2020-01-01T09:00:00+00:00",
                    "verificationStatus": {"coding": [{"code": "confirmed"}]},
                }
            },
        ],
    }
