#!/usr/bin/env python3
from datetime import datetime
from datetime import timedelta

import click
from config.fund_loader_config.cof.cof_r2 import rounds_config as cof_r2_configs
from config.fund_loader_config.cof.cof_r3 import round_config as cof_r3w1_config
from config.fund_loader_config.cof.cof_r3 import round_config_w2 as cof_r3w2_config
from config.fund_loader_config.cof.cof_r3 import round_config_w3 as cof_r3w3_config
from config.fund_loader_config.cof.cof_r4 import round_config_w1 as cof_r4_configs
from config.fund_loader_config.cof.eoi import round_config_eoi as cof_eoi_configs
from config.fund_loader_config.cyp.cyp_r1 import round_config as cyp_config
from config.fund_loader_config.digital_planning.dpi_r2 import round_config as dpif_config
from config.fund_loader_config.night_shelter.ns_r2 import round_config as nstf_config
from db import db
from db.models import Round

ROUND_IDS = {
    "COF_R2W2": "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
    "COF_R2W3": "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f",
    "COF_R3W1": "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762",
    "COF_R3W2": "6af19a5e-9cae-4f00-9194-cf10d2d7c8a7",
    "COF_R3W3": "4efc3263-aefe-4071-b5f4-0910abec12d2",
    "COF_R4W1": "33726b63-efce-4749-b149-20351346c76e",
    "COF_EOI": "6a47c649-7bac-4583-baed-9c4e7a35c8b3",
    "NSTF_R2": "fc7aa604-989e-4364-98a7-d1234271435a",
    "CYP_R1": "888aae3d-7e2c-4523-b9c1-95952b3d1644",
    "DPIF_R2": "0059aad4-5eb5-11ee-8c99-0242ac120002",
}

ALL_ROUNDS_CONFIG = {
    ROUND_IDS["COF_R2W2"]: cof_r2_configs[0],
    ROUND_IDS["COF_R2W3"]: cof_r2_configs[1],
    ROUND_IDS["COF_R3W1"]: cof_r3w1_config[0],
    ROUND_IDS["COF_R3W2"]: cof_r3w2_config[0],
    ROUND_IDS["COF_R3W3"]: cof_r3w3_config[0],
    ROUND_IDS["COF_R4W1"]: cof_r4_configs[0],
    ROUND_IDS["COF_EOI"]: cof_eoi_configs[0],
    ROUND_IDS["NSTF_R2"]: nstf_config[0],
    ROUND_IDS["CYP_R1"]: cyp_config[0],
    ROUND_IDS["DPIF_R2"]: dpif_config[0],
}
NONE = "none"
UNCHANGED = "unchanged"
PAST = "past"
FUTURE = "future"

DEFAULTS = {
    "round_short_name": None,
}


class DynamicPromptOption(click.Option):
    def prompt_for_value(self, ctx):
        q = ctx.obj.get("q")
        if q:
            return DEFAULTS.get(self.name, UNCHANGED)
        return super().prompt_for_value(ctx)


@click.group()
@click.option("-q", help="Disable all prompts", flag_value=True, default=False)
@click.pass_context
def cli(ctx, q):
    # Ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)
    # Apply group-wide feature switches
    ctx.obj["q"] = q


