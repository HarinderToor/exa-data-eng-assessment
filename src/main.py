import os

from config import DATA_DIR
from database import SessionLocal, init_db
from extractors.patient import extract_patients

init_db()

def main():
    session = SessionLocal()

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            path = os.path.join(DATA_DIR, filename)
            extract_patients(path, session)
    session.close()


if __name__ == "__main__":
    main()
