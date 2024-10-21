# flake8: noqa
from config.fund_loader_config.cof.cof_r3 import APPLICATION_BASE_PATH_COF_R3_W3
from config.fund_loader_config.cof.cof_r3 import ASSESSMENT_BASE_PATH_COF_R3_W3
from config.fund_loader_config.cof.cof_r3 import COF_ROUND_3_WINDOW_3_ID
from config.fund_loader_config.cof.cof_r3 import cof_r3w3_sections
from config.fund_loader_config.cof.cof_r3 import round_config_w3
from db.queries import insert_base_sections
from db.queries import insert_or_update_application_sections
from db.queries import upsert_round_data


def main() -> None:
    print("'insert_fund_config(...)' not required as COFR3W3 shares the same fund config from COFR3w1.")
    print("Inserting round data.")
    upsert_round_data(round_config_w3)

    print("Inserting base sections config.")
    insert_base_sections(
        APPLICATION_BASE_PATH_COF_R3_W3,
        ASSESSMENT_BASE_PATH_COF_R3_W3,
        COF_ROUND_3_WINDOW_3_ID,
    )
    print("Inserting sections.")
    insert_or_update_application_sections(COF_ROUND_3_WINDOW_3_ID, cof_r3w3_sections)


if __name__ == "__main__":
    from app import app

    with app.app.app_context():
        main()
