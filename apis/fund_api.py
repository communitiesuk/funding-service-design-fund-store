from flask_restx import Namespace, Resource, fields

api = Namespace('funds', description='Operations related to fund infomation')

eligibility_criteria = api.model('Eligibility', {
    'maximium_project_cost' : fields.Integer(description='The maxmium amount a project can ask for')
})

fund_model = api.model('Fund', {
    'name': fields.String(required=True, description='The name of the fund'),
    'eligibility criteria': fields.Nested(eligibility_criteria, desciption="The eligiblity criteria of the fund"),
    'closing date' : fields.DateTime(required=True, description="The fund closing date")
})

FUNDS = [
    {
        "name" : "Harry's breakfast fund",
        "eligibility criteria": {"maximium_project_cost" : "10"},
        "closing date" : "2022-12-25" 
    }
]

@api.route('/')
class FundList(Resource):
    @api.doc('list_funds')
    @api.marshal_list_with(fund_model)
    def get(self):
        '''List all funds'''
        return FUNDS

@api.route('/<name>')
@api.param('name', 'The name of the fund')
@api.response(404, 'Fund not found')
class Fund(Resource):
    @api.doc('get_fund')
    @api.marshal_with(fund_model)
    def get(self, name):
        '''Fetch a fund given its name'''
        for fund in FUNDS:
            if fund['name'] == name:
                return fund
        api.abort(404)