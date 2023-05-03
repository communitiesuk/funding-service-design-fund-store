from db.queries import get_all_funds
from db.queries import get_fund_by_id
from db.queries import get_fund_by_short_name
from distutils.util import strtobool
from flask import abort
from flask import request


def get_funds():
    # language = request.args.get("language")

    funds = get_all_funds(True)

    if funds:
        return funds

    abort(404)


def get_fund(fund_id):
    # language = request.args.get("language")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        fund = get_fund_by_short_name(fund_id, True)
    else:
        fund = get_fund_by_id(fund_id, True)

    if fund:
        return fund

    abort(404)
