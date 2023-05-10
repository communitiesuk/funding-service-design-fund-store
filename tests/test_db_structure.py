from typing import List

import pytest
from db.models.section import Section
from db.queries import get_all_funds
from db.queries import get_application_sections_for_round
from db.queries import get_assessment_sections_for_round
from db.queries import get_fund_by_id
from db.queries import get_fund_by_short_name
from db.queries import get_round_by_id
from db.queries import get_round_by_short_name
from db.queries import get_rounds_for_fund_by_id
from db.queries import get_rounds_for_fund_by_short_name
from db.queries import get_sections_for_round
from db.queries import insert_application_sections
from db.queries import insert_assessment_sections
from db.queries import upsert_fields
from fsd_test_utils.test_config.useful_config import UsefulConfig
from scripts.deprecated_config.assessment_section_config import scored_sections
from scripts.deprecated_config.assessment_section_config import (
    unscored_sections,
)
from scripts.deprecated_config.sort_application_sections import (
    return_numerically_sorted_section_for_application,
)
from scripts.deprecated_config.sort_assessment_sections import (
    return_numerically_sorted_section_for_assessment,
)


def test_get_fund_by_id(seed_dynamic_data):
    f = get_fund_by_id(seed_dynamic_data["funds"][0]["id"])
    short = seed_dynamic_data["funds"][0]["short_name"]
    assert f.name == f"Unit Test Fund {short}"
    assert f.short_name == f"{short}"


def test_get_fund_by_short_name(seed_dynamic_data):
    short = seed_dynamic_data["funds"][0]["short_name"]
    f = get_fund_by_short_name(f"{short}")
    assert f.name == f"Unit Test Fund {short}"
    assert f.short_name == f"{short}"


def test_get_round_by_id(seed_fund_data):
    r = get_round_by_id(UsefulConfig.COF_FUND_ID, UsefulConfig.COF_ROUND_2_ID)
    assert r.title == "Round 2 Window 2"
    assert r.short_name == "R2W2"
    assert str(r.id) == UsefulConfig.COF_ROUND_2_ID


def test_get_rounds_for_fund_by_id(seed_fund_data):
    r = get_rounds_for_fund_by_id(UsefulConfig.COF_FUND_ID)
    assert len(r) == 2
    assert r[0].title == "Round 2 Window 2"
    assert r[0].short_name == "R2W2"
    assert str(r[0].id) == UsefulConfig.COF_ROUND_2_ID


def test_get_rounds_for_fund_by_short_name(seed_fund_data):
    r = get_rounds_for_fund_by_short_name("COF")
    assert len(r) == 2
    assert r[0].title == "Round 2 Window 2"
    assert r[0].short_name == "R2W2"
    assert str(r[0].id) == UsefulConfig.COF_ROUND_2_ID


@pytest.mark.parametrize(
    "fund_short_name, round_short_name, expected_none, expected_title",
    [
        ("COF", "R2W2", False, "Round 2 Window 2"),
        ("cof", "r2w2", False, "Round 2 Window 2"),
        ("bad", "r2w2", True, None),
        ("cof", "bad", True, None),
        ("cof", "r2w3", False, "Round 2 Window 3"),
    ],
)
def test_get_round_by_short_name(
    fund_short_name,
    round_short_name,
    expected_none,
    expected_title,
    seed_fund_data,
):
    r = get_round_by_short_name(fund_short_name, round_short_name)

    if expected_none:
        assert r is None
    else:
        assert r.title == expected_title


def test_get_application_sections(seed_fund_data):
    sections: List[Section] = get_application_sections_for_round(
        UsefulConfig.COF_FUND_ID, UsefulConfig.COF_ROUND_2_ID
    )
    assert len(sections) == 2
    assert sections[0].title == "About your organisation"
    assert len(sections[0].children) == 2
    assert (
        sections[0].children[0].form_name[0].form_name
        == "organisation-information"
    )
    assert sections[1].title == "Strategic case"
    assert len(sections[1].children) == 2


def test_get_assessment_sections(seed_fund_data):
    sections: List[Section] = get_assessment_sections_for_round(
        UsefulConfig.COF_FUND_ID, UsefulConfig.COF_ROUND_2_ID, "en"
    )
    assert len(sections) == 2
    assert sections[0].title == "Unscored"
    assert len(sections[0].children) == 5
    assert sections[1].title == "Scored"
    assert len(sections[1].children) == 1

    sections: List[Section] = get_assessment_sections_for_round(
        UsefulConfig.COF_FUND_ID, UsefulConfig.COF_ROUND_2_W3_ID, "en"
    )
    assert len(sections) == 2
    assert sections[0].title == "Unscored"
    assert len(sections[0].children) == 2
    assert sections[1].title == "Scored"
    assert len(sections[1].children) == 0


def test_get_all_funds(seed_fund_data):
    result = get_all_funds(True)
    assert len(result) == 1
    assert result[0]["name"] == "Community Ownership Fund"
    result = get_all_funds(False)
    assert len(result) == 1
    assert result[0].name == "Community Ownership Fund"


@pytest.mark.skip(reason="tdd")
def test_get_sections_for_round(seed_fund_data):
    sections = get_sections_for_round(UsefulConfig.COF_ROUND_2_ID)
    for section in sections:
        print(section.title)


def test_load_application_sections(seed_only_fund_and_round_data):
    sorted_application_sections = (
        return_numerically_sorted_section_for_application(
            UsefulConfig.COF_R2_ORDERED_FORMS_CONFIG
        )["sorted_sections"]
    )
    result = insert_application_sections(
        UsefulConfig.COF_ROUND_2_ID, sorted_application_sections
    )
    assert len(result) == 28


def test_load_assessment_sections(seed_only_fund_and_round_data):
    # input config
    assessment_config = return_numerically_sorted_section_for_assessment(
        scored_sections, unscored_sections
    )

    inserted_field_ids = upsert_fields(assessment_config["all_fields"])
    result = insert_assessment_sections(
        UsefulConfig.COF_ROUND_2_ID, assessment_config
    )

    assert len(inserted_field_ids) == 124
    assert len(result["inserted_sections"]) == 53
    assert len(result["inserted_section_field_links"]) == 124
