# flake8: noqa
from config.fund_loader_config.digital_planning.pti_r4 import APPLICATION_BASE_PATH
from config.fund_loader_config.digital_planning.pti_r4 import ASSESSMENT_BASE_PATH
from config.fund_loader_config.digital_planning.pti_r4 import fund_config
from config.fund_loader_config.digital_planning.pti_r4 import PTI_ROUND_4_ID
from config.fund_loader_config.digital_planning.pti_r4 import r4_application_sections
from config.fund_loader_config.digital_planning.pti_r4 import round_config
from db.queries import insert_assessment_sections
from db.queries import insert_base_sections
from db.queries import insert_fund_data
from db.queries import insert_or_update_application_sections
from db.queries import insert_round_data


def main() -> None:
    print("Inserting fund data for the DPI fund.")
    insert_fund_data(fund_config)
    print("Inserting round data for round 2 of the DPI fund.")
    insert_round_data(round_config)

    print("Inserting base sections for DPI Round 2.")
    insert_base_sections(APPLICATION_BASE_PATH, ASSESSMENT_BASE_PATH, PTI_ROUND_4_ID)
    print("Inserting application sections for DPI Round 2.")
    insert_or_update_application_sections(PTI_ROUND_4_ID, r4_application_sections)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
