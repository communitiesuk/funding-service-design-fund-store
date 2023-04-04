"""
A file containing all tests related to the fund endpoint.
"""
import asserts
from flask import Flask
from flask import request
from tests.test_data import TEST_FUND_ONE, TEST_ROUND_DATA
from tests.test_data import TEST_ROUND_ONE
from tests.test_data import TEST_ROUNDS_IN_FUND_ONE


def test_all_funds_endpoint(client: Flask, load_test_data):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response length consistent
    with all inital data (including test data).
    """
    host_url = request.host_url
    url = host_url + "funds"
    api_response_json = client.get(url).json

    assert 3 == len(api_response_json)
    assert "COF" in [f["short_name"] for f in api_response_json]


def test_single_fund_endpoint(client: Flask, load_test_data):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/fb986cdc-8e02-477a-a7e0-41cf19dd7675"
    api_response_json = client.get(url).json

    expected_data = TEST_FUND_ONE

    asserts.assert_equal(
        api_response_json,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_all_rounds_in_single_fund_endpoint(client: Flask, load_test_data):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/fb986cdc-8e02-477a-a7e0-41cf19dd7675/rounds"
    api_response_json = client.get(url).json

    expected_data = TEST_ROUNDS_IN_FUND_ONE

    asserts.assert_equal(
        api_response_json,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_single_round_in_single_fund_endpoint(client: Flask, load_test_data):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = (
        host_url
        + "funds/fb986cdc-8e02-477a-a7e0-41cf19dd7675/"
        "rounds/3b1ae9e8-eda4-4910-a5dd-fc144f9a8ba1"
    )
    api_response_json = client.get(url).json

    expected_data = TEST_ROUND_ONE

    asserts.assert_equal(
        api_response_json,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_get_fund_by_short_name(client, load_test_data):
    host_url = request.host_url
    expected_data = TEST_FUND_ONE

    url = (
        host_url
        + "funds/fb986cdc-8e02-477a-a7e0-41cf19dd7675?use_short_name=false"
    )
    api_response_json = client.get(url).json

    assert api_response_json == expected_data

    url = (
        host_url
        + "funds/fb986cdc-8e02-477a-a7e0-41cf19dd7675?use_short_name=true"
    )
    response = client.get(url)

    assert 404 == response.status_code

    url = host_url + "funds/FUND1?use_short_name=true"
    api_response_json = client.get(url).json

    assert api_response_json == expected_data


def test_get_round_by_short_name(client, load_test_data):
    host_url = request.host_url
    expected_data = TEST_ROUND_DATA

    url = (
        host_url
        + "funds/FUND1/rounds/R2W3?use_short_name=true"
    )
    api_response_json = client.get(url).json

    assert api_response_json.get("short_name") == expected_data[0].get("short_name")
    assert api_response_json.get("fund_id") == expected_data[0].get("fund_id")
    assert api_response_json.get("id") == expected_data[0].get("id")
    assert api_response_json.get("title") == expected_data[0].get("title")

    url = (
        host_url
        + "funds/non-existant-fund/rounds/R2W3?use_short_name=true"
    )
    response = client.get(url)

    assert 404 == response.status_code
