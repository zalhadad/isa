from sqlalchemy import create_engine
from isa2api.settings import DATABASE

# init
db = create_engine(DATABASE)


def select(q, p=None):
    r = db.execute(q, p)
    return [dict(zip(r.keys(), x)) for x in r]


def estimate(q, p=None):
    r = db.execute("select estimate('" + q + "')", p)
    return r.scalar()


def where(p, t=None):
    sql = " WHERE server = %(server)s AND {}timestamp::date between %(fromDate)s::date AND %(toDate)s::date AND {}timestamp between %(fromDate)s AND %(toDate)s "
    if p.id != None:
        sql += ' AND id = %(id)s '
    if p.caller != None:
        sql += ' AND caller=%(caller)s '
    if p.called != None:
        sql += ' AND called=%(called)s '
    if not t is None:
        t = t + '.'
    else:
        t = ''
    sql = sql.format(t, t)
    return sql
