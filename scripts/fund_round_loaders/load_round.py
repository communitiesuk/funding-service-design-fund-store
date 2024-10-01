# flake8: noqa
from config.fund_loader_config.FAB.round_config import LOADER_CONFIG
from db import db
from db.queries import insert_assessment_sections
from db.queries import insert_base_sections
from db.queries import insert_fund_data
from db.queries import insert_or_update_application_sections
from db.queries import insert_round_data

# Variables (needs to be checked/validated)


"""
See required schema for import here: file_location
"""
ROUND_BASE_PATH = LOADER_CONFIG["base_path"]

# End of variables

if not LOADER_CONFIG.get("fund_config", None):
    print("No fund config found in the loader config.")
else:
    FUND_CONFIG = LOADER_CONFIG["fund_config"]

if not LOADER_CONFIG.get("round_config", None):
    print("No round config found in the loader config.")
else:
    ROUND_CONFIG = LOADER_CONFIG["round_config"]

APPLICATION_BASE_PATH = ".".join([str(ROUND_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(ROUND_BASE_PATH), str(2)])


def main() -> None:
    """
    Insert the FAB fund and round data into the database.
    """

    if FUND_CONFIG:
        FUND_SHORT = FUND_CONFIG["short_name"]
        print(f"Preparing fund data for the {FUND_SHORT} fund.")
        insert_fund_data(FUND_CONFIG)

    if ROUND_CONFIG:
        print(f"Preparing round data for the '{FUND_SHORT}' fund.")
        insert_round_data(ROUND_CONFIG)

        # Section config is per round, not per fund
        round_short_name = ROUND_CONFIG["short_name"]
        print(f"Preparing base sections for {round_short_name}.")
        insert_base_sections(APPLICATION_BASE_PATH, ASSESSMENT_BASE_PATH, ROUND_CONFIG["id"])

        print(f"Preparing application sections for {round_short_name}.")
        insert_or_update_application_sections(ROUND_CONFIG["id"], LOADER_CONFIG["sections_config"])

    print(f"All config has been successfully prepared, now committing to the database.")
    db.session.commit()
    print(f"Config has now been committed to the database.")


if __name__ == "__main__":
    from app import app

    with app.app.app_context():
        main()
