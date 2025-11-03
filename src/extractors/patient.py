import json

from fhir.resources.patient import Patient as FhirPatient
from models.patient import Patient
from sqlalchemy.orm import Session


def extract_patients(path: str, db: Session):
    with open(path) as f:
        data = json.load(f)

    count = 0
    for entry in data.get("entry", []):
        resource = entry.get("resource", {})
        if resource.get("resourceType") == "Patient":
            try:
                fhir_patient = FhirPatient(**resource)
                patient = Patient(
                    id=fhir_patient.id,
                    first_name=fhir_patient.name[0].given[0] if fhir_patient.name else None,
                    last_name=fhir_patient.name[0].family if fhir_patient.name else None,
                    gender=fhir_patient.gender,
                    birth_date=fhir_patient.birthDate,
                    city=fhir_patient.address[0].city if fhir_patient.address else None,
                    state=fhir_patient.address[0].state if fhir_patient.address else None,
                    country=fhir_patient.address[0].country if fhir_patient.address else None,
                    phone=fhir_patient.telecom[0].value if fhir_patient.telecom else None,
                )
                db.merge(patient)
                count += 1
            except Exception as e:
                print(f"Invalid Patient record: {e}")

    db.commit()
    print(f"Loaded {count} valid Patient records from {path}")
