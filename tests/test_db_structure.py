from typing import List

import pytest
from db.models.section import Section
from db.queries import get_application_sections_for_round
from db.queries import get_assessment_sections_for_round
from db.queries import get_fund_by_id
from db.queries import get_fund_by_short_name
from db.queries import get_round_by_id
from db.queries import get_round_by_short_name
from db.queries import get_sections_for_round
from fsd_utils.config.commonconfig import CommonConfig


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


def test_get_application_sections(seed_fund_data):
    sections: List[Section] = get_application_sections_for_round(
        CommonConfig.COF_ROUND_2_ID
    )
    assert len(sections) == 2
    assert sections[0].title == "About your organisation"
    assert len(sections[0].children) == 2
    assert sections[1].title == "Strategic case"
    assert len(sections[1].children) == 2


def test_get_assessment_sections(seed_fund_data):
    sections: List[Section] = get_assessment_sections_for_round(
        CommonConfig.COF_ROUND_2_ID
    )
    assert len(sections) == 2
    assert sections[0].title == "Unscored"
    assert len(sections[0].children) == 5
    assert sections[1].title == "Scored"
    assert len(sections[1].children) == 1

    sections: List[Section] = get_assessment_sections_for_round(
        CommonConfig.COF_ROUND_2_W3_ID
    )
    assert len(sections) == 2
    assert sections[0].title == "Unscored"
    assert len(sections[0].children) == 2
    assert sections[1].title == "Scored"
    assert len(sections[1].children) == 0


@pytest.mark.skip(reason="tdd")
def test_get_sections_for_round(seed_fund_data):
    sections = get_sections_for_round(CommonConfig.COF_ROUND_2_ID)
    for section in sections:
        print(section.title)
