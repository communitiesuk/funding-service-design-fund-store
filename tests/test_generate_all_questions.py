import json
import os

import pytest
from db.models.section import Section
from scripts.all_questions.generate_test_data import generate_test_data
from scripts.all_questions.generate_test_data import HOW_IS_ORG_CLASSIFIED
from scripts.all_questions.generate_test_data import JOINT_BID
from scripts.all_questions.generate_test_data import START_TO_MAIN_ACTIVITIES
from scripts.all_questions.metadata_utils import generate_index
from scripts.all_questions.metadata_utils import generate_metadata
from scripts.generate_all_questions import build_section_header
from scripts.generate_all_questions import find_forms_dir
from scripts.read_forms import increment_lowest_in_hierarchy
from scripts.read_forms import remove_lowest_in_hierarchy
from scripts.read_forms import strip_leading_numbers


metadata_path = "/Users/sarahsloan/dev/temp/metadata_applicant_ns.json"


def test_generate_metadata():
    path_to_form = (
        "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/"
        "fsd_config/form_jsons/night_shelter/applicant-information-ns.json"
    )
    with open(path_to_form, "r") as f:
        form_data = json.load(f)
    metadata = generate_metadata(full_form_data=form_data)
    with open(metadata_path, "w") as f:
        json.dump(metadata, f)


def test_generate_test_data():
    output_folder = "/Users/sarahsloan/dev/temp/"
    files_to_generate = [START_TO_MAIN_ACTIVITIES, HOW_IS_ORG_CLASSIFIED, JOINT_BID]
    generate_test_data(
        target_test_files=files_to_generate,
        in_path=metadata_path,
        out_folder=output_folder,
    )
    "/Users/sarahsloan/dev/temp/metadata_applicant_ns.json"


