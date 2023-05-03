"""
Contains test configuration.
"""
import copy

import pytest
from app import create_app
from core.data_operations import fund_data
from core.data_operations import round_data
from flask import Flask
from sqlalchemy import text
from tests.test_data import TEST_FUND_DATA
from tests.test_data import TEST_ROUND_DATA

pytest_plugins = ["fsd_test_utils.fixtures.db_fixtures"]


@pytest.fixture(scope="function")
def seed_fund_data(
    request, app, clear_test_data, enable_preserve_test_data, _db
):
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
