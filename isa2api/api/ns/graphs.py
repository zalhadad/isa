import logging
from io import BytesIO
from flask import send_file, make_response
from flask_restplus import Resource
from isa2api.api.serializers import *
from isa2api.api.parsers import token_arguments, paths_arguments, filter_arguments
from isa2api.api.restplus import api
from isa2api.business.graphs import *
log = logging.getLogger(__name__)


ns = api.namespace('graphs', description='Graphs : global & top paths')


@ns.route("/")
@ns.expect(token_arguments, filter_arguments)
class GlobalCtrl(Resource):
    def get(self):
        """
        return global graph as json
        """
        args = filter_arguments.parse_args()
        graph = GlobalGraph(args)
        return graph.get()


@ns.route('/paths')
@ns.expect(token_arguments, paths_arguments)
class PathsCtrl(Resource):
    def get(self):
        """
        return top paths graph as svg
        """
        args = paths_arguments.parse_args()
        paths = Paths(args)
        svg = paths.svg()
        if(len(paths.get()['nodes'])):
            buffer = BytesIO()
            buffer.write(svg)
            buffer.seek(0)
            return send_file(buffer, as_attachment=False, mimetype='image/svg+xml')
        return make_response('', 204)
