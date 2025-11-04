import json
import logging
from typing import List, Dict, Any

from sqlalchemy.orm import Session

from models import Condition, Observation, Encounter, Patient

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def _extract_entries(data: Dict[str, Any], resource_type: str):
    for entry in data.get("entry", []):
        resource = entry.get("resource", {})
        if resource.get("resourceType") == resource_type:
            yield resource


def _get_patient_id(resource: Dict[str, Any]) -> str | None:
    ref = resource.get("subject", {}).get("reference", "")
    return ref.split("/")[-1].replace("urn:uuid:", "") if ref else None


def extract_patients_from_bundle(data: Dict[str, Any]) -> List[Patient]:
    patients = []
    for resource in _extract_entries(data, "Patient"):
        try:
            name = resource.get("name", [{}])[0]
            address = resource.get("address", [{}])[0]
            telecom = resource.get("telecom", [{}])

            patient = Patient(
                id=resource.get("id"),
                first_name=name.get("given", [None])[0],
                last_name=name.get("family"),
                gender=resource.get("gender"),
                birth_date=resource.get("birthDate"),
                city=address.get("city"),
                state=address.get("state"),
                country=address.get("country"),
                phone=telecom[0].get("value") if telecom else None,
            )
            patients.append(patient)
        except Exception as e:
            logger.exception(f"Invalid Patient record: {e}")
    return patients


def extract_encounters_from_bundle(data: Dict[str, Any]) -> List[Encounter]:
    encounters = []
    for resource in _extract_entries(data, "Encounter"):
        try:
            encounter = Encounter(
                id=resource.get("id"),
                patient_id=_get_patient_id(resource),
                encounter_class=resource.get("class", {}).get("code"),
                encounter_type=resource.get("type", [{}])[0].get("text"),
                start_time=resource.get("period", {}).get("start"),
                end_time=resource.get("period", {}).get("end"),
                location=(
                    resource.get("location", [{}])[0].get("location", {}).get("display")
                ),
            )
            encounters.append(encounter)
        except Exception as e:
            logger.exception(f"Invalid Encounter record: {e}")
    return encounters


def extract_observations_from_bundle(data: Dict[str, Any]) -> List[Observation]:
    observations = []
    for resource in _extract_entries(data, "Observation"):
        try:
            value = resource.get("valueQuantity", {}) or {}
            observation = Observation(
                id=resource.get("id"),
                patient_id=_get_patient_id(resource),
                code=resource.get("code", {}).get("coding", [{}])[0].get("code"),
                description=resource.get("code", {}).get("text"),
                value=value.get("value"),
                unit=value.get("unit"),
                effective_datetime=resource.get("effectiveDateTime"),
            )
            observations.append(observation)
        except Exception as e:
            logger.exception(f"Invalid Observation record: {e}")
    return observations


def extract_conditions_from_bundle(data: Dict[str, Any]) -> List[Condition]:
    conditions = []
    for resource in _extract_entries(data, "Condition"):
        try:
            code_info = resource.get("code", {}).get("coding", [{}])[0]
            verification = resource.get("verificationStatus", {}).get("coding", [{}])[0]
            onset = resource.get("onsetDateTime") or resource.get(
                "onsetPeriod", {}
            ).get("start")

            condition = Condition(
                id=resource.get("id"),
                patient_id=_get_patient_id(resource),
                code=code_info.get("code"),
                description=resource.get("code", {}).get("text"),
                onset_date=onset,
                verification_status=verification.get("code"),
            )
            conditions.append(condition)
        except Exception as e:
            logger.exception(f"Invalid Condition record: {e}")
    return conditions


def extract_resources(path: str, db: Session):
    with open(path) as f:
        data = json.load(f)

    patients = extract_patients_from_bundle(data)
    encounters = extract_encounters_from_bundle(data)
    observations = extract_observations_from_bundle(data)
    conditions = extract_conditions_from_bundle(data)

    for collection in [patients, encounters, observations, conditions]:
        for obj in collection:
            db.merge(obj)

    db.commit()

    logging.info(
        f"Imported {len(patients)} Patients, {len(encounters)} Encounters, "
        f"{len(observations)} Observations, and {len(conditions)} Conditions from {path}"
    )
