from src.extractors.patient import extract_patients
from src.models.patient import Patient

def test_extract_patients_with_fake_data(fake_fhir_file, db_session):
    extract_patients(fake_fhir_file, db_session)

    patients = db_session.query(Patient).all()
    assert len(patients) == 1

    patient = patients[0]
    assert patient.first_name == "John"
    assert patient.last_name == "Doe"
    assert patient.gender == "male"
    assert patient.city == "Bristol"