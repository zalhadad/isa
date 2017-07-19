import logging
import traceback

from flask_restplus import Api
from flask import make_response
from isa2api.decorators.auth import auth_required
from isa2api.api.parsers import token_arguments

from isa2api import settings

log = logging.getLogger(__name__)

api = Api(version='1.1', title='ISA 2 API',
          description='Interactive Software Analyzer API', decorators=[auth_required], doc='/')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.representation('image/svg+xml')
def output_svg(data, code, headers=None):
    print(data)
    """Makes a Flask response with a svg encoded body"""
    resp = make_response(data, code, {"Content-Type": "image/svg+xml"})
    return resp
