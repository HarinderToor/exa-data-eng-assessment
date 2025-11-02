import pathlib
from fhir.resources.R4B.bundle import Bundle
from pydantic_core import from_json


def main():
    filename = pathlib.Path(
        "data/Harland508_Hintz995_a57f2290-27ed-6117-2989-f42ef6d291ab.json"
    )
    with open(filename, "rb") as f:
        data = from_json(f.read())

    data_bundle = Bundle.parse_obj(data)
    return print([entry.resource for entry in data_bundle.entry])


if __name__ == "__main__":
    main()
