from typing import List

from db import db
from db.models.fund import Fund
from db.models.round import Round
from db.models.section import Section
from db.schemas.fund import FundSchema
from db.schemas.round import RoundSchema
from db.schemas.section import SectionSchema
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.sql import expression
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


def get_fund_by_short_name(
    fund_short_name: str, as_json: bool = False
) -> Fund:
    fund = db.session.scalar(
        select(Fund).filter(
            func.lower(Fund.short_name) == func.lower(fund_short_name)
        )
    )
    if as_json:
        serialiser = FundSchema()
        return serialiser.dump(fund)
    else:
        return fund


def get_round_by_id(
    fund_id: str, round_id: str, as_json: bool = False
) -> Round:
    round = db.session.scalars(
        select(Round)
        .filter(Round.id == round_id)
        .filter(Round.fund_id == fund_id)
    ).one()
    if as_json:
        serialiser = RoundSchema()
        return serialiser.dump(round)
    else:
        return round


def get_rounds_for_fund_by_id(
    fund_id: str, as_json: bool = False
) -> List[Round]:
    rounds = db.session.scalars(
        select(Round).filter(Round.fund_id == fund_id)
    ).all()
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
        select(Section)
        .filter(Section.round_id == round_id)
        .order_by(Section.path)
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
