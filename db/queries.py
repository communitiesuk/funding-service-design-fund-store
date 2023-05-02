from db import db
from db.models.fund import Fund
from db.models.round import Round
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
