import json
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.patient import Base


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
def fake_fhir_file(tmp_path: Path):
    """
    Creates a temporary FHIR Patient JSON file that simulates a /data file.
    Returns the file path for extract_patients().
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
                    "address": [
                        {"city": "Bristol", "state": "BRI", "country": "UK"}
                    ],
                    "telecom": [{"system": "phone", "value": "12345"}],
                }
            }
        ],
    }

    file_path = tmp_path / "fake_fhir_patient.json"
    file_path.write_text(json.dumps(fake_fhir_data))

    return str(file_path)
