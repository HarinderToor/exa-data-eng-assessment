from src.extractors import (
    extract_patients_from_bundle,
    extract_encounters_from_bundle,
    extract_observations_from_bundle,
    extract_conditions_from_bundle,
    _extract_entries,
)


class TestExtractEntries:
    def test_extract_patient_entries(self, sample_bundle_data):
        patients = list(_extract_entries(sample_bundle_data, "Patient"))
        assert len(patients) == 1
        assert patients[0]["id"] == "test-patient-1"

    def test_extract_encounter_entries(self, sample_bundle_data):
        encounters = list(_extract_entries(sample_bundle_data, "Encounter"))
        assert len(encounters) == 1
        assert encounters[0]["id"] == "enc-1"

    def test_extract_nonexistent_type(self, sample_bundle_data):
        results = list(_extract_entries(sample_bundle_data, "Medication"))
        assert len(results) == 0

    def test_empty_bundle(self):
        empty_bundle = {"resourceType": "Bundle", "entry": []}
        results = list(_extract_entries(empty_bundle, "Patient"))
        assert len(results) == 0


class TestExtractPatients:
    def test_extract_single_patient(self, sample_bundle_data):
        patients = extract_patients_from_bundle(sample_bundle_data)
        assert len(patients) == 1
        patient = patients[0]
        assert patient.id == "test-patient-1"
        assert patient.first_name == "John"
        assert patient.last_name == "Doe"
        assert patient.gender == "male"
        assert patient.city == "Bristol"
        assert patient.state == "BRI"
        assert patient.phone == "12345"

    def test_extract_patient_minimal_data(self):
        minimal_bundle = {
            "entry": [
                {
                    "resource": {
                        "resourceType": "Patient",
                        "id": "minimal-patient",
                        "name": [{}],
                        "address": [{}],
                    }
                }
            ]
        }
        patients = extract_patients_from_bundle(minimal_bundle)
        assert len(patients) == 1
        assert patients[0].id == "minimal-patient"
        assert patients[0].first_name is None
        assert patients[0].last_name is None

    def test_extract_multiple_patients(self):
        multi_bundle = {
            "entry": [
                {
                    "resource": {
                        "resourceType": "Patient",
                        "id": "patient-1",
                        "name": [{"given": ["Alice"], "family": "Adams"}],
                        "address": [{}],
                    }
                },
                {
                    "resource": {
                        "resourceType": "Patient",
                        "id": "patient-2",
                        "name": [{"given": ["Bob"], "family": "Brown"}],
                        "address": [{}],
                    }
                },
            ]
        }
        patients = extract_patients_from_bundle(multi_bundle)
        assert len(patients) == 2
        assert patients[0].first_name == "Alice"
        assert patients[1].first_name == "Bob"


class TestExtractEncounters:
    def test_extract_single_encounter(self, sample_bundle_data):
        encounters = extract_encounters_from_bundle(sample_bundle_data)
        assert len(encounters) == 1
        encounter = encounters[0]
        assert encounter.id == "enc-1"
        assert encounter.patient_id == "patient-1"
        assert encounter.encounter_class == "AMB"
        assert encounter.encounter_type == "Outpatient visit"
        assert encounter.location == "Clinic Room 2"

    def test_extract_encounter_minimal_data(self):
        minimal_bundle = {
            "entry": [
                {
                    "resource": {
                        "resourceType": "Encounter",
                        "id": "enc-minimal",
                        "subject": {"reference": "Patient/test-patient"},
                        "class": {},
                        "type": [{}],
                        "period": {},
                        "location": [{}],
                    }
                }
            ]
        }
        encounters = extract_encounters_from_bundle(minimal_bundle)
        assert len(encounters) == 1
        assert encounters[0].id == "enc-minimal"
        assert encounters[0].patient_id == "test-patient"


class TestExtractObservations:
    def test_extract_single_observation(self, sample_bundle_data):
        observations = extract_observations_from_bundle(sample_bundle_data)
        assert len(observations) == 1
        obs = observations[0]
        assert obs.id == "obs-1"
        assert obs.patient_id == "patient-1"
        assert obs.code == "12345"
        assert obs.description == "Body temperature"
        assert obs.value == 37.2
        assert obs.unit == "C"

    def test_extract_observation_without_value_quantity(self):
        bundle = {
            "entry": [
                {
                    "resource": {
                        "resourceType": "Observation",
                        "id": "obs-no-value",
                        "subject": {"reference": "Patient/test-patient"},
                        "code": {"coding": [{"code": "test-code"}], "text": "Test"},
                        "effectiveDateTime": "2023-01-01",
                    }
                }
            ]
        }
        observations = extract_observations_from_bundle(bundle)
        assert len(observations) == 1
        assert observations[0].value is None
        assert observations[0].unit is None


class TestExtractConditions:
    def test_extract_single_condition(self, sample_bundle_data):
        conditions = extract_conditions_from_bundle(sample_bundle_data)
        assert len(conditions) == 1
        cond = conditions[0]
        assert cond.id == "cond-1"
        assert cond.patient_id == "patient-1"
        assert cond.code == "A01"
        assert cond.description == "Typhoid fever"
        assert cond.verification_status == "confirmed"

    def test_extract_condition_with_onset_period(self):
        bundle = {
            "entry": [
                {
                    "resource": {
                        "resourceType": "Condition",
                        "id": "cond-period",
                        "subject": {"reference": "Patient/test-patient"},
                        "code": {"coding": [{"code": "M15"}], "text": "Arthritis"},
                        "onsetPeriod": {"start": "2019-06-01"},
                        "verificationStatus": {"coding": [{"code": "confirmed"}]},
                    }
                }
            ]
        }
        conditions = extract_conditions_from_bundle(bundle)
        assert len(conditions) == 1
        assert conditions[0].onset_date == "2019-06-01"

    def test_extract_condition_minimal_data(self):
        minimal_bundle = {
            "entry": [
                {
                    "resource": {
                        "resourceType": "Condition",
                        "id": "cond-minimal",
                        "subject": {"reference": "Patient/test-patient"},
                        "code": {"coding": [{}], "text": "Unknown"},
                        "verificationStatus": {"coding": [{}]},
                    }
                }
            ]
        }
        conditions = extract_conditions_from_bundle(minimal_bundle)
        assert len(conditions) == 1
        assert conditions[0].id == "cond-minimal"
