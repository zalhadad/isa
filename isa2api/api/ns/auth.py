import logging
from flask import make_response
from flask_restplus import Resource
from isa2api.api.serializers import *
from isa2api.api.parsers import login_arguments, token_arguments
from isa2api.api.restplus import api
from isa2api.business.auth import Auth
log = logging.getLogger(__name__)


ns = api.namespace('auth', description='authenticate user')

auth = Auth()


@ns.route("/")
class AuthCtrl(Resource):
    """
     decode token then send user
    """
    @ns.expect(token_arguments)
    @api.response(200, 'valid token')
    def get(self):
        return auth.whoIs()

    @api.response(403, 'invalid user/password')
    @api.expect(login_arguments)
    def post(self):
        args = login_arguments.parse_args()
        token = auth.login(args)
        if not token:
            return make_response("{'message': 'username / password error'}", 403)
        return token
