from flask_restx import Api

from .fund_api import api as fund_api

api = Api(
    title='My Title',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(fund_api)