@cli.command
@click.option(
    "-r",
    "--round_short_name",
    type=click.Choice(ROUND_IDS.keys()),
    default="COF_R4W1",
    prompt=True,
    cls=DynamicPromptOption,
    help="Short name for round, will be mapped to round ID. Not needed if round_id supplied.",
)
@click.option(
    "-rid",
    "--round_id",
    prompt=False,
    default=None,
    help="UUID for round. Not needed if a valid round_short_name supplied",
)
@click.option(
    "-o",
    "--application_opens",
    default=UNCHANGED,
    prompt=True,
    cls=DynamicPromptOption,
)
@click.option(
    "-d",
    "--application_deadline",
    default=UNCHANGED,
    prompt=True,
    cls=DynamicPromptOption,
)
@click.option(
    "-as",
    "--assessment_start",
    default=UNCHANGED,
    prompt=True,
    cls=DynamicPromptOption,
)
@click.option(
    "-ad",
    "--assessment_deadline",
    default=UNCHANGED,
    prompt=True,
    cls=DynamicPromptOption,
)
def update_round_dates(
    round_short_name=None,
    round_id=None,
    application_opens=None,
    application_deadline=None,
    assessment_start=None,
    assessment_deadline=None,
):
    """Updates round dates for the supplied round ID. For any property, the following values are possible:
        - UNCHANGED: Leave existing value in place
        - PAST: Set to a date 5 days in the past
        - FUTURE: Set to a date 5 days in the future
        - Specific date in the format YYYY-mm-dd HH:MM:SS

    For assessment_start, the following value is also available:
        - NONE: Set the assessment_start to null"""
    if not round_id:
        round_id = ROUND_IDS[round_short_name]

    round_to_update = Round.query.get(round_id)
    date_in_past = (datetime.now() + timedelta(days=-5)).strftime("%Y-%m-%d %H:%M:%S")
    date_in_future = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    commit = False
    if application_opens and not application_opens.casefold() == UNCHANGED:
        commit = True

        if application_opens.casefold() == PAST:
            round_to_update.opens = date_in_past
        elif application_opens.casefold() == FUTURE:
            round_to_update.opens = date_in_future
        else:
            round_to_update.opens = datetime.strptime(application_opens, "%Y-%m-%d %H:%M:%S")

    if application_deadline and not application_deadline.casefold() == UNCHANGED:
        commit = True

        if application_deadline.casefold() == PAST:
            round_to_update.deadline = date_in_past
        elif application_deadline.casefold() == FUTURE:
            round_to_update.deadline = date_in_future
        else:
            round_to_update.deadline = datetime.strptime(application_deadline, "%Y-%m-%d %H:%M:%S")

    if assessment_start and not assessment_start.casefold() == UNCHANGED:
        commit = True

        if assessment_start.casefold() == NONE:
            round_to_update.assessment_start = None
        elif assessment_start.casefold() == PAST:
            round_to_update.assessment_start = date_in_past
        elif assessment_start.casefold() == FUTURE:
            round_to_update.assessment_start = date_in_future
        else:
            round_to_update.assessment_start = datetime.strptime(assessment_start, "%Y-%m-%d %H:%M:%S")

    if assessment_deadline and not assessment_deadline.casefold() == UNCHANGED:
        commit = True

        if assessment_deadline.casefold() == PAST:
            round_to_update.assessment_deadline = date_in_past
        elif assessment_deadline.casefold() == FUTURE:
            round_to_update.assessment_deadline = date_in_future
        else:
            round_to_update.deadline = datetime.strptime(assessment_deadline, "%Y-%m-%d %H:%M:%S")

    if commit:
        db.session.commit()
        print(f"Sucessfully updated the round dates for {round_short_name if round_short_name else ''} [{round_id}].")
    else:
        print("No changes supplied")
    return


@cli.command
@click.option(
    "-r",
    "--round_short_name",
    type=click.Choice(ROUND_IDS.keys()),
    default="COF_R4W1",
    prompt=True,
    cls=DynamicPromptOption,
)
@click.option("-rid", "--round_id", prompt=False, default=None)
def reset_round_dates(round_id, round_short_name):
    """Resets the dates for the supplied round to the dates in the fund loader config"""
    if not round_id:
        round_id = ROUND_IDS[round_short_name]

    round_to_update = Round.query.get(round_id)
    reset_config = ALL_ROUNDS_CONFIG[round_id]
    round_to_update.opens = reset_config["opens"]
    round_to_update.deadline = reset_config["deadline"]
    round_to_update.assessment_start = reset_config["assessment_start"]
    round_to_update.assessment_deadline = reset_config["assessment_deadline"]
    db.session.commit()
    print(
        f"Sucessfully reset the round dates for {round_short_name if round_short_name else ''} [{round_id}] to the"
        " dates in the fund loader config"
    )


if __name__ == "__main__":
    from app import app

    with app.app_context():
        cli()
