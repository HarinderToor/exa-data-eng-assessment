from src.extractors import extract_resources
from src.models import Patient, Encounter, Observation, Condition


def test_extract_patients_with_fake_data(fake_fhir_file, db_session):
    extract_resources(fake_fhir_file, db_session)

    patients = db_session.query(Patient).all()
    assert len(patients) == 1
    patient = patients[0]
    assert patient.first_name == "John"
    assert patient.last_name == "Doe"
    assert patient.gender == "male"
    assert patient.city == "Bristol"


def test_extract_encounter(fake_fhir_file, db_session):
    extract_resources(fake_fhir_file, db_session)

    encounters = db_session.query(Encounter).all()
    assert len(encounters) == 1
    encounters = encounters[0]
    assert encounters.patient_id == "patient-1"
    assert encounters.encounter_class == "AMB"
    assert "Outpatient" in encounters.encounter_type
    assert encounters.location == "Clinic Room 2"


def test_extract_observation(fake_fhir_file, db_session):
    extract_resources(fake_fhir_file, db_session)

    observations = db_session.query(Observation).one()
    assert observations.code == "12345"
    assert "temperature" in observations.description.lower()
    assert observations.value == 37.2
    assert observations.unit == "C"


def test_extract_condition(fake_fhir_file, db_session):
    extract_resources(fake_fhir_file, db_session)
    conditions = db_session.query(Condition).one()
    assert conditions.code == "A01"
    assert "Typhoid" in conditions.description
    assert conditions.verification_status == "confirmed"
