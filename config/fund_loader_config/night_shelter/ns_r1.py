from config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    NIGHT_SHELTER_BASE_PATH,
)

NIGHT_SHELTER_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NIGHT_SHELTER_ROUND_1_ID = "fc7aa604-989e-4364-98a7-d1234271435a"
APPLICATION_BASE_PATH = ".".join([str(NIGHT_SHELTER_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(NIGHT_SHELTER_BASE_PATH), str(2)])

r1_application_sections = [
    {
        "section_name": "About your organisation",
        "tree_path": f"{APPLICATION_BASE_PATH}.1",
    },
    {
        "section_name": "1.1 Organisation Information",
        "form_name": "organisation-information-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.1.1",
    },
    {
        "section_name": "1.2 Organisation type",
        "form_name": "organisation-type-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.1.2",
    },
    {
        "section_name": "1.3 Applicant information",
        "form_name": "applicant-information-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.1.3",
    },
    {
        "section_name": "1.4 Joint applications",
        "form_name": "joint-applications-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.1.4",
    },
    {
        "section_name": "Your skills and experience",
        "tree_path": f"{APPLICATION_BASE_PATH}.2",
        "weighting": 10,
    },
    {
        "section_name": "2.1 Staff and volunteers",
        "form_name": "staff-and-volunteers-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.2.1",
    },
    {
        "section_name": "2.2 Current services",
        "form_name": "current-services-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.2.2",
    },
    {
        "section_name": "Your proposal",
        "tree_path": f"{APPLICATION_BASE_PATH}.3",
        "weighting": 45,
    },
    {
        "section_name": "3.1 Objectives and activities",
        "form_name": "objectives-and-activities-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.1",
    },
    {
        "section_name": "3.2 Project milestones",
        "form_name": "project-milestones-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.2",
    },
    {
        "section_name": "3.3 Local need and support",
        "form_name": "local-need-and-support-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.3",
    },
    {
        "section_name": "3.4 Proposed services",
        "form_name": "proposed-services-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.4",
    },
    {
        "section_name": "3.5 Working in partnership",
        "form_name": "working-in-partnership-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.5",
    },
    {
        "section_name": "3.6 Proposal sustainability",
        "form_name": "proposal-sustainability-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.6",
    },
    {
        "section_name": "Outputs and outcomes",
        "tree_path": f"{APPLICATION_BASE_PATH}.4",
        "weighting": 15,
    },
    {
        "section_name": "4.1 Outputs and outcomes",
        "form_name": "outputs-and-outcomes-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.1",
    },
    {
        "section_name": "Risk and deliverability",
        "tree_path": f"{APPLICATION_BASE_PATH}.5",
        "weighting": 15,
    },
    {
        "section_name": "5.1 Risk and deliverability",
        "form_name": "risk-and-deliverability-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.5.1",
    },
    {
        "section_name": "Value for money",
        "tree_path": f"{APPLICATION_BASE_PATH}.6",
        "weighting": 15,
    },
    {
        "section_name": "6.1 Funding required",
        "form_name": "funding-required-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.6.1",
    },
    {
        "section_name": "6.2 Building works",
        "form_name": "building-works-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.6.2",
    },
    {
        "section_name": "6.3 Match funding",
        "form_name": "match-funding-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.6.3",
    },
    {
        "section_name": "Check declarations",
        "tree_path": f"{APPLICATION_BASE_PATH}.7",
    },
    {
        "section_name": "7.1 Declarations",
        "form_name": "declarations-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.7.1",
    },
]

fund_config = {
    "id": NIGHT_SHELTER_FUND_ID,
    "name": "Night Shelter Fund",
    "title": "",
    "short_name": "NS",
    "description": "",
}

round_config = [
    {
        "id": NIGHT_SHELTER_ROUND_1_ID,
        "fund_id": NIGHT_SHELTER_FUND_ID,
        "title": "Round 1",
        "short_name": "R1",
        "opens": "2020-05-31 12:00:00",
        "deadline": "2025-07-12 11:59:00",
        "assessment_deadline": "2025-08-09 12:00:00",
        "prospectus": "",
        "privacy_notice": "",
        "contact_email": "COF@levellingup.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions": (
            "You must have received an invitation to apply. If we did not invite you,"
            " first <a"
            ' href="https://www.gov.uk/government/publications/community-ownership-fund-prospectus">'
            " express your interest in the fund</a>."
        ),
    }
]
