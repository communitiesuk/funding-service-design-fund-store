from core.rounds import get_round, get_rounds_for_fund
from fsd_utils.config.commonconfig import CommonConfig
from datetime import datetime, timedelta
from core.data_operations.round_data import override_fields_from_env

class MockRequest_cy:

    args = {
        "language": "cy"
    }


class MockRequest_en:

    args = {
        "language": "en"
    }

def test_get_cof_r2w3(mocker, monkeypatch):

    monkeypatch.setattr(
        "core.rounds.request",
        MockRequest_en(),
    )
    result = get_round(CommonConfig.COF_FUND_ID, CommonConfig.COF_ROUND_2_W3_ID)
    assert "Round 2 Window 3" == result[0]["title"]
    assert "Monday to Friday" == result[0]["support_availability"]["days"]


def test_get_cof_r2w3_welsh(mocker, monkeypatch):

    monkeypatch.setattr(
        "core.rounds.request",
        MockRequest_cy(),
    )
    result = get_round(CommonConfig.COF_FUND_ID, CommonConfig.COF_ROUND_2_W3_ID)
    assert "Cylch 2 Window 3" == result[0]["title"]
    assert "Monday to Friday" == result[0]["support_availability"]["days"]

def test_get_cof_r2w2(mocker, monkeypatch):

    monkeypatch.setattr(
        "core.rounds.request",
        MockRequest_en(),
    )
    result = get_round(CommonConfig.COF_FUND_ID, CommonConfig.COF_ROUND_2_ID)
    assert "Round 2 Window 2" == result[0]["title"]
    assert "Monday to Friday" == result[0]["support_availability"]["days"]


def test_get_cof(mocker, monkeypatch):

    monkeypatch.setattr(
        "core.rounds.request",
        MockRequest_en(),
    )
    result = get_rounds_for_fund(CommonConfig.COF_FUND_ID)
    assert 2 == len(result[0])
    assert "Round 2 Window 3" == result[0][1]["title"]
    assert "Round 2 Window 2" == result[0][0]["title"]

def test_override_fields(monkeypatch):
    overridable_fields = ["opens"]
    round_data = {
        "short_name": "a1b2",
        "opens": "abc",
        "dont_override": "original"
    }
    monkeypatch.setenv("force_opens_a1b2", "changed")
    result = override_fields_from_env(round_data, overridable_fields)
    assert "changed" == result["opens"], "opens field not changed"
    assert "original" == result["dont_override"], "other field changed"
