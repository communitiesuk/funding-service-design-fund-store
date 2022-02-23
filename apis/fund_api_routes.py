"""
Imports the API from fund_app.py and creates the routes
in it.
"""
from apis.fund_api import api
from apis.fund_api import full_fund_model
from apis.fund_api import identify_fund_model
from apis.fund_api import round_model
from apis.fund_store_orm import FUNDS
from flask_restx import Resource


@api.route("/")
class FundList(Resource):
    @api.doc("list_funds")
    @api.marshal_list_with(identify_fund_model)
    def get(self):
        """List all funds"""
        return FUNDS.get_all()


@api.route("/<fund_identifer>")
@api.param("fund_identifer", "The id of the fund")
@api.response(404, "Fund not found")
class Fund(Resource):
    @api.doc("get_fund")
    @api.marshal_with(full_fund_model)
    def get(self, fund_identifer):
        """Fetch a fund given its name"""
        return FUNDS.get(fund_identifer)


@api.route("/<fund_identifer>/round/<round_number>")
@api.param("fund_identifer", "The round of the fund")
@api.param("round_number", "The round of the fund")
@api.response(404, "Round not found")
class Round(Resource):
    @api.doc("get_round")
    @api.marshal_with(round_model)
    def get(self, fund_identifer, round_number):
        """Fetch a fund given its name"""
        return FUNDS.get(fund_identifer)["rounds"][int(round_number)]
