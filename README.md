# funding-service-design-fund-store

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Repo for the funding service design fund store.

Built with Flask.

## Prerequisites
- python ^= 3.10

# Getting started

## Installation

Clone the repository.

### Create a Virtual environment

    python3 -m venv .venv

### Enter the virtual environment

...either macOS using bash:

    source .venv/bin/activate

...or if on Windows using Command Prompt:

    .venv\Scripts\activate.bat

### Install dependencies
From the top-level directory enter the command to install pip and the dependencies of the project

    python3 -m pip install --upgrade pip && pip install -r requirements-dev.txt

NOTE: requirements-dev.txt and requirements.txt are updated using [pip-tools pip-compile](https://github.com/jazzband/pip-tools)
To update requirements please manually add the dependencies in the .in files (not the requirements.txt files)
Then run:

    pip-compile requirements.in

    pip-compile requirements-dev.in

## How to use
Enter the virtual environment as described above, then:

    flask run

### Run with Gunicorn

In deployed environments the service is run with gunicorn. You can run the service locally with gunicorn to test

First set the FLASK_ENV environment you wish to test eg:

    export FLASK_ENV=dev

Then run gunicorn using the following command:

    gunicorn wsgi:app -c run/gunicorn/local.py

### Build with Paketo

[Pack](https://buildpacks.io/docs/tools/pack/cli/pack_build/)

[Paketo buildpacks](https://paketo.io/)

```pack build <name your image> --builder paketobuildpacks/builder:base```

Example:

```
[~/work/repos/funding-service-design-fund-store] pack build paketo-demofsd-app --builder paketobuildpacks/builder:base
***
Successfully built image paketo-demofsd-app
```

You can then use that image with docker to run a container

```
docker run -d -p 8080:8080 --env PORT=8080 --env FLASK_ENV=dev paketo-demofsd-app
```

```
docker ps -a
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS                    PORTS                    NAMES
42633142c619   paketo-demofsd-app          "/cnb/process/web"       8 seconds ago    Up 7 seconds              0.0.0.0:8080->8080/tcp   peaceful_knuth
```

# Pipelines

Place brief descriptions of Pipelines here

* Deploy to Gov PaaS - This is a simple pipeline to demonstrate capabilities. Builds, tests and deploys a simple python application to the PaaS for evaluation in Dev and Test Only.
* Tag to Release - This is a simple pipeline that will create the tag required and push an image, built with Paketo, to the GHCR with that tag

# Testing

## Unit

To run all tests in a development environment run:

    pytest

# Extras

This repo comes with a .pre-commit-config.yaml, if you wish to use this do
the following while in your virtual enviroment:

    pip install pre-commit black

    pre-commit install

Once the above is done you will have autoformatting and pep8 compliance built
into your workflow. You will be notified of any pep8 errors during commits.

In deploy.yml, there are three environment variables called users, spawn-rate and run-time. These are used
to override the locust config if the performance tests need to run with different configs for fund store.

# Data
This repo also defines the production data for funds and rounds in JSON format in lieu of a real database. Certain fields can be overridden through environment variables in the following format:

        force_fieldname_roundshortid=value

The fields that can be overridden are: opens, deadline, assessment_deadline. So to override the opening date:

        export force_opens_R2W3=2023-01-01

You can also force all defined rounds to be open by setting the environment variable `FORCE_OPEN`. This has the effect of setting the following values for all rounds:

        `opens = "2022-02-02 12:00:00",
        deadline = "2024-12-31 11:59:00",`
