import pandas as pd
import isa2api.database as db
import json


class Sessions():
    
    def __init__(self,params):
        params.setdefault('server',-1)
        params.setdefault('per_page',10)
        params.setdefault('page',10)
        params.setdefault('offset', (params.page - 1 ) * params.per_page  )
        sql="SELECT * FROM sessions WHERE server = %(server)s "
        if params.id != None:
            sql += ' AND id LIKE %(id)s'        
        if params.caller != None:
            sql += ' AND caller=%(caller)s'        
        if params.called != None:
            sql += ' AND called=%(called)s'        
        if params.fromDate != None:
            sql += ' AND timestamp::date >= %(fromDate)s::date'        
        if params.fromDate != None:
            sql += ' AND timestamp >= %(fromDate)s'        
        if params.toDate != None:
            sql += ' AND timestamp::date <= %(toDate)s::date'        
        if params.toDate != None:
            sql += ' AND timestamp <= %(toDate)s'        
        sql += ' ORDER BY timestamp desc LIMIT %(per_page)s OFFSET %(offset)s '
       
       
        sql2="SELECT count(*) FROM sessions WHERE server = %(server)s "
        if params.id != None:
            sql2 += ' AND id LIKE %(id)s'        
        if params.caller != None:
            sql2 += ' AND caller=%(caller)s'        
        if params.called != None:
            sql2 += ' AND called=%(called)s'        
        if params.fromDate != None:
            sql2 += ' AND timestamp::date >= %(fromDate)s::date'        
        if params.fromDate != None:
            sql2 += ' AND timestamp >= %(fromDate)s'        
        if params.toDate != None:
            sql2 += ' AND timestamp::date <= %(toDate)s::date'        
        if params.toDate != None:
            sql2 += ' AND timestamp <= %(toDate)s' 
        cursor = db.connection.cursor()
        try:
            cursor.execute(sql2,params)
            self.total = cursor.fetchone()['count']
            cursor.close()
        except:
            self.total = 0
            db.connection.rollback()
        self.data = pd.read_sql(sql,db.connection,params=params)
    
    def get(self):
        return json.loads(self.data.to_json(orient='records',date_format='iso'))


    def __repr__(self):
        return self.data.to_json(orient='records')



class Session():
    
    def __init__(self,id):
        try:
            sql = 'select * from sessions WHERE id=%(id)s'
            cursor = db.connection.cursor()
            cursor.execute(sql,{'id': id})
            self.session = cursor.fetchone()
            cursor.close()
        except:
            db.connection.rollback()
    def get(self):
        return self.session


class History():
    
    def __init__(self,id):
        self.id = id
        sql = "SELECT timestamp,node FROM sessions_history WHERE session=%(id)s AND node <> '' ORDER BY timestamp"
        history = pd.read_sql(sql,db.connection,params={'id' : self.id})
        self.nodes = [dict({'id' : x}) for x in history['node'].unique()]

        sources = history['node'][0:-1].values
        targets = history['node'][1:].values
        durations = history['timestamp'].diff()[1::].values.astype('timedelta64[ms]')
        edgesList = list(zip(sources, targets, durations))
        print(sources)
        self.edges = [dict({'from' : x[0], 'to' : x[1], 'duration' : x[2]}) for x in edgesList]

    def get(self):
        return { 'id' : self.id,  'nodes' : self.nodes , 'edges' : self.edges}