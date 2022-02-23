from fund_api import api
from slugify import slugify


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


FUND_DATA = [
    {
        "name": "Harry's breakfast fund",
        "eligibility_criteria": {"maximium_project_cost": "10"},
        "rounds": [
            {
                "fund_name": "Harry's breakfast fund",
                "opens": "2022-02-01",
                "deadline": "2022-07-23",
            },
            {
                "fund_name": "Harry's breakfast fund",
                "opens": "2022-02-01",
                "deadline": "2022-07-23",
            },
        ],
    },
    {
        "name": "Ram's Get Fit Feb fund",
        "eligibility_criteria": {"maximium_project_cost": "100"},
        "rounds": [
            {
                "fund_name": "Ram's Get Fit Feb fund",
                "opens": "2022-02-01",
                "deadline": "2022-07-23",
            },
            {
                "fund_name": "Ram's Get Fit Feb fund",
                "opens": "2022-02-01",
                "deadline": "2022-07-23",
            },
        ],
    },
    {
        "name": "Funding service design",
        "eligibility_criteria": {"maximium_project_cost": "550"},
        "deadline": "2022-10-05",
        "opens": "2022-01-01",
        "rounds": [
            {
                "fund_name": "Funding Service Design",
                "opens": "2022-02-01",
                "deadline": "2022-07-23",
            },
            {
                "fund_name": "Funding Service Design",
                "opens": "2022-02-01",
                "deadline": "2022-07-23",
            },
        ],
    },
]

FUNDS = FundDAO()

for fund in FUND_DATA:

    FUNDS.create(fund)
