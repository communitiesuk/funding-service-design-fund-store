from db.queries import get_fund_by_id
from db.queries import get_fund_by_short_name
from distutils.util import strtobool
from flask import request


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

    return 404
