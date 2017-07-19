import logging

from flask import request, make_response
from flask_restplus import Resource
from isa2api.api.serializers import page_of_sessions, session_history
from isa2api.api.parsers import session_arguments, filter_arguments, token_arguments
from isa2api.api.restplus import api
from isa2api.business.sessions import Sessions, History
log = logging.getLogger(__name__)


ns = api.namespace('sessions', description='sessions related informations')


@ns.route('/')
@ns.expect(token_arguments, session_arguments)
class SessionsCtrl(Resource):

    #@api.marshal_with(page_of_sessions)
    def get(self):
        """
        Returns list of session.
        """
        args = session_arguments.parse_args(request)
        sessions = Sessions(args)
        out = {'page': args.page,
               'pages': -(-sessions.total // args.per_page),
               'per_page': args.per_page,
               'total': sessions.total,
               'sessions': sessions.get()
               }
        return out


@ns.route('/<id>')
@ns.expect(token_arguments, filter_arguments)
class HistoryCtrl(Resource):
    @api.marshal_with(session_history)
    def get(self, id):
        """
        Returns session history steps.
        """
        history = History(id, True).get()
        return history
