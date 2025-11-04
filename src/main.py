import logging
import os
from typing import List
import argparse

from config import DATA_DIR
from database import SessionLocal
from extractors import extract_resources


def main():
    parser = argparse.ArgumentParser(
        description="Extract FHIR resources (Patient, Encounter, Observation, Condition) from JSON files."
    )
    parser.add_argument(
        "--data",
        type=str,
        default="data",
        help="Path to directory containing FHIR JSON files (default: ./data)",
    )

    args = parser.parse_args()

    fhir_files: List[str] = [
        os.path.join(args.data, f)
        for f in os.listdir(DATA_DIR)
        if f.endswith(".json")
    ]
    if not fhir_files:
        logging.warning(f"No FHIR files found in {DATA_DIR}")
        return

    logging.info(f"Found {len(fhir_files)} FHIR files in {DATA_DIR}")

    with SessionLocal() as session:
        for path in fhir_files:
            try:
                extract_resources(path, session)
                session.commit()
            except Exception as e:
                session.rollback()
                logging.exception(f"Error processing {path}: {e}")


if __name__ == "__main__":
    main()
