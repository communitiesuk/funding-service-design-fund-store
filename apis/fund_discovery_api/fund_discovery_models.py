"""Contains the set up for our API and a basic DAO
for prototyping.
"""
from flask_restx import fields
from flask_restx import Namespace

api = Namespace(
    "funds", description="Operations related to searching for fund infomation"
)

full_search_result = api.model(
    "Fund Search Result",
    {
        "fund_name": fields.String(
            required=True, description="The name of the fund"
        ),
        "fund_description": fields.String(
            required=True, description="The unique id for this fund"
        ),
    },
)
