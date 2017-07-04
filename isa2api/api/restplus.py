import logging
import traceback

from flask_restplus import Api
from isa2api.decorators.auth import auth_required 
from isa2api.api.parsers import token_arguments

from isa2api import settings

log = logging.getLogger(__name__)


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    },
    'token': {
        'type': 'apiKey',
        'in': 'query',
        'name': 'token'
    }
    
}
api = Api(version='1.0', title='ISA 2 API',
          description='Interactive Software Analyzer API',decorators=[auth_required],doc='/doc/')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500