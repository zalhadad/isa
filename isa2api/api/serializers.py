from flask_restplus import fields
from ..api.restplus import api

session = api.model('Session inforamtion', {
    'id': fields.String(readOnly=True, description='The unique identifier of session'),
    'caller': fields.String(description='Caller number'),
    'called': fields.String(description='Called number'),
    'timestamp': fields.DateTime(description='Session date'),
    'duration': fields.Integer(description='Session duration'),
    'server': fields.String(),
    'info': fields.String(),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of items'),
})

page_of_sessions = api.inherit('Page of sessions', pagination, {
    'sessions': fields.List(fields.Nested(session))
})

node = api.model('Node', {
    'id': fields.String(description='Node unique identifier'),

})
edge = api.model('Edge', {
    'from': fields.String(description='source node identifier'),
    'to': fields.String(description='target node identifier'),
    'duration': fields.String(description='Node unique identifier'),

})
sessionHistory = api.model('Session inforamtion', {
    'id': fields.String(readOnly=True, description='The unique identifier of session'),
    'nodes': fields.List(fields.Nested(node)),
    'edges': fields.List(fields.Nested(edge))
})

