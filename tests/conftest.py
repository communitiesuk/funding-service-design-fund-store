"""
Contains test configuration.
"""
import pytest
import copy
from core.app import create_app
from core.data_operations import fund_data
from core.data_operations import round_data
from tests.test_data import TEST_ROUND_DATA, TEST_FUND_DATA
from flask import Flask


@pytest.fixture()
def app() -> Flask:
    app = create_app()
    # load test data, the test data is copied to prevent test data pollution.
    fund_data.FUNDS_DUMMY_DAO.load_dummy(copy.deepcopy(TEST_FUND_DATA))
    round_data.ROUNDS_DUMMY_DAO.load_dummy(copy.deepcopy(TEST_ROUND_DATA))
    yield app
