# funding-service-design-fund-store

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is the fund store for funding service design Access Funding. This service provides an API and associated model implementation for fund and round configuration data.
<!--
[Developer setup guide](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-setup.md) -->

This service depends on:
- A postgres database
- No other microservices

# Dev Container
This repo contains a vs code dev container specification in [.devcontainer](./.devcontainer/python-container/devcontainer.json). When used through VS code it provides:
- All the python dependencies for fund-store pre-installed
- The postgres cmd client `psql`
- A standalone postgres instance, accessible from the dev container at `fund-store-db:5432`

## Local Setup
- Clone the repo into eg. funding-service-design-fund-store
- Open the folder funding-service-design-fund-store
- Use the command pallette (cmd + shift + P) and select 'Dev Containers: Reopen folder in container' (VS Code may prompt you for this on its own - it does the same thing)
- You are now in the dev container with all dependencies installed, and useful VS code extensions.
- There may be a delay in all the extensions (eg. unit testing) being available while it installs them in the container. This only happens the first time.
- You can now start the app with `flask run` or run unit tests using the vs code extension or run `pytest` on the command line.

## Files involved
- [.devcontainer](./.devcontainer/python-container/devcontainer.json) Contains the vs code configuration for the container, such as which docker compose files to reference, and what extensions to install in the container.
- [docker-compose.yml](./docker-compose.yml) Details of the containers that are needed to develop this app. For fund-store it uses [Dockerfile](./Dockerfile) and a `posgtres` image.
- [Dockerfile](./Dockerfile) Details of the image to use for the dev container, under the stage `fund-store-dev`. Built on the fsd base image, and adds this repo's requirements.txt, and the psql command line client.
- [Optional] [compose.override.yml](./compose.override.yml) Allows overriding of properties such as exposed ports, or adding environment variables to the containers listed in `docker-compose.yml`. eg. If you want the postgres instance to be accessible from your local machine you could add the following to this file:
    ```
    services:
    fund-store-db:
        ports:
        - 5433:5432
    ```
    This will expose that postgres instance on port `5433` so you could connect a local `psql` client to it at `localhost:5432`

    If using this, add an additional item to the `dockerComposeFile` array in [devcontainer.json](./.devcontainer/python-container/devcontainer.json) pointing to this overrides file.


# Data
## Local DB Setup
~~General instructions for local db development are available here: [Local database development](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-db-development.md)~~

The `docker-compose` file invokes a `postgres` container which this dev container will use for accessing the DB, either through unit tests or when running with `flask run`.

You can also access it directly:

`psql --host fund-store-db --port 5432 --user postgres`

with the password configured as `POSTGRES_PASSWORD` in [docker-compose.yml](./docker-compose.yml)

## DB Helper Scripts
This repository uses `invoke` to provide scripts for dropping and recreating the local database in [tasks.py](./tasks.py)

### Running Locally
These scripts can be run on the command line from the dev container, eg. `inv recreate-local-db`. PSQL is installed as part of the dev container so does not need to be on your machine.

### Available scripts
The following commands are the same locally or in container

### Recreate DB instance

        inv recreate-local-db

this drops (if it exists) and recreates the DB

### Truncate data

        inv truncate-data


## Seeding Fund Data
To seed fund & round data to db for all funds and rounds, use the fund/round loaders scripts.

If running against a local postgresql instance:
```bash
    python -m scripts.load_all_fund_rounds
```

If running with the docker compose setup:

```bash
    docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.load_all_fund_rounds
```

Further details on the fund/round loader scripts, and how to load data for a specific fund or round can be found [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/40337455/Adding+or+updating+fund+and+round+data)

## Amending round dates
This script allows you to open/close rounds using their dates to test different functionality as needed. You can also use the keywords 'PAST', 'FUTURE' and 'UNCHANGED' to save typing dates.

```bash
docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates -q update-round-dates --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --application_deadline "2023-03-30 12:00:00"

docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates -q update-round-dates -r COF_R3W3 -o "2022-10-04 12:00:00" -d "2022-12-14 11:59:00" -ad "2023-03-30 12:00:00" -as NONE

docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates -q update-round-dates -r COF_R3W3 -o PAST -d FUTURE
```
For an interactive prompt where you can supply (or leave unchanged) all dates:
```bash
docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates update-round-dates
```
To reset the dates for a round to those in the fund loader config:
```bash
docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates -q reset-round-dates -r COF_R4W1
```
And with an interactive prompt:
```bash
docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates reset-round-dates
```

# Testing
[Testing in Python repos](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-db-development.md)


# IDE Setup
[Python IDE Setup](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-ide-setup.md)


# Builds and Deploys
Details on how our pipelines work and the release process is available [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/73695505/How+do+we+deploy+our+code+to+prod)
## Paketo
Paketo is used to build the docker image which gets deployed to our test and production environments. Details available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-paketo.md)
## Copilot
Copilot is used for infrastructure deployment. Instructions are available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-copilot.md), with the following values for the fund store:
- service-name: fsd-fund-store
- image-name: funding-service-design-fund-store
