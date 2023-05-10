from typing import List

from db import db
from db.models.form_name import FormName
from db.models.fund import Fund
from db.models.round import Round
from db.models.section import AssessmentField
from db.models.section import Section
from db.models.section import SectionField
from db.schemas.fund import FundSchema
from db.schemas.round import RoundSchema
from db.schemas.section import SectionSchema
from sqlalchemy import bindparam
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.sql import expression
from sqlalchemy_utils import Ltree
from sqlalchemy_utils.types.ltree import LQUERY


def get_all_funds(as_json: bool = False) -> List[Fund]:
    funds = db.session.scalars(select(Fund)).all()
    if as_json:
        serialiser = FundSchema()
        return serialiser.dump(funds, many=True)
    else:
        return funds


def get_fund_by_id(fund_id: str, as_json: bool = False) -> Fund:
    fund = db.session.scalars(select(Fund).filter(Fund.id == fund_id)).one()
    if as_json:
        serialiser = FundSchema()
        return serialiser.dump(fund)
    else:
        return fund


def get_fund_by_short_name(fund_short_name: str, as_json: bool = False) -> Fund:
    fund = db.session.scalar(
        select(Fund).filter(func.lower(Fund.short_name) == func.lower(fund_short_name))
    )
    if as_json:
        serialiser = FundSchema()
        return serialiser.dump(fund)
    else:
        return fund


def get_round_by_id(fund_id: str, round_id: str, as_json: bool = False) -> Round:
    round = db.session.scalars(
        select(Round).filter(Round.id == round_id).filter(Round.fund_id == fund_id)
    ).one()
    if as_json:
        serialiser = RoundSchema()
        return serialiser.dump(round)
    else:
        return round


def get_rounds_for_fund_by_id(fund_id: str, as_json: bool = False) -> List[Round]:
    rounds = db.session.scalars(select(Round).filter(Round.fund_id == fund_id)).all()
    if as_json:
        serialiser = RoundSchema()
        return serialiser.dump(rounds, many=True)
    else:
        return rounds


def get_round_by_short_name(
    fund_short_name: str, round_short_name: str, as_json: bool = False
) -> Round:
    round = db.session.scalar(
        select(Round)
        .filter(func.lower(Round.short_name) == func.lower(round_short_name))
        .join(Fund)
        .filter(func.lower(Fund.short_name) == func.lower(fund_short_name))
    )
    if as_json:
        serialiser = RoundSchema()
        return serialiser.dump(round)
    else:
        return round


def get_rounds_for_fund_by_short_name(fund_short_name, as_json: bool = False):
    rounds = db.session.scalars(
        select(Round)
        .join(Fund)
        .filter(func.lower(Fund.short_name) == func.lower(fund_short_name))
    ).all()
    if as_json:
        serialiser = RoundSchema()
        return serialiser.dump(rounds, many=True)
    else:
        return rounds


def get_sections_for_round(round_id) -> List[Section]:
    return db.session.scalars(
        select(Section).filter(Section.round_id == round_id).order_by(Section.path)
    ).all()


def get_application_sections_for_round(
    fund_id, round_id, as_json: bool = False
) -> List[Section]:
    application_level = db.session.scalar(
        select(Section)
        .filter(Section.round_id == round_id)
        .filter(Section.title == "Application")
        .join(Round)
        .filter(Round.fund_id == fund_id)
    )
    if not application_level:
        return None

    query = f"{application_level.path}.*{'{1}'}"
    lquery = expression.cast(query, LQUERY)
    application_sections = db.session.scalars(
        select(Section).filter(Section.path.lquery(lquery))
    ).all()

    if as_json:
        serialiser = SectionSchema(many=True)
        return serialiser.dump(application_sections)
    else:
        return application_sections


def get_assessment_sections_for_round(
    fund_id, round_id, language, as_json: bool = False
) -> List[Section]:
    assessment_level = db.session.scalar(
        select(Section)
        .filter(Section.round_id == round_id)
        .filter(Section.title == "Assessment")
        .join(Round)
        .filter(Round.fund_id == fund_id)
    )
    if not assessment_level:
        return None

    query = f"{assessment_level.path}.*{'{1}'}"
    lquery = expression.cast(query, LQUERY)
    # select(Section).join(Translation, onclause=(Section.title_content_id ==
    #  Translation.content_id) and (Translation.language == 'en'),
    #  isouter=True)
    # .filter(Section.id == 12)
    assessment_sections = db.session.scalars(
        select(Section)
        # .join
        # (
        #     Translation,
        #     onclause=and_((Translation.language == language),
        # (Section.title_content_id == Translation.content_id)),
        #     isouter=True
        # )
        # select (Section).filter(Section.path.lquery(lquery))
        # select(Section).join(Translation, onclause=f"section.title_content_id
        #  = translation.content_id and translation.language='{language}'",
        # isouter=True).filter(Section.path.lquery(lquery))
        .filter(Section.path.lquery(lquery))
    ).all()

    if as_json:
        serialiser = SectionSchema(many=True)
        return serialiser.dump(assessment_sections)
    else:
        return assessment_sections


def upsert_fields(fields: list):

    stmt = (
        (
            postgres_insert(AssessmentField).values(
                id=bindparam("id"),
                title=bindparam("title"),
                field_type=bindparam("field_type"),
                display_type=bindparam("display_type"),
            )
        )
        .on_conflict_do_nothing(index_elements=[AssessmentField.id])
        .returning(AssessmentField.id)
    )

    update_params = [
        {
            "id": item["form_json_id"],
            "title": item["title"],
            "field_type": item["type"],
            "display_type": item["presentation_type"],
        }
        for item in fields
    ]

    result = db.session.execute(stmt, update_params)
    inserted_field_ids = [row.id for row in result]
    return inserted_field_ids


