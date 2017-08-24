import logging
from flask import make_response, abort
from flask_restplus import Resource
from isa2api.api.serializers import *
from isa2api.api.parsers import stat_args, stat_pages_args
from isa2api.api.restplus import api
from isa2api.business.reports import Stats
log = logging.getLogger(__name__)


ns = api.namespace('reports', description='reports calls/callers/nodes')

s = Stats()


@ns.route("/")
@ns.expect(stat_args)
class Calls(Resource):
    """
     decode token then send user
    """
    @api.response(200, 'valid token and not expired')
    def get(self):
        args = stat_args.parse_args()
        return s.get_calls(args)


@ns.route("/nodes")
@ns.expect(stat_pages_args)
class Nodes(Resource):
    """

    """

    def get(self):
        args = stat_pages_args.parse_args()
        out = {'page': args.page,
               'pages': -(-s.total_nodes // args.per_page),
               'per_page': args.per_page,
               'total': s.total_nodes,
               'data': s.get_nodes(args)
               }
        return out


@ns.route("/callers")
@ns.expect(stat_pages_args)
class Callers(Resource):
    """

    """

    def get(self):
        args = stat_pages_args.parse_args()
        out = {
            'page': args.page,
            'pages': -(-s.total_callers // args.per_page),
            'per_page': args.per_page,
            'total': s.total_callers,
            'data': s.get_callers(args)
        }
        return out
