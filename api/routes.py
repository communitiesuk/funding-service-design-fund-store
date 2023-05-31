from db.queries import get_all_funds
from db.queries import get_application_sections_for_round
from db.queries import get_assessment_sections_for_round
from db.queries import get_fund_by_id
from db.queries import get_fund_by_short_name
from db.queries import get_round_by_id
from db.queries import get_round_by_short_name
from db.queries import get_rounds_for_fund_by_id
from db.queries import get_rounds_for_fund_by_short_name
from db.schemas.fund import FundSchema
from db.schemas.round import RoundSchema
from db.schemas.section import SectionSchema
from distutils.util import strtobool
from flask import abort
from flask import request
from fsd_utils.locale_selector.get_lang import get_lang


def filter_fund_by_lang(fund_data, lang_key: str = "en"):
    def filter_fund(data):
        out = {}
        for k, v in data.items():
            if k == "name_json":
                out["name"] = v[lang_key]
                continue

            if k == "title_json":
                out["title"] = v[lang_key]
                continue

            if k == "description_json":
                out["description"] = v[lang_key]
                continue

            out[k] = v

        return out

    if isinstance(fund_data, dict):
        fund = filter_fund(fund_data)
    elif isinstance(fund_data, list):
        fund = [filter_fund(item) for item in fund_data]
    else:
        fund = fund_data

    return fund


def filter_round_by_lang(round_data, lang_key: str = "en"):
    def filter_round(data):
        out = {}
        for k, v in data.items():
            if k == "title_json":
                out["title"] = v[lang_key]
                continue
            out[k] = v
        return out

    if isinstance(round_data, dict):
        round = filter_round(round_data)
    elif isinstance(round_data, list):
        round = [filter_round(item) for item in round_data]
    else:
        round = round_data

    return round


def get_funds():
    language = request.args.get("language", "en")
    funds = get_all_funds()

    if funds:
        serialiser = FundSchema()
        return filter_fund_by_lang(
            fund_data=serialiser.dump(funds, many=True), lang_key=language
        )

    abort(404)


def get_fund(fund_id):
    language = request.args.get("language", "en")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        fund = get_fund_by_short_name(fund_id)
    else:
        fund = get_fund_by_id(fund_id)

    if fund:
        serialiser = FundSchema()
        return filter_fund_by_lang(fund_data=serialiser.dump(fund), lang_key=language)

    abort(404)


def get_round(fund_id, round_id):
    language = request.args.get("language", "en")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        round = get_round_by_short_name(fund_id, round_id)
    else:
        round = get_round_by_id(fund_id, round_id)
    if round:
        serialiser = RoundSchema()
        return filter_round_by_lang(
            round_data=serialiser.dump(round), lang_key=language
        )

    abort(404)


def get_rounds_for_fund(fund_id):
    language = request.args.get("language", "en")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        rounds = get_rounds_for_fund_by_short_name(fund_id)
    else:
        rounds = get_rounds_for_fund_by_id(fund_id)

    if rounds:
        serialiser = RoundSchema()
        return filter_round_by_lang(
            round_data=serialiser.dump(rounds), lang_key=language
        )

    abort(404)


def get_sections_for_round_application(fund_id, round_id):
    sections = get_application_sections_for_round(fund_id, round_id)
    if sections:
        serialiser = SectionSchema()
        return serialiser.dump(sections, many=True)

    abort(404)


def get_sections_for_round_assessment(fund_id, round_id):
    sections = get_assessment_sections_for_round(fund_id, round_id, get_lang())
    if sections:
        serialiser = SectionSchema()
        return serialiser.dump(sections, many=True)

    abort(404)
