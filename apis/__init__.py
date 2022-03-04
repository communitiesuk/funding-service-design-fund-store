from apis.fund_discovery_api.fund_discovery_routes import api as discovery_api
from apis.fund_store_api.fund_api_routes import api as fund_api
from flask_restx import Api

api = Api(
    title="Fund Store API",
    version="0.2",
    description=(
        "An api for requesting infomation about funds from the fund store"
    ),
    # All API metadatas
)

api.add_namespace(fund_api, path="/funds")

api.add_namespace(discovery_api, path="/funds/search")
