# flake8: noqa
from config.fund_loader_config.cof.cof_r4 import APPLICATION_BASE_PATH_COF_R4_W2
from config.fund_loader_config.cof.cof_r4 import ASSESSMENT_BASE_PATH_COF_R4_W2
from config.fund_loader_config.cof.cof_r4 import COF_ROUND_4_WINDOW_2_ID
from config.fund_loader_config.cof.cof_r4 import cof_r4w2_sections
from config.fund_loader_config.cof.cof_r4 import round_config_w2
from db.queries import insert_base_sections
from db.queries import insert_or_update_application_sections
from db.queries import insert_round_data


def main() -> None:
    print("'insert_fund_config(...)' not required as COFR4W2 shares the same fund config from COFR4w1.")
    print("Inserting round data.")
    insert_round_data(round_config_w2)

    print("Inserting base sections config.")
    insert_base_sections(
        APPLICATION_BASE_PATH_COF_R4_W2,
        ASSESSMENT_BASE_PATH_COF_R4_W2,
        COF_ROUND_4_WINDOW_2_ID,
    )
    print("Inserting sections.")
    insert_or_update_application_sections(COF_ROUND_4_WINDOW_2_ID, cof_r4w2_sections)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
