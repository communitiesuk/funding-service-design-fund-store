"""
Imports the API from fund_app.py and creates the routes
in it.
"""
from apis.fund_discovery_api.fund_discovery_dao import FundDiscoveryDAO
from apis.fund_discovery_api.fund_discovery_dummy_data import FUND_DATA
from apis.fund_discovery_api.fund_discovery_models import api
from apis.fund_discovery_api.fund_discovery_models import full_search_result
from flask_restx import Resource

FUNDS = FundDiscoveryDAO()
FUNDS.load_dummy(FUND_DATA)


@api.route("/<words>")
@api.param("words", "A series of hyphon seperated words.")
class FundList(Resource):
    @api.doc("search_funds")
    @api.marshal_list_with(full_search_result)
    def get(self, words):
        """List all funds"""
        return FUNDS.search(words)
