from flask import current_app
from sqlalchemy import update

import config.fund_loader_config.cof.eoi as eoi
from db import db
from db.models.round import Round


def update_rounds_with_links(round_config):
    current_app.logger.warning(f"\tRound: {round_config[0]['short_name']} ({round_config[0]['id']})")
    if round_config[0].get("instructions_json"):
        current_app.logger.warning("\t\tUpdating instructions & application_guidance")
        stmt = (
            update(Round)
            .where(Round.id == round_config[0]["id"])
            .values(
                instructions_json=round_config[0]["instructions_json"],
                application_guidance_json=round_config[0]["application_guidance_json"],
            )
        )

        db.session.execute(stmt)
    db.session.commit()


def main() -> None:
    current_app.logger.warning("Updating instructions & application_guidance for EOI")
    update_rounds_with_links(eoi.round_config_eoi)
    current_app.logger.warning("Updates complete")


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
