#!/usr/bin/env python3
# flake8: noqa
from app import app  # noqa: E402
from fsd_utils import CommonConfig  # noqa: E402

from config import Config  # noqa: E402

from scripts.deprecated_config.sort_application_sections import return_numerically_sorted_section_for_application
from scripts.deprecated_config.sort_assessment_sections import return_numerically_sorted_section_for_assessment
from scripts.deprecated_config.assessment_section_config import scored_sections, unscored_sections
from db.queries import insert_application_sections
from db.queries import insert_fund_data
from db.queries import insert_round_data
from db.queries import insert_assessment_sections
from db.queries import upsert_fields

with app.app_context():
    application_tree_base_path = "0.1"
    assessment_tree_base_path = "0.2"

    # -- convert old config into new config (stage not necessary for new rounds) --
    sorted_application_sections = return_numerically_sorted_section_for_application(CommonConfig.COF_R2_ORDERED_FORMS_CONFIG, application_tree_base_path)["sorted_sections"]
    assessment_config = return_numerically_sorted_section_for_assessment(scored_sections, unscored_sections)

    # -- load fund and rounds --
    fund_config = {
        "id":'47aef2f5-3fcb-4d45-acb5-f0152b5f03c4', 
        "name":'Community Ownership Fund', 
        "title":'funding to save an asset in your community', 
        "short_name":"COF", 
        "description":"The Community Ownership Fund is a £150 million fund over 4 years to support community groups across England, Wales, Scotland and Northern Ireland to take ownership of assets which are at risk of being lost to the community."
    }

    rounds_config = [{
        "id":'c603d114-5364-4474-a0c4-c41cbf4d3bbd',
        "title":'Round 2 Window 2',
        "short_name":'R2W2',
        "opens":'2022-10-04 12:00:00',
        "deadline":'2022-12-14 11:59:00',
        "fund_id":'47aef2f5-3fcb-4d45-acb5-f0152b5f03c4',
        "assessment_deadline":'2023-03-30 12:00:00',
        "prospectus":'https://www.gov.uk/government/publications/community-ownership-fund-prospectus',
        "privacy_notice":'https://www.gov.uk/government/publications/community-ownership-fund-privacy-notice/community-ownership-fund-privacy-notice',
        "contact_email":'COF@levellingup.gov.uk',
        "contact_phone": None,
        "contact_textphone": None,
        "support_times":'9am to 5pm',
        "support_days":'Monday to Friday',
        "instructions":'You must have received an invitation to apply. If we did not invite you, first <a href="https://www.gov.uk/government/publications/community-ownership-fund-prospectus"> express your interest in the fund</a>.'
    }]

    inserted_fund = insert_fund_data(fund_config)
    print("Fund inserted:")
    print(inserted_fund)
    inserted_rounds = insert_round_data(rounds_config)
    print("Rounds inserted:")
    print(inserted_rounds)

    # load base sections
    tree_base_sections = [
        {'section_name': 'Application', 'tree_path': application_tree_base_path, 'weighting': None},
        {'section_name': 'Assessment', 'tree_path': assessment_tree_base_path, 'weighting': None}
    ]
    insert_application_sections(CommonConfig.COF_ROUND_2_ID, tree_base_sections)

    # -- load fields belonging to round --
    # inserted_field_ids = upsert_fields(assessment_config["all_fields"])

    # -- load application sections --
    application_result = insert_application_sections(CommonConfig.COF_ROUND_2_ID, sorted_application_sections)

    # -- load assessment sections --
    # assessment_result = insert_assessment_sections(CommonConfig.COF_ROUND_2_ID, assessment_config)