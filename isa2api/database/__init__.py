import psycopg2
import psycopg2.extras
from isa2api.settings import DATABASE

connection = psycopg2.connect(DATABASE,cursor_factory=psycopg2.extras.RealDictCursor)