def insert_fund_data(fund_config):
    stmt = (
        insert(Fund).values(
            id=bindparam("id"),
            name=bindparam("name"),
            title=bindparam("title"),
            short_name=bindparam("short_name"),
            description=bindparam("description"),
        )
    ).returning(Fund.id)

    update_params = {
        "id": fund_config["id"],
        "name": fund_config["name"],
        "title": fund_config["title"],
        "short_name": fund_config["short_name"],
        "description": fund_config["description"],
    }

    result = db.session.execute(stmt, update_params)
    inserted_fund_ids = [row.id for row in result]
    db.session.commit()
    return inserted_fund_ids


def insert_round_data(round_config):
    stmt = (
        insert(Round).values(
            id=bindparam("id"),
            title=bindparam("title"),
            short_name=bindparam("short_name"),
            opens=bindparam("opens"),
            deadline=bindparam("deadline"),
            fund_id=bindparam("fund_id"),
            assessment_deadline=bindparam("assessment_deadline"),
            prospectus=bindparam("prospectus"),
            privacy_notice=bindparam("privacy_notice"),
            contact_email=bindparam("contact_email"),
            contact_phone=bindparam("contact_phone"),
            contact_textphone=bindparam("contact_textphone"),
            support_times=bindparam("support_times"),
            support_days=bindparam("support_days"),
            instructions=bindparam("instructions"),
        )
    ).returning(Round.id)

    update_params = [
        {
            "id": item["id"],
            "title": item["title"],
            "short_name": item["short_name"],
            "opens": item["opens"],
            "deadline": item["deadline"],
            "fund_id": item["fund_id"],
            "assessment_deadline": item["assessment_deadline"],
            "prospectus": item["prospectus"],
            "privacy_notice": item["privacy_notice"],
            "contact_email": item["contact_email"],
            "contact_phone": item["contact_phone"],
            "contact_textphone": item["contact_textphone"],
            "support_times": item["support_times"],
            "support_days": item["support_days"],
            "instructions": item["instructions"],
        }
        for item in round_config
    ]

    result = db.session.execute(stmt, update_params)
    inserted_round_ids = [row.id for row in result]
    db.session.commit()
    return inserted_round_ids


def insert_application_sections(round_id, sorted_application_sections: dict):
    inserted_section_ids = []
    for section in sorted_application_sections:

        stmt = (
            insert(Section).values(
                round_id=bindparam("round_id"),
                title=bindparam("title"),
                weighting=bindparam("weighting"),
                path=bindparam("path"),
            )
        ).returning(Section.id)

        update_params = {
            "round_id": round_id,
            "title": section["section_name"],
            "weighting": None,
            "path": Ltree(section["tree_path"]),
        }

        result = db.session.execute(stmt, update_params).fetchall()
        inserted_section_id = result[0].id
        inserted_section_ids.append(inserted_section_id)

        if section.get("form_name"):
            form_stmt = insert(FormName).values(
                section_id=bindparam("section_id"),
                form_name=bindparam("form_name"),
            )
            form_params = {
                "section_id": inserted_section_id,
                "form_name": section["form_name"],
            }
            db.session.execute(form_stmt, form_params)
    db.session.commit()
    return inserted_section_ids


def __add__section_fields(field_section_links):
    stmt = (
        (
            postgres_insert(SectionField).values(
                field_id=bindparam("field_id"),
                section_id=bindparam("section_id"),
                display_order=bindparam("display_order"),
            )
        )
        .on_conflict_do_nothing(constraint="pk_section_field")
        .returning(
            SectionField.field_id,
            SectionField.section_id,
            SectionField.display_order,
        )
    )

    field_section_params = [
        {
            "field_id": section_link["field_id"],
            "section_id": section_link["section_id"],
            "display_order": section_link["display_order"],
        }
        for section_link in field_section_links
    ]

    inserted_field_section_result = db.session.execute(
        stmt, field_section_params
    ).fetchall()
    return inserted_field_section_result


def insert_assessment_sections(round_id, assessment_config: list):
    sorted_assessment_sections = (
        assessment_config["sorted_scored_sections"]
        + assessment_config["sorted_unscored_sections"]
    )

    stmt = (
        insert(Section).values(
            round_id=bindparam("round_id"),
            title=bindparam("title"),
            weighting=bindparam("weighting"),
            path=bindparam("path"),
        )
    ).returning(Section.id)

    inserted_section_ids = []
    field_section_links = []
    for section in sorted_assessment_sections:

        section_params = {
            "round_id": round_id,
            "title": section["section_name"],
            "weighting": None,
            "path": Ltree(section["tree_path"]),
        }
        inserted_assessment_section_result = db.session.execute(
            stmt, section_params
        ).fetchall()
        inserted_section_id = inserted_assessment_section_result[0][0]
        inserted_section_ids.append(inserted_section_id)
        if "fields" in section:
            for field in section["fields"]:
                field_section_links.append(
                    {
                        "field_id": field["form_json_id"],
                        "section_id": inserted_section_id,
                        "display_order": field["display_order"],
                    }
                )

    # flush so we can see the rows in the db before committing
    # db.session.commit()
    inserted_section_field_links = __add__section_fields(field_section_links)
    db.session.commit()
    return {
        "inserted_sections": inserted_section_ids,
        "inserted_section_field_links": inserted_section_field_links,
    }
