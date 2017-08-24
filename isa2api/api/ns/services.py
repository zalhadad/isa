import logging
from flask_restplus import Resource
from isa2api.api.parsers import token_arguments
from isa2api.api.restplus import api
from isa2api.business.services import Services
log = logging.getLogger(__name__)


ns = api.namespace('services', description='services list')


@ns.route("/")
@ns.expect(token_arguments)
class ServicesCtrl(Resource):
    """
     return current user's services
    """

    def get(self):
        s = Services()
        return s.get()
