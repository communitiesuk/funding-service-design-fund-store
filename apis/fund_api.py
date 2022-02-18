from flask_restx import Namespace, Resource, fields

api = Namespace('funds', description='Operations related to fund infomation')

eligibility_criteria = api.model('Eligibility', {
    'maximium_project_cost' : fields.Integer(description='The maxmium amount a project can ask for')
})

fund_model = api.model('Fund', {
    'name': fields.String(required=True, description='The name of the fund'),
    'identifer': fields.String(required=True, description="The unique id for this fund"),
    'eligibility_criteria': fields.Nested(eligibility_criteria, desciption="The eligiblity criteria of the fund"),
    'deadline' : fields.DateTime(description="The fund closing date"),
    'opens' : fields.DateTime(required=True, description="The fund opening date")
})

FUNDS = [
    {
        "name" : "Harry's breakfast fund",
        "eligibility_criteria": {"maximium_project_cost" : "10"},
        "deadline" : "2022-12-25",
        "opens" : "2022-11-25",
        "identifer" : "harrys-breakfast-fund"
    },
        {
        "name" : "Ram's Get Fit Feb fund",
        "eligibility_criteria": {"maximium_project_cost" : "100"},
        "deadline" : "2022-12-31",
        "opens" : "2022-01-01",
        "identifer" : "rams-get-fit-feb-fund"
    }
]

@api.route('/')
class FundList(Resource):
    @api.doc('list_funds')
    @api.marshal_list_with(fund_model)
    def get(self):
        '''List all funds'''
        return FUNDS

@api.route('/<identifer>')
@api.param('identifer', 'The id of the fund')
@api.response(404, 'Fund not found')
class Fund(Resource):
    @api.doc('get_fund')
    @api.marshal_with(fund_model)
    def get(self, identifer):
        '''Fetch a fund given its name'''
        for fund in FUNDS:
            if fund['identifer'] == identifer:
                return fund
        api.abort(404)