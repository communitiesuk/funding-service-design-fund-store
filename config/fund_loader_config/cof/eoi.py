# flake8: noqa
import textwrap
from datetime import datetime
from datetime import timezone

from config.fund_loader_config.cof.eoi_r1_schema import COF_R3_EOI_SCHEMA_CY
from config.fund_loader_config.cof.eoi_r1_schema import COF_R3_EOI_SCHEMA_EN
from config.fund_loader_config.cof.shared import EOI_APPLICATION_GUIDANCE
from config.fund_loader_config.cof.shared import fund_config
from config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    COF_EOI_BASE_PATH,
)
from config.fund_loader_config.logo import DLUHC_LOGO_PNG
from db.models.fund import FundingType

COF_FUND_ID = "54c11ec2-0b16-46bb-80d2-f210e47a8791"
COF_EOI_ROUND_ID = "6a47c649-7bac-4583-baed-9c4e7a35c8b3"

APPLICATION_BASE_PATH_COF_EOI = ".".join([str(COF_EOI_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH_COF_EOI = ".".join([str(COF_EOI_BASE_PATH), str(2)])

COF_EOI_OPENS_DATE = datetime(2024, 3, 6, 14, 00, 0, tzinfo=timezone.utc)  # 2023-12-06 14:00:00
COF_EOI_ASSESSMENT_OPENS_DATE = COF_EOI_OPENS_DATE
COF_EOI_DEADLINE_DATE = datetime(2024, 5, 25, 0, 1, 0, tzinfo=timezone.utc)  # 2024-05-25 00:01:00 (1min past midnight)
COF_EOI_ASSESSMENT_DEADLINE_DATE = datetime(2124, 3, 6, 12, 0, 0, tzinfo=timezone.utc)  # 2124-03-06 12:00:00

fund_config = {
    "id": COF_FUND_ID,
    "name_json": {
        "en": "Community Ownership Fund - Expression of Interest",
        "cy": "Y Cronfa Perchnogaeth Gymunedol - Mynegi diddordeb",
    },
    "title_json": {
        "en": "expression of interest in applying for the Community Ownership Fund",
        "cy": "Gwneud cais am ddatganiad o ddiddordeb mewn gwneud cais i'r Gronfa Perchnogaeth Gymunedol",
    },
    "short_name": "COF-EOI",
    "funding_type": FundingType.EOI,
    "description_json": fund_config["description_json"],
    "welsh_available": True,
    "owner_organisation_name": "Department for Levelling Up, Housing and Communities",
    "owner_organisation_shortname": "DLUHC",
    "owner_organisation_logo_uri": DLUHC_LOGO_PNG,
}

cof_eoi_sections = [
    {
        "section_name": {
            "en": "1. Expression of interest",
            "cy": "1. Mynegi diddordeb",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1",
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "1.1 Organisation details",
            "cy": "1.1 Manylion y sefydliad",
        },
        "form_name_json": {
            "en": "organisation-details",
            "cy": "manylion-y-sefydliad",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1.1",
    },
    {
        "section_name": {
            "en": "1.2 About your asset",
            "cy": "1.2 Ynglŷn â'ch ased",
        },
        "form_name_json": {
            "en": "about-your-asset",
            "cy": "ynglyn-ach-ased",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1.2",
    },
    {
        "section_name": {
            "en": "1.3 Your funding request",
            "cy": "1.3 Eich cais am gyllid",
        },
        "form_name_json": {
            "en": "your-funding-request",
            "cy": "eich-cais-am-gyllid",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1.3",
    },
    {
        "section_name": {
            "en": "1.4 Development support provider (not scored)",
            "cy": "1.4 Darparwr cymorth datblygu (heb ei sgorio)",
        },
        "form_name_json": {
            "en": "development-support-provider",
            "cy": "darparwr-cymorth-datblygu",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1.4",
    },
    {
        "section_name": {
            "en": "1.5 Declaration",
            "cy": "1.5 Datganiad",
        },
        "form_name_json": {
            "en": "declaration",
            "cy": "datganiad",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1.5",
    },
]

round_config_eoi = [
    {
        "id": COF_EOI_ROUND_ID,
        "fund_id": COF_FUND_ID,
        "title_json": {"en": "Expression of interest", "cy": "Mynegi diddordeb"},
        "short_name": "R1",
        "opens": COF_EOI_OPENS_DATE,
        "assessment_start": COF_EOI_ASSESSMENT_OPENS_DATE,
        "deadline": COF_EOI_DEADLINE_DATE,
        "application_reminder_sent": False,
        "reminder_date": None,
        "assessment_deadline": COF_EOI_ASSESSMENT_DEADLINE_DATE,
        "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
        "privacy_notice": (
            "https://www.gov.uk/government/publications/community-ownership-fund-"
            "privacy-notice/community-ownership-fund-privacy-notice"
        ),
        "reference_contact_page_over_email": True,
        "contact_us_banner_json": {
            "en": textwrap.dedent(
                """
                 <h2 class="govuk-heading-m">Get application support</h2>
                 <p class="govuk-body">
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund">Visit the My Community website</a>
                    for information and guidance on applying to Community Ownership Fund.
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund#enquiry-form">Fill out the enquiry form</a>
                    to request advice from My Community.
                </p>
                <p class="govuk-body">
                    We cannot provide direct support to applicants outside of this service.
                </p>
                <h2 class="govuk-heading-m">Get technical support</h2>
                <p  class="govuk-body">
                    Contact the Department of Levelling Up, Housing and Communities funding team if you need
                    help with accessing or submitting an application form.
                </p>
            """
            ),
            "cy": textwrap.dedent(
                """
                 <h2 class="govuk-heading-m">Cael cymorth â'r cais</h2>
                 <p class="govuk-body">
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund">Ewch i wefan My Community</a>
                    i gael gwybodaeth ac arweiniad ar wneud cais i'r Gronfa Perchnogaeth Gymunedol.
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund#enquiry-form">Llenwch y ffurflen ymholiad</a>
                    i ofyn am gyngor gan My Community.
                </p>
                <p class="govuk-body">
                    Ni allwn ddarparu cymorth uniongyrchol i ymgeiswyr tu hwnt i'r gwasanaeth hwn.
                </p>
                <h2 class="govuk-heading-m">Cael cymorth technegol</h2>
                <p  class="govuk-body">
                    Cysylltwch â thîm cyllid yr Adran Ffyniant Bro, Tai a Chymunedau os oes angen help arnoch i gael at ffurflen gais neu ei chyflwyno.
                </p>
            """
            ),
        },
        "contact_email": "COF@communities.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions_json": {
            "en": (
                "You must complete this Expression of Interest (EOI) form if you"
                " are interested in applying for the Community Ownership Fund (COF)."
            ),
            "cy": (
                "Mae'n rhaid i chi gwblhau'r ffurflen Datganiad o Ddiddordeb hon os"
                " oes diddordeb gennych mewn gwneud cais i'r Gronfa Perchnogaeth Gymunedol."
            ),
        },
        "feedback_link": (
            "https://forms.office.com/Pages/ResponsePage.aspx?id="
            "EGg0v32c3kOociSi7zmVqFJBHpeOL2tNnpiwpdL2iElURUY1WkhaS0NFMlZVQUhYQ1NaN0E4RjlQMC4u"
        ),
        "project_name_field_id": "SMRWjl",
        "application_guidance_json": EOI_APPLICATION_GUIDANCE,
        "guidance_url": (
            "https://www.gov.uk/government/publications/community-ownership-fund-round-3-application-form"
            "-assessment-criteria-guidance"
        ),
        "all_uploaded_documents_section_available": False,
        "application_fields_download_available": True,
        "display_logo_on_pdf_exports": False,
        "mark_as_complete_enabled": False,
        "is_expression_of_interest": True,
        "feedback_survey_config": {
            "has_feedback_survey": False,
            "has_section_feedback": True,
            "is_feedback_survey_optional": False,
            "is_section_feedback_optional": True,
        },
        "eligibility_config": {"has_eligibility": False},
        "eoi_decision_schema": {"en": COF_R3_EOI_SCHEMA_EN, "cy": COF_R3_EOI_SCHEMA_CY},
    }
]
