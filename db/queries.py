from typing import List

from db import db
from db.models.fund import Fund
from db.models.round import Round
from db.models.section import Section
from sqlalchemy import select


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


def sections_filter(round_id) -> List[Section]:
    app = db.session.scalars(
        select(Section)
        .filter(Section.round_id == round_id)
        .filter(Section.title == "Application")
    ).one()
    application_sections = db.session.scalars(
        select(Section).filter(Section.path.descendant_of(app))
    ).all()
    return application_sections
