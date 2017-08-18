import logging
from flask import make_response, abort
from flask_restplus import Resource, reqparse
from isa2api.api.serializers import *
from isa2api.api.parsers import login_arguments, token_arguments
from isa2api.api.restplus import api
from isa2api.business.nodes import Nodes
log = logging.getLogger(__name__)


ns = api.namespace('nodes', description='nodes names & labels')
parser = reqparse.RequestParser()
parser.add_argument('server', type=int, required=True,
                    help='Server id should be in Integer')

parser_label = parser.copy()
parser_label.add_argument(
    'label', type=str, required=True, help='Should be a string')


@ns.route("/")
@ns.expect(token_arguments)
class NodesCtrl(Resource):
    """
     send all nodes from this service
    """
    @ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        n = Nodes(args)
        return n.get()


@ns.route("/<name>")
class NodeCtrl(Resource):
    """
    update node name
    """

    @ns.expect(parser_label)
    def put(self, name):
        args = parser_label.parse_args()
        args.update({"name": name})
        n = Nodes(args)
        return n.update_node(args)

    @ns.expect(parser)
    def delete(self, name):
        args = parser.parse_args()
        n = Nodes(args)
        return n.delete_node_label({"name": name})
