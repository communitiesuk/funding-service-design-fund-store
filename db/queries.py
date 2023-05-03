from typing import List

from db import db
from db.models.fund import Fund
from db.models.round import Round
from db.models.section import Section
from db.schemas.fund import FundSchema
from db.schemas.round import RoundSchema
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


def get_application_sections_for_round(round_id) -> List[Section]:
    application = db.session.scalars(
        select(Section)
        .filter(Section.round_id == round_id)
        .filter(Section.title == "Application")
    ).one()
    query = f"{application.path}.*{'{1}'}"
    lquery = expression.cast(query, LQUERY)
    application_sections = db.session.scalars(
        select(Section).filter(Section.path.lquery(lquery))
    ).all()
    return application_sections


def get_assessment_sections_for_round(round_id) -> List[Section]:
    assessment = db.session.scalars(
        select(Section)
        .filter(Section.round_id == round_id)
        .filter(Section.title == "Assessment")
    ).one()
    query = f"{assessment.path}.*{'{1}'}"
    lquery = expression.cast(query, LQUERY)
    assessment_sections = db.session.scalars(
        select(Section).filter(Section.path.lquery(lquery))
    ).all()
    return assessment_sections