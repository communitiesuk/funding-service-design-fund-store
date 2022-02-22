"""Contains the set up for our API and a basic DAO
for prototyping.
"""
from flask_restx import fields
from flask_restx import Namespace
from slugify import slugify

api = Namespace("funds", description="Operations related to fund infomation")

eligibility_criteria = api.model(
    "Eligibility",
    {
        "maximium_project_cost": fields.Integer(
            description="The maxmium amount a project can ask for"
        )
    },
)

full_fund_model = api.model(
    "Fund Full Data",
    {
        "name": fields.String(
            required=True, description="The name of the fund"
        ),
        "fund_identifer": fields.String(
            required=True, description="The unique id for this fund"
        ),
        "eligibility_criteria": fields.Nested(
            eligibility_criteria,
            desciption="The eligiblity criteria of the fund",
        ),
        "deadline": fields.DateTime(description="The fund closing date"),
        "opens": fields.DateTime(
            required=True, description="The fund opening date"
        ),
    },
)

identify_fund_model = api.model(
    "Fund Summary",
    {
        "name": fields.String(
            required=True, description="The name of the fund"
        ),
        "fund_identifer": fields.String(
            required=True, description="The unique id for this fund"
        ),
    },
)

FUND_DATA = [
    {
        "name": "Harry's breakfast fund",
        "eligibility_criteria": {"maximium_project_cost": "10"},
        "deadline": "2022-12-25",
        "opens": "2022-11-25",
    },
    {
        "name": "Ram's Get Fit Feb fund",
        "eligibility_criteria": {"maximium_project_cost": "100"},
        "deadline": "2022-12-31",
        "opens": "2022-01-01",
    },
]


class FundDAO:
    def __init__(self):
        self.funds = {}

    def get_all(self):
        return list(self.funds.values())

    def create(self, data):
        key = slugify(data["name"])
        data["fund_identifer"] = key
        self.funds[key] = data

    def get(self, identifer):
        if identifer in self.funds.keys():
            return self.funds[identifer]
        api.abort(404, f"Fund {identifer} doesn't exist")


FUNDS = FundDAO()

for fund in FUND_DATA:

    FUNDS.create(fund)
