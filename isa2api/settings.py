# Flask settings
FLASK_DEBUG = True  # Do not use debug mode in production
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 8888
# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_SWAGGER_LANG = ['en', 'fr']
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = True
RESTPLUS_ERROR_404_HELP = False
RESTPLUS_API_PREFIX = '/api/v1'
RESTPLUS_SUPER_SECRET = 'oh_so_secret'
RESTPLUS_TOKEN_EXPIRE = 3600


# Database settings

# best way !
#DATABASE = 'postgres:///stat'

# via TCP socket
DATABASE = "postgres://isa:pass@localhost/isa"
