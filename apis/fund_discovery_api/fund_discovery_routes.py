"""
Imports the API from fund_app.py and creates the routes
in it.
"""
from apis.fund_discovery_api.fund_discovery_models import api
from apis.fund_discovery_api.fund_discovery_models import full_search_result
from apis.fund_discovery_api.fund_discovery_search import search
from apis.fund_store_api.fund_store_dummy_data import FUNDS
from flask_restx import Resource


@api.route("/<words>")
@api.param("words", "A series of hyphon seperated words.")
class FundList(Resource):
    @api.doc("search_funds")
    @api.marshal_list_with(full_search_result)
    def get(self, words):
        """List all funds"""
        return search(FUNDS.get_all(), words)
