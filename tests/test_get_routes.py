"""
Contains the tests regarding get requests to the Fund Store API
"""
import json


def expected_content_from_get(
    endpoint: str, expected_content: str, test_client
):

    response = test_client.get(endpoint, follow_redirects=True)
    assert json.loads(response.data) == expected_content


def test_funds_endpoint_get(flask_test_client):

    expected_content = [
        {
            "name": "Harry's breakfast fund",
            "identifer": "harry-s-breakfast-fund",
            "eligibility_criteria": {"maximium_project_cost": 10},
            "deadline": "2022-12-25T00:00:00",
            "opens": "2022-11-25T00:00:00",
        },
        {
            "name": "Ram's Get Fit Feb fund",
            "identifer": "ram-s-get-fit-feb-fund",
            "eligibility_criteria": {"maximium_project_cost": 100},
            "deadline": "2022-12-31T00:00:00",
            "opens": "2022-01-01T00:00:00",
        },
    ]

    expected_content_from_get("/funds", expected_content, flask_test_client)
