## Research and notes

Main deliverable = Transform FHIR into preferably tabular format to be used in data analysis (querying etc.)

Inspect FHIR files and context -> Bundles
FHIR is a nested JSON format, so can be parsed with Pydantic or similar  
Large files so need to check the performance of Pydantic vs other options and raw JSON parsing

### Early prototype ideas

Files have lots of information nested - the most relevant `resourceTypes` for analytics were chosen (others can be added later)
- Patient
- Encounter
- Condition
- Observation

To keep the proof of concept simple:

**Extract**: Use existing FHIR resources Python library if possible, based on Pydantic!  
**Transform**: Design sqlalchemy models for each resource  
**Load**: Flatten each resource and load into MySQL

Potentially add an export layer from mysql + pandas to parquet format files.

### Areas to improve

- Encounters, Observations and Conditions aren't using built in lib due to some early parsing problems
- Optimise extractors so they aren't parsing the files more than they have to
- Update models to handle the various data types properly (e.g. DateTimes)
- Add Threading to file processing (e.g. give workers a unique session to prevent db errors)
- Custom exceptions / logging
- Improve typing - add type checker with pre commit or similar
- More tests



