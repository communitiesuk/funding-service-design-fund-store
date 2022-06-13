"""
A file containing all tests related to the fund endpoint.
"""
from ast import literal_eval

import asserts
from flask import Flask
from flask import request
from tests.test_data import BREKKY_ROUND
from tests.test_data import HARRY_S_BREAKFAST_FUND
from tests.test_data import ROUNDS_IN_HARRY_S_BREAKFAST_FUND
from tests.test_data import TEST_RESPONSE_FUND_DATA


def test_all_funds_endpoint(client: Flask):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response length consistent
    with all inital data (including test data).
    """
    host_url = request.host_url
    url = host_url + "funds"
    api_response = client.get(url)

    raw_data = api_response.data
    number_of_funds_in_store_response = len(
        literal_eval(raw_data.decode("utf-8"))
    )
    number_of_pre_configured_funds_in_store = 1
    expected_number_of_funds = (
        len(TEST_RESPONSE_FUND_DATA) + number_of_pre_configured_funds_in_store
    )
    asserts.assert_equal(
        number_of_funds_in_store_response,
        expected_number_of_funds,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_all_funds_endpoint_includes_fund_test_data(client: Flask):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response including the
    test data.
    """
    host_url = request.host_url
    url = host_url + "funds"
    api_response = client.get(url)

    raw_data = api_response.data
    response_data = literal_eval(raw_data.decode("utf-8"))[
        -len(TEST_RESPONSE_FUND_DATA) :
    ]

    expected_data = TEST_RESPONSE_FUND_DATA
    asserts.assert_equal(
        response_data,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_single_fund_endpoint(client: Flask):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/harry-s-breakfast-fund"
    api_response = client.get(url)

    raw_data = api_response.data
    response_data = literal_eval(raw_data.decode("utf-8"))

    expected_data = HARRY_S_BREAKFAST_FUND

    asserts.assert_equal(
        response_data,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_all_rounds_in_single_fund_endpoint(client: Flask):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/harry-s-breakfast-fund/rounds"
    api_response = client.get(url)

    raw_data = api_response.data
    response_data = literal_eval(raw_data.decode("utf-8"))

    expected_data = ROUNDS_IN_HARRY_S_BREAKFAST_FUND

    asserts.assert_equal(
        response_data,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_single_round_in_single_fund_endpoint(client: Flask):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/harry-s-breakfast-fund/rounds/brekky"
    api_response = client.get(url)

    raw_data = api_response.data
    response_data = literal_eval(raw_data.decode("utf-8"))

    expected_data = BREKKY_ROUND

    asserts.assert_equal(
        response_data,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )
