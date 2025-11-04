# FHIR Data Processor

Processes a folder of FHIR JSON files, and stores them in a local MySQL database.

## Requirements

* [uv](https://docs.astral.sh/uv/) for Python package and environment management.
* [Docker](https://www.docker.com/) and Docker compose.
* Populated `.env` file. A sample one is included.

## Local Setup

Install all the dependencies with:

```console
$ uv sync
```

Build the stack with `docker compose`:

```console
$ docker compose build
$ docker compose up -d
```

## Usage

To process all the files use:

```console
$ uv run src/main.py
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
