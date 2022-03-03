"""
Imports the API from fund_app.py and creates the routes
in it.
"""
from apis.fund_discovery_api.fund_discovery_models import api
from apis.fund_discovery_api.fund_discovery_models import full_search_result
from apis.fund_discovery_api.fund_discovery_search import search
from apis.fund_store_api.fund_store_dummy_data import FUNDS
from flask_restx import reqparse
from flask_restx import Resource

search_parser = reqparse.RequestParser()
search_parser.add_argument("search_items", action="split")


@api.route("/")
class FundSearch(Resource):
    @api.doc("search_funds")
    @api.marshal_list_with(full_search_result)
    @api.expect(search_parser)
    def post(self):
        """List all funds"""
        args = search_parser.parse_args()
        return search(FUNDS.get_all(), args["search_items"])
