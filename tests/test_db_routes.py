from fsd_utils.config.commonconfig import CommonConfig


def test_get_fund_by_short_name(flask_test_client, seed_fund_data):
    response = flask_test_client.get("/db/funds/COF?use_short_name=True")
    assert response.status_code == 200
    result = response.json
    assert result["name"] == "Community Ownership Fund"


def test_get_fund_by_id(flask_test_client, seed_fund_data):
    response = flask_test_client.get(f"/db/funds/{CommonConfig.COF_FUND_ID}")
    assert response.status_code == 200
    result = response.json
    assert result["name"] == "Community Ownership Fund"
