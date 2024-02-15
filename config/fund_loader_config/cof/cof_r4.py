from datetime import datetime
from datetime import timezone

from config.fund_loader_config.cof.shared import COF_APPLICATION_GUIDANCE
from config.fund_loader_config.cof.shared import fund_config
from config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    COF_R4_W1_BASE_PATH,
)

COF_FUND_ID = fund_config["id"]
COF_ROUND_4_WINDOW_1_ID = "33726b63-efce-4749-b149-20351346c76e"

APPLICATION_BASE_PATH_COF_R4_W1 = ".".join([str(COF_R4_W1_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH_COF_R4_W1 = ".".join([str(COF_R4_W1_BASE_PATH), str(2)])

# TODO Dates are still being debated and are likely to change
COF_R4W1_OPENS_DATE = datetime(2024, 3, 13, 11, 00, 0, tzinfo=timezone.utc)  # 2024-04-13 11:00:00
COF_R4W1_SEND_REMINDER_DATE = datetime(2024, 3, 22, 11, 59, 0, tzinfo=timezone.utc)  # 2024-03-22 11:59:00
COF_R4W1_DEADLINE_DATE = datetime(2024, 4, 24, 11, 59, 0, tzinfo=timezone.utc)  # 2024-04-24 11:59:00
COF_R4W1_ASSESSMENT_DEADLINE_DATE = datetime(2024, 6, 23, 12, 0, 0, tzinfo=timezone.utc)  # 2024-06-23 12:00:00

cof_r4w1_sections = [
    {
        "section_name": {
            "en": "1. About your organisation",
            "cy": "1. Ynglŷn â'ch sefydliad",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.1",
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "1.1 Organisation information",
            "cy": "1.1 Gwybodaeth am y sefydliad",
        },
        "form_name_json": {
            "en": "organisation-information-cof",
            "cy": "gwybodaeth-am-y-sefydliad-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.1.1",
    },
    {
        "section_name": {
            "en": "1.2 Applicant information",
            "cy": "1.2 Gwybodaeth am yr ymgeisydd",
        },
        "form_name_json": {
            "en": "applicant-information-cof",
            "cy": "gwybodaeth-am-yr-ymgeisydd-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.1.2",
    },
    {
        "section_name": {
            "en": "2. About your project",
            "cy": "2. Ynglŷn â'ch prosiect",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.2",
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "2.1 Project information",
            "cy": "2.1 Gwybodaeth am y prosiect",
        },
        "form_name_json": {
            "en": "project-information-cof",
            "cy": "gwybodaeth-am-y-prosiect-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.2.1",
    },
    {
        "section_name": {
            "en": "2.2 Asset information",
            "cy": "2.2 Gwybodaeth am yr ased",
        },
        "form_name_json": {
            "en": "asset-information-cof",
            "cy": "gwybodaeth-am-yr-ased-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.2.2",
    },
    {
        "section_name": {"en": "3. Strategic case", "cy": "3. Achos strategol"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3",
        "requires_feedback": True,
        "weighting": 53,
    },
    {
        "section_name": {"en": "3.1 Community use/significance", "cy": "3.1 Defnydd cymunedol"},
        "form_name_json": {
            "en": "community-use-cof",
            "cy": "defnydd-cymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3.1",
    },
    {
        "section_name": {
            "en": "3.2 Community engagement",
            "cy": "3.2 Ymgysylltu â'r gymuned",
        },
        "form_name_json": {
            "en": "community-engagement-cof",
            "cy": "ymgysylltiad-cymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3.2",
    },
    {
        "section_name": {"en": "3.3 Local support", "cy": "3.3 Cefnogaeth leol"},
        "form_name_json": {
            "en": "local-support-cof",
            "cy": "cefnogaeth-leol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3.3",
    },
    {
        "section_name": {
            "en": "3.4 Community benefits",
            "cy": "3.4 Buddion cymunedol",
        },
        "form_name_json": {
            "en": "community-benefits-cof",
            "cy": "buddion-cymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3.4",
    },
    {
        "section_name": {
            "en": "3.5 Environmental sustainability",
            "cy": "3.5 Cynaliadwyedd amgylcheddol",
        },
        "form_name_json": {
            "en": "environmental-sustainability-cof",
            "cy": "cynaliadwyedd-amgylcheddol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3.5",
    },
    {
        "section_name": {"en": "4. Management case", "cy": "4. Achos rheoli"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4",
        "weighting": 47,
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "4.1 Funding required",
            "cy": "4.1 Cyllid sydd ei angen",
        },
        "form_name_json": {
            "en": "funding-required-cof",
            "cy": "cyllid-sydd-ei-angen-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.1",
    },
    {
        "section_name": {"en": "4.2 Feasibility", "cy": "4.2 Dichonoldeb"},
        "form_name_json": {
            "en": "feasibility-cof",
            "cy": "dichonoldeb-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.2",
    },
    {
        "section_name": {"en": "4.3 Risk", "cy": "4.3 Risg"},
        "form_name_json": {"en": "risk-cof", "cy": "risg-cof"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.3",
    },
    {
        "section_name": {"en": "4.4 Operational costs", "cy": "4.4 Costau gweithredol"},
        "form_name_json": {
            "en": "operational-costs-cof",
            "cy": "costau-gweithredol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.4",
    },
    {
        "section_name": {
            "en": "4.5 Skills and resources",
            "cy": "4.5 Sgiliau ac adnoddau",
        },
        "form_name_json": {
            "en": "skills-and-resources-cof",
            "cy": "sgiliau-ac-adnoddau-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.5",
    },
    {
        "section_name": {
            "en": "4.6 Community representation",
            "cy": "4.6 Cynrychiolaeth gymunedol",
        },
        "form_name_json": {
            "en": "community-representation-cof",
            "cy": "cynrychiolaeth-gymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.6",
    },
    {
        "section_name": {
            "en": "4.7 Inclusiveness and integration",
            "cy": "4.7 Cynhwysiant ac integreiddio",
        },
        "form_name_json": {
            "en": "inclusiveness-and-integration-cof",
            "cy": "cynhwysiant-ac-integreiddio-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.7",
    },
    {
        "section_name": {
            "en": "4.8 Upload business plan",
            "cy": "4.8 Lanlwythwch y cynllun busnes",
        },
        "form_name_json": {
            "en": "upload-business-plan-cof",
            "cy": "lanlwythwch-y-cynllun-busnes-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.8",
    },
    {
        "section_name": {"en": "5. Check declarations", "cy": "5. Gwirio datganiadau"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.5",
    },
    {
        "section_name": {"en": "5.1 Declarations", "cy": "5.1 Datganiadau"},
        "form_name_json": {
            "en": "declarations-cof",
            "cy": "cadarnhadau-terfynol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.5.1",
    },
]

round_config_w1 = [
    {
        "id": COF_ROUND_4_WINDOW_1_ID,
        "fund_id": COF_FUND_ID,
        "title_json": {"en": "Round 4 Window 1", "cy": "Round 4 Window 1"},
        "short_name": "R4W1",
        "opens": COF_R4W1_OPENS_DATE,
        "assessment_start": None,
        "deadline": COF_R4W1_DEADLINE_DATE,
        "application_reminder_sent": False,
        "reminder_date": COF_R4W1_SEND_REMINDER_DATE,
        "assessment_deadline": COF_R4W1_ASSESSMENT_DEADLINE_DATE,
        "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
        "privacy_notice": (
            "https://www.gov.uk/government/publications/community-ownership-fund-"
            "privacy-notice/community-ownership-fund-privacy-notice"
        ),
        "contact_email": "COF@levellingup.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions": (
            "You must have received an invitation to apply. If we did not invite you,"
            " first <a"
            ' href="https://www.gov.uk/guidance/community-ownership-fund-round-3-how-'
            'to-express-your-interest-in-applying">'
            " express your interest in the fund</a>."
        ),
        "feedback_link": (
            "https://forms.office.com/Pages/ResponsePage.aspx?id="
            "EGg0v32c3kOociSi7zmVqFJBHpeOL2tNnpiwpdL2iElURUY1WkhaS0NFMlZVQUhYQ1NaN0E4RjlQMC4u"
        ),
        "project_name_field_id": "apGjFS",
        "application_guidance": COF_APPLICATION_GUIDANCE,
        "guidance_url": (
            "https://www.gov.uk/government/publications/community-ownership-fund-round-3-application-form"
            "-assessment-criteria-guidance"
        ),
        "all_uploaded_documents_section_available": True,
        "application_fields_download_available": True,
        "display_logo_on_pdf_exports": False,
        "mark_as_complete_enabled": True,
        "feedback_survey_config": {
            "has_feedback_survey": True,
            "has_section_feedback": True,
            "is_feedback_survey_optional": False,
            "is_section_feedback_optional": False,
        },
        "eligibility_config": {"has_eligibility": False},
        "eoi_decision_schema": None,
    }
]
