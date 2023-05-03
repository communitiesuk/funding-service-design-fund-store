from typing import List

from db import db
from db.models.fund import Fund
from db.models.round import Round
from db.models.section import Section
from sqlalchemy import select
from sqlalchemy.sql import expression
from sqlalchemy_utils.types.ltree import LQUERY


def get_fund_by_id(fund_id: str) -> Fund:
    return db.session.scalars(select(Fund).filter(Fund.id == fund_id)).one()


def get_fund_by_short_name(fund_short_name: str) -> Fund:
    return db.session.scalars(
        select(Fund).filter(Fund.short_name == fund_short_name)
    ).one()


def get_round_by_id(round_id: str) -> Round:
    return db.session.scalars(select(Round).filter(Round.id == round_id)).one()


def get_round_by_short_name(round_short_name: str) -> Round:
    return db.session.scalars(
        select(Round).filter(Round.short_name == round_short_name)
    ).one()


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
