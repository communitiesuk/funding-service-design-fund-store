"""empty message

Revision ID: b5f7bf2831de
Revises: 5fe9a48b7739
Create Date: 2023-05-31 18:56:06.440068

FS-2701: Adds relevant welsh translations to the fund-store for form_name table.

Authors: https://github.com/tferns

"""
import json

import sqlalchemy
from alembic import op

# revision identifiers, used by Alembic.
revision = "b5f7bf2831de"
down_revision = "5fe9a48b7739"
branch_labels = None
depends_on = None

english_form_name_to_welsh_form_name = {
    "applicant-information": "gwybodaeth-am-y-ymgeisydd",
    "asset-information": "gwybodaeth-am-yr-ased",
    "community-benefits": "buddion-cymunedol",
    "community-engagement": "ymgysylltu-a'r-gymuned",
    "community-representation": "cynrychiolaeth-gymunedol",
    "community-use": "defnydd-cymunedol",
    "declarations": "datganiadau",
    "environmental-sustainability": "cynaliadwyedd-amgylcheddol",
    "feasibility": "cynhwysiant-ac-integreiddio",
    "funding-required": "cyllid-sydd-ei-angen",
    "inclusiveness-and-integration": "cynhwysiant-ac-integreiddio",
    "local-support": "cefnogaeth-leol",
    "operational-costs": "costau-gweithredol",
    "organisation-information": "gwybodaeth-am-y-sefydliad",
    "project-costs": "costau'r-prosiect",
    "project-information": "gwybodaeth-am-y-prosiect",
    "project-qualification": "cymhwystra'r-prosiect",
    "project-qualifications": "cymhwysedd-y-prosiect",
    "risk": "risg",
    "skills-and-resources": "sgiliau-ac-adnoddau",
    "upload-business-plan": "lanlwythwch-y-cynllun-busnes",
    "value-to-the-community": "gwerth-i'r-gymuned",
}


def upgrade():
    connection = op.get_bind()
    query = sqlalchemy.text("SELECT form_name_json FROM form_name")
    form_name_entries = connection.execute(query)

    for form_name_json, *_ in form_name_entries:
        original_english_form_name = form_name_json["en"]
        if original_english_form_name.endswith("-cof-r3-w1"):
            r3 = True
            english_form_name = original_english_form_name[: -len("-cof-r3-w1")]
        else:
            r3 = False
            english_form_name = original_english_form_name

        is_night_shelter = english_form_name.endswith("-ns")
        if is_night_shelter:
            continue

        welsh_form_name = english_form_name_to_welsh_form_name.get(english_form_name)
        if not welsh_form_name:
            raise Exception(
                f"Could not find welsh form name for {form_name_json['en']}"
            )

        welsh_form_name = welsh_form_name.replace("'", "''")

        form_name_json["cy"] = welsh_form_name
        if r3:
            form_name_json["cy"] += "-cof-r3-w1"

        new_form_name_json_str = json.dumps(form_name_json)
        update_query = sqlalchemy.text(
            f"UPDATE form_name SET form_name_json = '{new_form_name_json_str}' "
            f"WHERE form_name_json->>'en' = '{original_english_form_name}'"
        )
        connection.execute(update_query)


def downgrade():
    connection = op.get_bind()
    query = sqlalchemy.text(
        "SELECT form_name_json FROM form_name WHERE form_name_json->>'cy' IS NOT NULL"
    )
    form_name_entries = connection.execute(query)

    for form_name_json, *_ in form_name_entries:
        original_welsh_form_name = form_name_json["cy"].replace("'", "''")

        del form_name_json["cy"]
        new_form_name_json_str = json.dumps(form_name_json)

        update_query = sqlalchemy.text(
            f"UPDATE form_name SET form_name_json = '{new_form_name_json_str}' "
            f"WHERE form_name_json->>'cy' = '{original_welsh_form_name}'"
        )
        connection.execute(update_query)
