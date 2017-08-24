import json
from isa2api.database import db, where, select
import datetime


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


class Stats():

    def __init__(self):
        self.total_callers = 0
        self.total_nodes = 0

    def get_calls_frequency(self, params):
        sql = "select * from calls_frequency(%(fromDate)s,%(toDate)s,%(server)s);"
        return select(sql, params)

    def get_calls_category(self, params):
        sql = "select * from calls_category(%(fromDate)s,%(toDate)s,%(server)s);"
        return select(sql, params)

    def get_calls_stat(self, params):
        sql = "select * from calls_stat(%(fromDate)s,%(toDate)s,%(server)s);"
        return select(sql, params)

    def get_calls(self, params):
        res = {
            "global": self.get_calls_stat(params),
            "categories": self.get_calls_category(params),
            "frequency": {"name": "call_frequency", "series": self.get_calls_frequency(params)}
        }
        return json.loads(json.dumps(res, default=datetime_handler))

    def get_nodes(self, params):
        params.setdefault('offset', (params.page - 1) * params.per_page)
        sql = "SELECT node,count(*) from  sessions_history h  inner join sessions s on h.session = s.id" + \
            where(params, 's')
        sql += " AND node <> '' group by node ORDER BY " + params.get('sort') + ' ' + params.get(
            'order') + ' LIMIT %(per_page)s OFFSET %(offset)s '
        sql2 = "SELECT count(*) FROM  (SELECT DISTINCT node FROM sessions_history h  inner join sessions s on h.session = s.id" + \
            where(params, 's')
        sql2 += " AND node <> '' ) as t "
        self.total_nodes = select(sql2, params)[0]['count']
        return select(sql, params)

    def get_callers(self, params):
        params.setdefault('offset', (params.page - 1) * params.per_page)
        sql = "SELECT caller,count(*) FROM sessions" + where(params)
        sql += ' group by caller ORDER BY ' + params.get('sort') + ' ' + params.get(
            'order') + ' LIMIT %(per_page)s OFFSET %(offset)s '

        sql2 = "SELECT count(*) FROM ( SELECT DISTINCT caller FROM sessions" + \
            where(params) + " ) as t"
        self.total_callers = select(sql2, params)[0]['count']
        return select(sql, params)
