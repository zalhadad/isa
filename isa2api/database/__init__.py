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
    sql = " WHERE server = %(server)s AND ( {}timestamp::date between %(fromDate)s::date AND %(toDate)s::date )  AND ( {}timestamp between %(fromDate)s AND %(toDate)s ) "
    if hasattr(p, 'id') and p.id != None:
        sql += ' AND id = %(id)s '
    if hasattr(p, 'caller') and p.caller != None:
        sql += ' AND caller=%(caller)s '
    if hasattr(p, 'called') and p.called != None:
        sql += ' AND called=%(called)s '
    if not t is None:
        t = t + '.'
    else:
        t = ''
    sql = sql.format(t, t)
    return sql


def types(t):
    return select("""select t.typname as name, array_agg(enumlabel) as value from pg_type t    join pg_enum e on t.oid=e.enumtypid  
                    join pg_catalog.pg_namespace n ON n.oid=t.typnamespace where t.typname=%(t)s
        group by name
                 """, {"t": t})
