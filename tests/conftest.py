"""
Contains test configuration.
"""
import copy
from uuid import uuid4

import pytest
from app import create_app
from core.data_operations import fund_data
from core.data_operations import round_data
from db.queries import insert_fund_data
from flask import Flask
from sqlalchemy import text
from tests.test_data import TEST_FUND_DATA
from tests.test_data import TEST_ROUND_DATA

pytest_plugins = ["fsd_test_utils.fixtures.db_fixtures"]


@pytest.fixture(scope="function")
def seed_fund_data(request, app, clear_test_data, enable_preserve_test_data, _db):
    with _db.engine.begin() as conn:
        with open("db/cof_sql/fund.sql") as file:
            conn.execute(text(file.read()))
        with open("db/cof_sql/rounds.sql") as file:
            conn.execute(text(file.read()))
        with open("db/cof_sql/sections_sqla.sql") as file:
            conn.execute(text(file.read()))
        with open("db/cof_sql/assessment_fields.sql") as file:
            conn.execute(text(file.read()))
        with open("db/cof_sql/section_fields.sql") as file:
            conn.execute(text(file.read()))
        with open("db/cof_sql/form_name.sql") as file:
            conn.execute(text(file.read()))
        # with open("db/cof_sql/translations.sql") as file:
        #     conn.execute(text(file.read()))


@pytest.fixture(scope="function")
def seed_only_fund_and_round_data(
    request, app, clear_test_data, enable_preserve_test_data, _db
):
    with _db.engine.begin() as conn:
        with open("db/cof_sql/fund.sql") as file:
            conn.execute(text(file.read()))
        with open("db/cof_sql/rounds.sql") as file:
            conn.execute(text(file.read()))


@pytest.fixture(scope="function")
def seed_dynamic_data(request, app, clear_test_data, enable_preserve_test_data, _db):
    marker = request.node.get_closest_marker("seed_config")
    if marker is None:
        seed_config = {
            "funds": [
                {
                    "rounds": [
                        {
                            "is_open": True,
                            "is_past_deadline": False,
                            "is_not_yet_open": False,
                        },
                        {
                            "is_open": False,
                            "is_past_deadline": True,
                            "is_not_yet_open": False,
                        },
                        {
                            "is_open": False,
                            "is_past_deadline": False,
                            "is_not_yet_open": True,
                        },
                    ]
                }
            ]
        }
    else:
        seed_config = marker.args[0]
    inserted_data = {"funds": []}
    for fund in seed_config["funds"]:
        fund_id = str(uuid4())
        short_suffix = fund_id[0:4]
        fund_config = {
            "id": fund_id,
            "name": f"Unit Test Fund {short_suffix}",
            "title": f"Unit test fund title {short_suffix}",
            "short_name": short_suffix,
            "description": "testing description",
        }
        insert_fund_data(fund_config)
        inserted_data["funds"].append(
            {"rounds": [], "id": fund_id, "short_name": short_suffix}
        )

    yield inserted_data


@pytest.fixture(scope="session")
def app() -> Flask:
    app = create_app()
    yield app


@pytest.fixture(scope="function")
def flask_test_client():

    with create_app().app_context() as app_context:
        with app_context.app.test_client() as test_client:
            yield test_client


@pytest.fixture(scope="session")
def load_test_data():
    fund_data.FUNDS_DAO.load_data(copy.deepcopy(TEST_FUND_DATA))
    round_data.ROUNDS_DAO.load_data(copy.deepcopy(TEST_ROUND_DATA))
