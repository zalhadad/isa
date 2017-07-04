# Flask settings
FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = True
RESTPLUS_ERROR_404_HELP = False
RESTPLUS_API_PREFIX = '/api/v1'
RESTPLUS_SUPER_SECRET = 'oh_so_secret'
RESTPLUS_TOKEN_EXPIRE = 3600

# Database settings
DATABASE = " host='localhost' dbname='stat' user='postgres' password='postgres' "