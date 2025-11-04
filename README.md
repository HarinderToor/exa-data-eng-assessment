# FHIR Data Processor

Processes a folder of FHIR JSON files, and stores them in a local MySQL database.

## Requirements

* [uv](https://docs.astral.sh/uv/) for Python package and environment management.
* [Docker](https://www.docker.com/) and Docker compose.
* Populated `.env` file. A sample one is included.

## Local Docker & Development Setup

Install all the dependencies with:

```console
$ uv sync
```

Build the stack with `docker compose`:

```console
$ docker compose build
$ docker compose up -d
```
This will process all files within the data folder and upload them to the database.

## Usage examples

To separate the processing, you can use:

```console
$ docker compose up -d mysql
$ docker compose run --rm fhir-etl
```

Or for a local setup update the env host settings and then:

```console
$ uv run src/main.py
$ uv run src/main.py --data /path/to/fhir/files
```

To run the tests:

```console
$ uv run pytest
```




Code quality is managed by `ruff`:
```console
$ ruff check
$ ruff check --fix
$ ruff format
```



## Examples


```console
docker exec -it mysql mysql -uroot -proot fhir_db

SELECT p.id                 AS patient_id,
       p.first_name,
       p.last_name,
       p.gender,
       p.birth_date,
       p.city,
       p.state,
       p.country,
       p.phone,
       e.id                 AS encounter_id,
       e.encounter_class,
       e.encounter_type,
       e.start_time         AS encounter_start,
       e.end_time           AS encounter_end,
       e.location           AS encounter_location,
       o.id                 AS observation_id,
       o.code               AS observation_code,
       o.value              AS observation_value,
       o.unit               AS observation_unit,
       o.effective_datetime AS observation_time,
       c.id                 AS condition_id,
       c.code               AS condition_code,
       c.description        AS condition_description,
       c.onset_date         AS condition_onset
FROM   patients p
       LEFT JOIN encounters e
              ON p.id = e.patient_id
       LEFT JOIN observations o
              ON p.id = o.patient_id
       LEFT JOIN conditions c
              ON p.id = c.patient_id
LIMIT  1; 

*************************** 1. row ***************************
           patient_id: 09e292d4-f186-331c-ed95-c503acabc54e
           first_name: Gus973
            last_name: Windler79
               gender: male
           birth_date: 1913-02-23
                 city: Gardner
                state: MA
              country: US
                phone: 555-425-8155
         encounter_id: 143a7095-23bd-1455-3747-1ecd072fa08c
      encounter_class: AMB
       encounter_type: Well child visit (procedure)
      encounter_start: 1930-04-13T14:15:01+01:00
        encounter_end: 1930-04-13T14:30:01+01:00
   encounter_location: PCP34313
       observation_id: 00410180-b86f-b1cc-5883-8f7386fe4314
     observation_code: 72514-3
    observation_value: 1
     observation_unit: {score}
     observation_time: 1932-04-24T14:15:01+01:00
         condition_id: 058ebb60-c297-a850-583b-5cfd64ac9806
       condition_code: 444814009
condition_description: Viral sinusitis (disorder)
      condition_onset: 1931-08-07T10:15:01+01:00
1 row in set (0.00 sec)

```
