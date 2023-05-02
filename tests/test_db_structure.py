from db.queries import get_fund_by_id
from db.queries import get_fund_by_short_name
from db.queries import get_round_by_id
from db.queries import get_round_by_short_name
from fsd_utils.config.commonconfig import CommonConfig


# @pytest.mark.preserve_test_data(True)
def test_db_created(seed_fund_data):
    pass


def test_get_fund_by_id(seed_fund_data):
    f = get_fund_by_id(CommonConfig.COF_FUND_ID)
    assert f.name == "Community Ownership Fund"
    assert f.short_name == "COF"


def test_get_fund_by_short_name(seed_fund_data):
    f = get_fund_by_short_name("COF")
    assert f.name == "Community Ownership Fund"
    assert f.short_name == "COF"


def test_get_round_by_id(seed_fund_data):
    r = get_round_by_id(CommonConfig.COF_ROUND_2_ID)
    assert r.title == "Round 2 Window 2"
    assert r.short_name == "R2W2"
    assert str(r.id) == CommonConfig.COF_ROUND_2_ID


def test_get_round_by_short_name(seed_fund_data):
    r = get_round_by_short_name("R2W2")
    assert r.title == "Round 2 Window 2"
    assert r.short_name == "R2W2"
    assert str(r.id) == CommonConfig.COF_ROUND_2_ID
