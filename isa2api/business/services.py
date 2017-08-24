from isa2api.database import db, where, select
from isa2api.business.auth import Auth


class Services():

    def __init__(self):
        auth = Auth()
        self.current_user = auth.whoIs().get('username')

    def get(self):
        print(self.current_user)
        return select("SELECT id,name,role FROM services s RIGHT JOIN permissions p ON s.id = p.service WHERE p.user=%(user)s", {
            "user": self.current_user})

    def __repr__(self):
        return None
