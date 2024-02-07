import config.fund_loader_config.cyp.cyp_r1 as cyp_r1
from db import db
from db.models.round import Round
from flask import current_app
from sqlalchemy import update


def update_rounds_with_application_guidance(rounds):
    for round in rounds:
        current_app.logger.info(f"\tRound: {round['short_name']} ({round['id']})")
        if round.get("application_guidance"):
            current_app.logger.info("\t\tUpdating application_guidance")
            stmt = (
                update(Round).where(Round.id == round["id"]).values(application_guidance=round["application_guidance"])
            )

            db.session.execute(stmt)
        else:
            current_app.logger.info("\t\tNo application_guidance defined")
    db.session.commit()


def main() -> None:
    current_app.logger.info("Updating application_guidance field for CYP")
    update_rounds_with_application_guidance(cyp_r1.round_config)
    current_app.logger.info("Updates complete")


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
