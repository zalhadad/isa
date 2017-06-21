import logging

from flask import request
from flask_restplus import Resource
from .serializers import *
from .parsers import session_arguments
from .restplus import api
from isa2api.database.models import Sessions , Session,History
log = logging.getLogger(__name__)

ns = api.namespace('sessions', description='sessions related informations')

@ns.route('/')
class SessionsCtrl(Resource):

    @api.expect(session_arguments)
    @api.marshal_with(page_of_sessions)
    def get(self):
        """
        Returns list of session.
        """
        args = session_arguments.parse_args(request)
        sessions = Sessions((args))
        out = {'page': args.page,
            'pages': -(-sessions.total // args.per_page),
            'per_page': args.per_page,
            'total' : sessions.total ,
            'sessions' : sessions.get()
            }
        return  out

@ns.route('/<id>')
@api.response(404, 'session not found.')
class SessionCtrl(Resource):

    @api.marshal_with(session)
    def get(self, id):
        """
        Returns session information.
        """
        session = Session(id)
        return session.get()

@ns.route('/<id>/history')
@api.response(404, 'session not found.')
class HistoryCtrl(Resource):
    @api.marshal_with(sessionHistory)
    def get(self, id):
        """
        Returns session history steps.
        """
        history = History(id)
        return history.get()