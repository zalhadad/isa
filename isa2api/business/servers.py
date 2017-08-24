from isa2api.database import db, where, select
from isa2api.business.auth import Auth


class Servers():

    def __init__(self):
        pass

    def get(self, p):
        return select("SELECT id,name FROM servers WHERE service=%(service)s", p)

    def __repr__(self):
        return None
