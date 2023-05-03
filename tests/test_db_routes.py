from fsd_utils.config.commonconfig import CommonConfig


def test_get_fund_by_short_name(flask_test_client, seed_fund_data):
    response = flask_test_client.get("/db/funds/COF?use_short_name=True")
    assert response.status_code == 200
    result = response.json
    assert result["name"] == "Community Ownership Fund"

    response = flask_test_client.get("/db/funds/bad?use_short_name=True")
    assert response.status_code == 404


def test_get_fund_by_id(flask_test_client, seed_fund_data):
    response = flask_test_client.get(f"/db/funds/{CommonConfig.COF_FUND_ID}")
    assert response.status_code == 200
    result = response.json
    assert result["name"] == "Community Ownership Fund"


def test_get_round_by_short_name(flask_test_client, seed_fund_data):
    response = flask_test_client.get(
        "/db/funds/cof/rounds/r2w2?use_short_name=True"
    )
    assert response.status_code == 200
    result = response.json
    assert result["title"] == "Round 2 Window 2"


def test_get_round_by_id(flask_test_client, seed_fund_data):
    response = flask_test_client.get(
        f"/db/funds/{CommonConfig.COF_FUND_ID}/"
        f"rounds/{CommonConfig.COF_ROUND_2_ID}"
    )
    assert response.status_code == 200
    result = response.json
    assert result["title"] == "Round 2 Window 2"


def test_get_rounds_for_fund_by_short_name(flask_test_client, seed_fund_data):
    response = flask_test_client.get(
        "/db/funds/cof/rounds?use_short_name=True"
    )
    assert response.status_code == 200
    result = response.json
    assert len(result) == 2
    assert result[0]["title"] == "Round 2 Window 2"


def test_get_rounds_for_fund_by_id(flask_test_client, seed_fund_data):
    response = flask_test_client.get(
        f"/db/funds/{CommonConfig.COF_FUND_ID}/rounds"
    )
    assert response.status_code == 200
    result = response.json
    assert len(result) == 2
    assert result[0]["title"] == "Round 2 Window 2"


def test_get_all_funds(flask_test_client, seed_fund_data):
    response = flask_test_client.get("/db/funds")
    assert response.status_code == 200
    result = response.json
    assert result[0]["name"] == "Community Ownership Fund"


def test_get_all_funds_no_data(flask_test_client):
    response = flask_test_client.get("/db/funds")
    assert response.status_code == 404
