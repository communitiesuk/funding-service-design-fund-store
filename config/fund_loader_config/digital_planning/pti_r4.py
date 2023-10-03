from datetime import datetime
from datetime import timezone

from config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    PTI_R4_BASE_PATH,
)
from config.fund_loader_config.logo import DLUHC_LOGO_PNG

PTI_FUND_ID = "4fee1393-fdb9-473c-9914-c10134cd902b"
PTI_ROUND_4_ID = "efba29de-60f9-4ae5-bdf3-3b52ddf201a1"
APPLICATION_BASE_PATH = ".".join([str(PTI_R4_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(PTI_R4_BASE_PATH), str(2)])
PTI_R4_OPENS_DATE = datetime(
    2023, 10, 19, 10, 0, 0, tzinfo=timezone.utc
)  # 2023-10-17 10:00:00
PTI_R4_DEADLINE_DATE = datetime(
    2023, 12, 1, 11, 59, 0, tzinfo=timezone.utc
)  # 2023-11-1 11:59:00
PTI_R4_ASSESSMENT_DEADLINE_DATE = datetime(
    2024, 1, 31, 12, 0, 0, tzinfo=timezone.utc
)  # 2023-01-31 12:00:00

PTI_PROSPECTS_LINK = ""  # noqa
PTI_PRIVACY_NOTICE = ""  # TODO(adamdavies1) to be added
PTI_APPLICATION_GUIDANCE = (
    "<h2 class='govuk-heading govuk-heading-s'>Before you start</h2><p"
    f" class='govuk-body'><a href='{PTI_PROSPECTS_LINK}'>Read the fund's prospectus</a>"
    " before you apply.</p><p class='govuk-body'>You can <a"
    " href='{all_questions_url}'>preview the full list of application"
    " questions</a>.</p>"
)

r4_application_sections = [
    {
        "section_name": {"en": "Before you start", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.1",
    },
    {
        "section_name": {"en": "Name your application", "cy": ""},
        "form_name_json": {"en": "name-your-application", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.1.1",
    },
]

fund_config = {
    "id": PTI_FUND_ID,
    "name_json": {
        "en": "PropTech Innovation Fund",
        "cy": "",
    },
    "title_json": {
        "en": "",  # TODO(adamdavies1) add title here
        "cy": "",
    },
    "short_name": "PTI",
    "description_json": {"en": "", "cy": ""},
    "welsh_available": False,
    "owner_organisation_name": "Department for Levelling Up, Housing and Communities",
    "owner_organisation_shortname": "DLUHC",
    "owner_organisation_logo_uri": DLUHC_LOGO_PNG,
}

round_config = [
    {
        "id": PTI_ROUND_4_ID,
        "fund_id": PTI_FUND_ID,
        "title_json": {"en": "Round 4", "cy": ""},
        "short_name": "R4",
        "opens": PTI_R4_OPENS_DATE,
        "deadline": PTI_R4_DEADLINE_DATE,
        "assessment_deadline": PTI_R4_ASSESSMENT_DEADLINE_DATE,
        "prospectus": PTI_PROSPECTS_LINK,
        "privacy_notice": PTI_PRIVACY_NOTICE,
        "contact_email": "digitalplanningteam@levellingup.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions": "",
        "feedback_link": "",
        "project_name_field_id": "JAAhRP",  # TODO(adamdavies1) this might need changing
        "application_guidance": PTI_APPLICATION_GUIDANCE,
        "guidance_url": "",
        "all_uploaded_documents_section_available": False,
        "application_fields_download_available": False,
        "display_logo_on_pdf_exports": False,
        "requires_feedback": False,
        "mark_as_complete_enabled": True,
    }
]
