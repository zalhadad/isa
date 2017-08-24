import logging
from flask import make_response, abort
from flask_restplus import Resource, reqparse
from isa2api.api.serializers import *
from isa2api.api.parsers import login_arguments, token_arguments
from isa2api.api.restplus import api
from isa2api.business.servers import Servers
log = logging.getLogger(__name__)


ns = api.namespace('servers', description='servers list')
parser = reqparse.RequestParser()
parser.add_argument('service', type=int, required=True,
                    help='service id should be in Integer')


@ns.route("/")
@ns.expect(token_arguments)
@ns.expect(parser)
class ServersCtrl(Resource):
    @api.expect(login_arguments)
    def get(self):
        args = parser.parse_args()
        s = Servers()
        return s.get(args)
