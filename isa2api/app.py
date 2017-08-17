#!/usr/bin/env python
import logging.config

from flask import Flask, Blueprint
from isa2api import settings
from isa2api.api.ns.services import ns as servicesNs
from isa2api.api.ns.servers import ns as serversNs
from isa2api.api.ns.nodes import ns as nodesNs
from isa2api.api.ns.jobs import ns as jobsNs
from isa2api.api.ns.users import ns as usersNs
from isa2api.api.ns.auth import ns as authNs
from isa2api.api.ns.sessions import ns as sessionsNs
from isa2api.api.ns.graphs import ns as graphsNs
from isa2api.api.ns.reports import ns as reportsNs
from isa2api.api.restplus import api

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config.SWAGGER_UI_LANGUAGES = settings.RESTPLUS_SWAGGER_LANG


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint(
        'api', __name__, url_prefix=settings.RESTPLUS_API_PREFIX)
    api.init_app(blueprint)
    api.add_namespace(servicesNs)
    api.add_namespace(serversNs)
    api.add_namespace(nodesNs)
    api.add_namespace(jobsNs)
    api.add_namespace(usersNs)
    api.add_namespace(authNs)
    api.add_namespace(sessionsNs)
    api.add_namespace(graphsNs)
    api.add_namespace(reportsNs)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    log.info('>>>>> Starting server <<<<<')
    app.run(debug=settings.FLASK_DEBUG,
            host=settings.FLASK_HOST, port=settings.FLASK_PORT)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Expose-Headers', 'X-API-KEY')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,X-API-KEY')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == "__main__":
    main()