def test_generate_index_applicant_ns():
    with open("/Users/sarahsloan/dev/temp/metadata_applicant_ns.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 4
    start_level = results["/13-applicant-information"]
    assert results["/lead-contact-details"] == start_level
    assert results["/authorised-signatory-details"] == start_level + 1
    assert results["/summary"] == start_level


def test_generate_index_risk_cyp():
    with open("/Users/sarahsloan/dev/temp/metadata_risk_cyp.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 5
    start_level = results["/intro-risk-and-deliverability"]
    for _, value in results.items():
        assert value == start_level


def test_generate_index_name_app_cyp():
    with open("/Users/sarahsloan/dev/temp/metadata_name_app_cyp.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 2
    start_level = results["/name-your-application"]
    assert results["/summary"] == start_level


def test_generate_index_branch_out_multi_pages_back_to_parent_sibling():
    with open("/Users/sarahsloan/dev/temp/joint_bid_out_and_back.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 5
    start_level = results["/joint-bid"]
    assert results["/partner-organisation-details"] == start_level + 1
    assert results["/work-with-partner-organisations"] == start_level + 1
    assert results["/agreement-exists"] == start_level + 1
    assert results["/website-and-social-media"] == start_level


def test_generate_index_branch_out_all_back_to_new():
    with open("/Users/sarahsloan/dev/temp/how_is_org_classified.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 5
    start_level = results["/how-is-your-organisation-classified"]
    assert results["/how-is-your-organisation-classified-other"] == start_level + 1
    assert results["/charity-number"] == start_level + 1
    assert results["/company-registration-number"] == start_level + 1
    assert results["/organisation-address"] == start_level


def test_generate_index_simple_branch():
    with open("/Users/sarahsloan/dev/temp/start_to_main_activites.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 4
    org_details_level = results["/organisation-details"]
    assert results["/alternative-organisation-name"] == org_details_level + 1
    assert (
        results["/tell-us-about-your-organisations-main-activities"]
        == org_details_level
    )


def test_generate_index_about_your_org_cyp():
    with open("/Users/sarahsloan/dev/temp/metadata_about_your_org_cyp.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"], start_page=True)

    assert len(results) == 16
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
    assert results["/organisation-address"] == org_details_level

    with open("/Users/sarahsloan/dev/temp/metadata_about_your_org_cyp.json", "r") as f:
        form_data = json.load(f)

    results = {}


def test_generate_cut_down_form():
    path_to_form = (
        "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/"
        "fsd_config/form_jsons/cof_r3w2/en/organisation-information-cof-r3-w2.json"
    )
    with open(path_to_form, "r") as f:
        form_data = json.load(f)

    cutdown = {"start_page": form_data["startPage"], "all_pages": []}
    for page in form_data["pages"]:
        cp = {"path": page["path"], "next_paths": [p["path"] for p in page["next"]]}
        cutdown["all_pages"].append(cp)

    with open("/Users/sarahsloan/dev/temp/cutdown_about_your_org_cyp.json", "w") as f:
        json.dump(cutdown, f)


metadata_path = "/Users/sarahsloan/dev/temp/metadata_org_info_cof_r3w2.json"


def test_generate_metadata():
    path_to_form = (
        "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/"
        "fsd_config/form_jsons/cof_r3w2/en/organisation-information-cof-r3-w2.json"
    )
    with open(path_to_form, "r") as f:
        form_data = json.load(f)
    metadata = generate_metadata(full_form_data=form_data)
    with open(metadata_path, "w") as f:
        json.dump(metadata, f)


def test_generate_test_data():
    output_folder = "/Users/sarahsloan/dev/temp/"
    files_to_generate = [START_TO_MAIN_ACTIVITIES, HOW_IS_ORG_CLASSIFIED, JOINT_BID]
    generate_test_data(
        target_test_files=files_to_generate,
        in_path=metadata_path,
        out_folder=output_folder,
    )
    "/Users/sarahsloan/dev/temp/metadata_applicant_ns.json"


def test_generate_index_org_info_cof_r3w2():
    with open("/Users/sarahsloan/dev/temp/metadata_org_info_cof_r3w2.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"], start_page=True)

    assert len(results) == 18
    org_details_level = results["/organisation-names"]
    assert results["/alternative-names-of-your-organisation"] == org_details_level + 1
    assert results["/purpose-and-activities"] == org_details_level
    assert results["/previous-projects-similar-to-this-one"] == org_details_level + 1

    assert results["/how-your-organisation-is-classified"] == org_details_level
    assert (
        results["/how-your-organisation-is-classified-other"] == org_details_level + 1
    )
    # TODO why does this fail assert results["/registration-details"] == org_details_level
    assert results["/trading-subsidiaries"] == org_details_level
    assert results["/parent-organisation-details"] == org_details_level + 1

    assert results["/organisation-address"] == org_details_level
    assert results["/correspondence-address"] == org_details_level + 1
    assert results["/joint-applications"] == org_details_level
    assert results["/partner-organisation-details"] == org_details_level + 1


def test_generate_index_applicant_ns():
    with open("/Users/sarahsloan/dev/temp/metadata_applicant_ns.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 4
    start_level = results["/13-applicant-information"]
    assert results["/lead-contact-details"] == start_level
    assert results["/authorised-signatory-details"] == start_level + 1
    assert results["/summary"] == start_level


def test_generate_index_risk_cyp():
    with open("/Users/sarahsloan/dev/temp/metadata_risk_cyp.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 5
    start_level = results["/intro-risk-and-deliverability"]
    for _, value in results.items():
        assert value == start_level


def test_generate_index_name_app_cyp():
    with open("/Users/sarahsloan/dev/temp/metadata_name_app_cyp.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 2
    start_level = results["/name-your-application"]
    assert results["/summary"] == start_level


def test_generate_index_branch_out_multi_pages_back_to_parent_sibling():
    with open("/Users/sarahsloan/dev/temp/joint_bid_out_and_back.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 5
    start_level = results["/joint-bid"]
    assert results["/partner-organisation-details"] == start_level + 1
    assert results["/work-with-partner-organisations"] == start_level + 1
    assert results["/agreement-exists"] == start_level + 1
    assert results["/website-and-social-media"] == start_level


def test_generate_index_branch_out_all_back_to_new():
    with open("/Users/sarahsloan/dev/temp/how_is_org_classified.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 5
    start_level = results["/how-is-your-organisation-classified"]
    assert results["/how-is-your-organisation-classified-other"] == start_level + 1
    assert results["/charity-number"] == start_level + 1
    assert results["/company-registration-number"] == start_level + 1
    assert results["/organisation-address"] == start_level


def test_generate_index_simple_branch():
    with open("/Users/sarahsloan/dev/temp/start_to_main_activites.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 4
    org_details_level = results["/organisation-details"]
    assert results["/alternative-organisation-name"] == org_details_level + 1
    assert (
        results["/tell-us-about-your-organisations-main-activities"]
        == org_details_level
    )


def test_generate_index_about_your_org_cyp():
    with open("/Users/sarahsloan/dev/temp/metadata_about_your_org_cyp.json", "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(
        p for p in form_data["all_pages"] if p["path"] == form_data["start_page"]
    )
    generate_index(first_page, results, 1, form_data["all_pages"], start_page=True)

    assert len(results) == 16
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
    assert results["/organisation-address"] == org_details_level


@pytest.mark.parametrize(
    "number,exp",
    [
        ("5.1", "5"),
        ("5.0.0", "5.0"),
        ("5.1.2", "5.1"),
        ("5", ""),
        ("5.1.2.3.4.6", "5.1.2.3.4"),
    ],
)
def test_remove_lowest_in_hierarchy(number, exp):
    assert remove_lowest_in_hierarchy(number) == exp


@pytest.mark.parametrize(
    "number,exp",
    [
        ("5.1", "5.2"),
        ("5.1.", "5.2"),
        ("5.1.2", "5.1.3"),
        ("5", "6"),
        ("5.1.2.3.4.5", "5.1.2.3.4.6"),
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


# def test_build_display_for_form_cyp_r1_risk():

#     path_to_form = (
#         "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/"
#         "fsd_config/form_jsons/cyp_r1/risk-and-deliverability-cyp.json"
#     )
#     with open(path_to_form, "r") as f:
#         form_data = json.load(f)

#     result = build_display_for_form(form_data)
#     assert len(result) == 4


# def test_build_page_index_cyp_r1_about_org():

#     path_to_form = (
#         "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/"
#         "fsd_config/form_jsons/cyp_r1/about-your-organisation-cyp.json"
#     )
#     with open(path_to_form, "r") as f:
#         form_data = json.load(f)

#     index = build_page_index(form_data)
#     assert len(index) == 4


# def test_build_page_index_cyp_r1_risk():

#     path_to_form = (
#         "/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/"
#         "fsd_config/form_jsons/cyp_r1/risk-and-deliverability-cyp.json"
#     )
#     with open(path_to_form, "r") as f:
#         form_data = json.load(f)

#     index = build_page_index(form_data)
#     assert len(index) == 4
#     assert index["4"]["page"]["path"] == "/organisation-governance-structure"


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
