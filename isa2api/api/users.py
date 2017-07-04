import logging
from flask import make_response,abort
from flask_restplus import Resource
from .serializers import *
from .parsers import login_arguments,token_arguments
from .restplus import api
from isa2api.business.users import User 
log = logging.getLogger(__name__)



ns = api.namespace('users', description='sessions related informations')

user = User()
@ns.route("/me")
@ns.expect(token_arguments)
class Me(Resource):
    """
     decode token then send user
    """
    @api.response(200, 'valid token and not expired')
    def get(self):
        return user.decodeToken() 

@ns.route('/authenticate')
class Auth(Resource):
    @api.expect(login_arguments)
    def post(self):
        args = login_arguments.parse_args()
        token = user.login(args)
        if not token:
            return make_response("{'message': 'username / password error'}",403)
        return token
