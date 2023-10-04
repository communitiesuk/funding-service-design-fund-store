import json
import os

import pytest
from db.models.section import Section
from scripts.generate_all_questions import build_section_header
from scripts.generate_all_questions import find_forms_dir
from scripts.read_forms import build_display_for_form
from scripts.read_forms import build_hierarchy
from scripts.read_forms import build_page_index
from scripts.read_forms import increment_lowest_in_hierarchy
from scripts.read_forms import strip_leading_numbers


def test_build_hierarchy():
    path_to_form = (
        "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/"
        "fsd_config/form_jsons/cyp_r1/about-your-organisation-cyp.json"
    )
    with open(path_to_form, "r") as f:
        form_data = json.load(f)

    results = build_hierarchy(form_data)
    org_details_level = results["/organisation-details"]
    assert results["/alternative-organisation-name"] == org_details_level + 1
    assert (
        results["/tell-us-about-your-organisations-main-activities"]
        == org_details_level
    )
    assert results["/how-is-your-organisation-classified"] == org_details_level
    assert (
        results["/how-is-your-organisation-classified-other"] == org_details_level + 1
    )
    assert results["/organsiation-address"] == org_details_level


@pytest.mark.parametrize(
    "number,exp",
    [
        ("5.1", "5.2."),
        ("5.1.", "5.2."),
        ("5.1.2", "5.1.3."),
        ("5", "6."),
        ("5.1.2.3.4.5", "5.1.2.3.4.6."),
    ],
)
def test_increment_lowest_in_hierarchy(number, exp):
    assert increment_lowest_in_hierarchy(number) == exp


@pytest.mark.parametrize(
    "text,exp",
    [
        ("5.1 hello", "hello"),
        ("5.1. hello", "hello"),
        ("55.1. hello", "hello"),
        ("5.13. hello", "hello"),
        ("hello", "hello"),
    ],
)
def test_strip_leading_numbers(text, exp):
    assert strip_leading_numbers(text) == exp


def test_build_display_for_form_cyp_r1_risk():

    path_to_form = (
        "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/"
        "fsd_config/form_jsons/cyp_r1/risk-and-deliverability-cyp.json"
    )
    with open(path_to_form, "r") as f:
        form_data = json.load(f)

    result = build_display_for_form(form_data)
    assert len(result) == 4


def test_build_page_index_cyp_r1_about_org():

    path_to_form = (
        "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/"
        "fsd_config/form_jsons/cyp_r1/about-your-organisation-cyp.json"
    )
    with open(path_to_form, "r") as f:
        form_data = json.load(f)

    index = build_page_index(form_data)
    assert len(index) == 4


def test_build_page_index_cyp_r1_risk():

    path_to_form = (
        "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/"
        "fsd_config/form_jsons/cyp_r1/risk-and-deliverability-cyp.json"
    )
    with open(path_to_form, "r") as f:
        form_data = json.load(f)

    index = build_page_index(form_data)
    assert len(index) == 4
    assert index["4"]["page"]["path"] == "/organisation-governance-structure"


# def test_build_questions_cyp_r1_name_your_application():
#     path = "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/fsd_config/form_jsons/cyp_r1/"
#     pages = build_questions(None, "name-your-application-cyp", path)
#     assert len(pages) == 1
#     assert pages[1]["title"] == "Name your application"
#     assert len(pages[1]["components"]) == 1
#     assert pages[1]["components"][0]["title"] == "Name your application"
#     assert pages[1]["components"][0]["hide_title"] is True
#     assert len(pages[1]["components"][0]["text"]) == 2


@pytest.mark.parametrize(
    "section,lang,exp_anchor,exp_text",
    [
        (
            Section(title_json={"en": "Before You Start"}),
            "en",
            "before-you-start",
            "Before You Start",
        ),
        (
            Section(title_json={"en": "1. Before You Start"}),
            "en",
            "before-you-start",
            "Before You Start",
        ),
        (
            Section(title_json={"en": "Before You Start", "cy": "Welsh"}),
            "cy",
            "welsh",
            "Welsh",
        ),
        (
            Section(title_json={"en": "Before You Start", "cy": "10. Welsh"}),
            "cy",
            "welsh",
            "Welsh",
        ),
    ],
)
def test_build_section_headers(section, lang, exp_anchor, exp_text):
    res_anchor, res_text = build_section_header(section, lang)
    assert res_anchor == exp_anchor
    assert res_text == exp_text


def test_find_forms_dir_no_lang(tmp_path):
    temp_json_dir = os.path.join(tmp_path, "form_jsons")
    os.mkdir(temp_json_dir)
    round_dir = os.path.join(temp_json_dir, "f1_r1")
    os.mkdir(round_dir)
    result = find_forms_dir(temp_json_dir, "f1", "r1", "en")
    assert result == round_dir


def test_find_forms_dir_with_lang(tmp_path):
    temp_json_dir = os.path.join(tmp_path, "form_jsons")
    os.mkdir(temp_json_dir)
    round_dir = os.path.join(temp_json_dir, "f1_r1")
    os.mkdir(round_dir)
    round_dir = os.path.join(round_dir, "en")
    os.mkdir(round_dir)
    result = find_forms_dir(temp_json_dir, "f1", "r1", "en")
    assert result == round_dir
