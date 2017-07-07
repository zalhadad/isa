import logging

from flask import request
from flask_restplus import Resource
from .serializers import *
from .parsers import session_arguments,fromTo_arguments,token_arguments,paths_arguments
from .restplus import api
from isa2api.database.models import Sessions ,GlobalGraph, Session,History,Paths
log = logging.getLogger(__name__)


ns = api.namespace('sessions', description='sessions related informations')


@ns.route('/')
@api.expect(token_arguments)
class SessionsCtrl(Resource):

    @api.expect(session_arguments)
    @api.marshal_with(page_of_sessions)
    def get(self):
        """
        Returns list of session.
        """
        args = session_arguments.parse_args(request)
        sessions = Sessions(args)
        out = {'page': args.page,
            'pages': -(-sessions.total // args.per_page),
            'per_page': args.per_page,
            'total' : sessions.total ,
            'sessions' : sessions.get()
            }
        return  out


@ns.route('/history')
@api.expect(token_arguments)
@api.response(404, 'session not found.')
class HistoryOfSessions(Resource):
    @api.expect(fromTo_arguments)
    @api.marshal_with(graphItems)
    def get(self):
        """
        Returns global graph step with specified filter.
        """
        args = session_arguments.parse_args(request)
        g = GlobalGraph(args)
        return g.get()


@ns.route('/paths')
@api.expect(token_arguments)
@api.response(404, 'session not found.')
class TopPaths(Resource):
    @api.expect(paths_arguments)
    @api.marshal_with(graphItems)
    def get(self):
        """
        Returns paths graph step with specified filter.
        """
        args = paths_arguments.parse_args(request)
        p = Paths(args)
        return p.get()


@ns.route('/<id>')
@api.expect(token_arguments)
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
@api.expect(token_arguments)
@api.response(404, 'session not found.')
class HistoryCtrl(Resource):
    @api.marshal_with(sessionHistory)
    def get(self, id):
        """
        Returns session history steps.
        """
        history = History(id,True)
        return history.get()
