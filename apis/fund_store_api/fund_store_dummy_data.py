from apis.fund_store_api.fund_store_dao import FundDAO


FUND_DATA = [
    {
        "fund_name": "Harry's breakfast fund",
        "fund_description": (
            "A fund designed to supply Harry's endless supply of muesli."
        ),
    },
    {
        "fund_name": "Ram's Get Fit Feb fund",
        "fund_description": (
            "A fund designed to supply gym memberships to home workers during"
            " Feb."
        ),
    },
    {
        "fund_name": "Funding service design",
        "fund_description": (
            "A fund designed to test the funding service design dev team."
        ),
    },
]

FUNDS = FundDAO()
FUNDS.load_dummy(FUND_DATA)
