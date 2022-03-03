"""
Imports the API from fund_app.py and creates the routes
in it.
"""
from apis.fund_store_api.fund_api_models import api
from apis.fund_store_api.fund_api_models import full_fund_model
from apis.fund_store_api.fund_api_models import identify_fund_view
from apis.fund_store_api.fund_store_dummy_data import FUNDS
from flask_restx import Resource


@api.route("/")
class FundList(Resource):
    @api.doc("list_funds")
    @api.marshal_list_with(identify_fund_view)
    def get(self):
        """List all funds"""
        return FUNDS.get_all()


@api.route("/<fund_identifier>")
@api.param("fund_identifier", "The id of the fund")
@api.response(404, "Fund not found")
class Fund(Resource):
    @api.doc("get_fund")
    @api.marshal_with(full_fund_model)
    def get(self, fund_identifier):
        """Fetch a fund given its name"""
        return FUNDS.get(fund_identifier)
