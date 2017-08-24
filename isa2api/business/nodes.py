from isa2api.database import db, where, select


class Nodes():

    def __init__(self, params):
        r = db.execute("select service from servers where id=%(id)s",
                       {"id": params.get('server')})
        self.service = r.scalar()

    def get(self):
        sql = "SELECT name,label FROM nodes where service = %(service)s ORDER BY name"
        return select(sql, {"service": self.service})

    def __repr__(self):
        return None

    def update_node(self, params):
        sql = "update nodes set label=%(label)s where service = %(service)s and name = %(name)s"
        params.update({"service": self.service})
        db.execute(sql, params)
        sql = "SELECT name,label FROM nodes where service = %(service)s and name = %(name)s"
        return select(sql, params)

    def delete_node_label(self, params):
        print(params)
        sql = "update nodes set label='' where service = %(service)s and name = %(name)s"
        params.update({"service": self.service})
        db.execute(sql, params)
        sql = "SELECT name,label FROM nodes where service = %(service)s and name = %(name)s"
        return select(sql, params)
