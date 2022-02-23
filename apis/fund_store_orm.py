from apis.fund_api import api
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
                "opens": "2022-02-01",
                "deadline": "2022-07-23",
            },
            {
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
                "opens": "2022-02-01",
                "deadline": "2022-07-23",
            },
            {
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
                "opens": "2022-02-01",
                "deadline": "2022-07-23",
            },
            {
                "opens": "2022-02-01",
                "deadline": "2022-07-23",
            },
        ],
    },
]

for fund in FUND_DATA:

    for round_num in range(len(fund["rounds"])):

        fund["rounds"][round_num]["round_identifer"] = round_num + 1


FUNDS = FundDAO()

for fund in FUND_DATA:

    FUNDS.create(fund)
